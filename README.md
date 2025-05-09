### Generating Competency Question using LLMs

#### Domains
- [hci: Human Computer Interaction](hci/)
- [re: Requirement Engeneering](re/)

#### Parameter setting
- [.env.example](hci/.env.example): environment and parameters settings, needs to replace the value of API KEY with your own OPENAI api key.

#### Code(hci)
- [chatGenerate.py](hci/chatGenerate.py): generates CQs using just LLM prompting, output a list of generative CQs
- [RAGgenerate.py](hci/RAGgenerate.py): generates CQs using just RAG, output a list of generative CQs
- [generate-iteration.py](hci/generate-iteration.py): iteration of each parameter settings in chatGenerate.py or RAGgenerate.py
- [similarity.py](hci/similarity.py): similarity calculation between generative CQs and ground-truth CQs
- [similarity-iteration.py](hci/similarity.py): iteration of each parameter settings in similariy.py
- [plotting.ipynb](hci/ploting.ipynb): plots the evaluation metrics

#### Data(hci)
- [references](hci/reference/): papers in PDF format as input to the RAG
- [ground-truth-cqs.txt](hci/ground-truth-cqs.txt): 15 ground truth CQs for HCI refernce ontology

#### Results(hci)
- [gpt-output](hci/gpt-output/): output of the [generate-iteration.py](hci/generate-iteration.py), contains generative CQs with different number of papers as input to the RAG, differnt temperature, and different iteration.
- [all-cos-results](hci/all-cos-results/): cosinie similarity of all pairs of (genCQs, gtCQs), here in HCI is 15*15 pairs
- [highest-cos-results](hci/highest-cos-results/): cosinie similarity of best pairs of (genCQs, gtCQs), here in HCI is 15 pairs
- [metric-results](hci:metric-results/): Precision and Recall for 10 iteration

### How we calculate the similarity between the genCQ and the expertCQ (ground truth)

#### Step 1: generating CQs. 

For the frist task in HCI domain, there are 15 expertCQs, so we ask LLMs to generate 15 genCQs using the following prompt:

<img src="https://media.springernature.com/lw685/springer-static/image/chp%3A10.1007%2F978-3-031-81974-2_6/MediaObjects/641861_1_En_6_Figc_HTML.png" alt="Text document titled &quot;Listing 3: Prompt for HCI&quot; detailing a task for an expert in Human-Computer Interaction. The task involves developing a reference ontology about human-computer interaction, grounded in Unified Foundational Ontology. The goal is to create clear definitions of domain concepts for communication, learning, and problem-solving. The document requests the derivation of 15 competency questions for the ontology using provided documents, specifying that only the competency questions should be returned." style="zoom:67%;" /> 

The raw output are save in [hci/gpt-output](hci/gpt-output).

The meaning of files in this directory is as follows:

e.g. [rag-file-count-3/gpt-4o-temp-0.5-iteration-0.txt](hci/gpt-output/rag-file-count-3/gpt-4o-temp-0.5-iteration-0.txt)

- rag-file-count-3: number of scientific papers in the domain, used as the knowledge base for RAG, rag-file-count-0 means there is no RAG, only the prompt.
- gpt-4o-temp-0.5-iteration-0.txt: using get-4o with temperature = 0.5, the first iteration. For each setting we run for 10 times and get the average for the final evaluation metrics.

#### Step 2: calculate the similarity, results save at [all_cos_results](hci/all_cos_results)

Explanation of the similarity results in [hci/all_cos_results/rag-file-count-2/gpt-4o-temp-0.5-1.csv](hci/all_cos_results/rag-file-count-2/gpt-4o-temp-0.5-1.csv):
There are 15 genCQs and 15 expertCQs, we calculate the similarity scores of all (15*15) pairs of (genCQs, expertCQQs)

#### Step 3: select the highest scores of cosine similarity for each genCQs

Results saves at [hci/highest_cos_results/best_expert_cq_4_each_gen_cq/](hci/highest_cos_results/best_expert_cq_4_each_gen_cq/)

#### Step 4: caluculate the precision

For each pair of (genCQs, expertCQs) with highest cos score, if the threshold is higher than 0.6, we consider the genCQs as a valid genCQs. 

Precision = TP/(TP+FP)

True positives (TP) is the number of valid genCQs and false positives (FP) is the number of invalid genCQs.

The final precision is the average precision of 10 rounds.


