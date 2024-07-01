### Generating Competency Question using LLMs

#### domains
- [Human Computer Interaction](hci/)
- [Requirement Engeneering](re/)

#### Code inside each domain
##### HCI
- [chatGenerate.py](hci/chatGenerate.py): generates CQs using just LLM prompting, output a list of generative CQs
- [RAGgenerate.py](hci/RAGgenerate.py): generates CQs using just RAG, output a list of generative CQs
- [generate-iteration.py](hci/generate-iteration.py): iteration of each parameter settings in chatGenerate.py or RAGgenerate.py
- [similarity.py](hci/similarity.py): similarity calculation between generative CQs and ground-truth CQs
- [similarity-iteration.py](hci/similarity.py): iteration of each parameter settings in similariy.py
- [plot.ipynb](hci/plot.ipynb): plots the evaluation metrics
##### RE
- [chatGenerate.py](re/chatGenerate.py): generates CQs using just LLM prompting, output a list of generative CQs
- [RAGgenerate.py](re/RAGgenerate.py): generates CQs using just RAG, output a list of generative CQs
- [generate-iteration.py](re/generate-iteration.py): iteration of each parameter settings in chatGenerate.py or RAGgenerate.py
- [similarity.py](re/similarity.py): similarity calculation between generative CQs and ground-truth CQs
- [similarity-iteration.py](re/similarity.py): iteration of each parameter settings in similariy.py
- [plot.ipynb](re/plot.ipynb): plots the evaluation metrics

#### Results

#### Analysis
