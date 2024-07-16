import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

def get_file_paths(folder_path):
    """
    get_file_paths: iterate a folder and its sub folders, return the path of all files in this folder
    """
    file_paths = []
    # Iterate through all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.pdf'):
                # Get the absolute path of the file
                file_path = os.path.join(root, file_name)
                # Append the file path to the list
                file_paths.append(file_path)
            else:
                pass
    return file_paths


def create_client_and_assistant(api_key, model, assistant_name, assistant_instruction):
    """
    create an OPENAI client
    """
    client = OpenAI(api_key=api_key)
    assistant = client.beta.assistants.create(
        name = assistant_name,
        instructions = assistant_instruction,
        tools = [{"type": "file_search"}],
        model = model
        )
    return client, assistant


def create_vector_store(client, vector_store_name, rag_file_folder, rag_file_count):
    """
    create_vector_store for a client and upload the files to the vector store
    """
    # create a Vector Store
    vector_store = client.beta.vector_stores.create(name=vector_store_name)
    # add rag files into the vector store
    file_paths = get_file_paths(rag_file_folder)
    # print(f'\nfile_paths: {file_paths}\n')
    if rag_file_count == 1:
        file_streams = [open(path, 'rb') for path in file_paths[0:1]]
    elif rag_file_count > 1:
        file_streams = [open(path, 'rb') for path in file_paths[0:rag_file_count]]
    else:
        print('!!!No RAG FILES!!!')
        file_streams = [open(path, 'rb') for path in file_paths[0:rag_file_count]]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
    )
    # check if the status of the files vectorization 
    print(f'File batch status: {file_batch.status}')
    print(f'Number of files uploaded: {file_batch.file_counts}')
    return vector_store


def get_response(prompt,client,assistant):
    # create a thread and add message to the thread
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    # create a run
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # get messages
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    # print(message_content.value)
    # print("\n".join(citations))
    return message_content.value,citations


def save_to_file(text, file):
    """
    save_to_file: save output to a txt file
    """
    with open(file, 'w') as file:
    # Step 3: Write the multi-line string to the file
        file.write(text)


def main(rag_file_count, tempterature, iteration):
    # load environment setting and env variables
    load_dotenv()
    api_key = os.getenv('OPEN_API_KEY')
    model = os.getenv('MODEL')
    assistant_name = os.getenv('ASSISTANT_NAME')
    rag_file_folder = os.getenv('RAG_FILE_FOLDER')
    # rag_file_count = int(os.getenv('RAG_FILE_COUNT'))
    vector_store_name = os.getenv('VECTOR_STORE_NAME')
    # tempterature = float(os.getenv('TEMPERATURE'))
    assistant_instruction = os.getenv('INSTRUCTION')
    prompt = os.getenv('PROMPT')
    print(f'rag file: {rag_file_folder}')
    print(os.getcwd())
    print(f"prompt: {prompt}")
    print(f"rag_file_count: {rag_file_count}")

    # create output folders for intermediate and final results
    os.makedirs('gpt-output', exist_ok=True)

    output_folder = f'gpt-output/rag-file-count-{rag_file_count}'
    os.makedirs(output_folder, exist_ok=True)

    # Chat with RAG-based LLM
    client,assistant = create_client_and_assistant(api_key, model, assistant_name, assistant_instruction)
    print('creating vector store ......')
    vector_store = create_vector_store(client, vector_store_name, rag_file_folder, rag_file_count)
    # update the assistant with the vector store
    print('updating assistant ......')
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    print('Asking GPT ......')
    while True:
        try:
            output_response, output_ref = get_response(prompt,client,assistant)
            # print(f"query: {prompt}")
            # print(f'response: {output_response}')
            # print(f"reference: {output_ref}")
            cq_output_file = f'gpt-output/rag-file-count-{rag_file_count}/{model}-temp-{tempterature}-iteration-{iteration}.txt'
            save_to_file(output_response, cq_output_file)
            print(f'output file: {cq_output_file}')
            break
        except:
            print('\n*************No message returned, keep trying')
            continue


if __name__ == "__main__":
    main()

