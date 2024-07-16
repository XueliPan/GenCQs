import os
import sys
from dotenv import load_dotenv
from openai import OpenAI


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
    # tempterature = float(os.getenv('TEMPERATURE'))
    assistant_instruction = os.getenv('CHAT_INSTRUCTION')
    prompt = os.getenv('PROMPT')
    print(os.getcwd())
    print(f"prompt: {prompt}")

    output_folder = f'gpt-output/rag-file-count-{rag_file_count}'
    os.makedirs(output_folder, exist_ok=True)

    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": assistant_instruction},
            {"role": "user", "content": prompt}])
    output_response = completion.choices[0].message.content
    cq_output_file = f'gpt-output/rag-file-count-{rag_file_count}/{model}-temp-{tempterature}-iteration-{iteration}.txt'
    save_to_file(output_response, cq_output_file)
    print(f'output file: {cq_output_file}')

if __name__ == "__main__":
    main()

