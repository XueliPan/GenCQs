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

#### Analysis(hci)
