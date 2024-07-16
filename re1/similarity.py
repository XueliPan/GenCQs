import os
import sys
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util

def get_cqs(gen_cq_file, ground_truth_cq_file):
    """
    get_cqs: get competency questions list from txt file
    return: two lists
    """
    with open(ground_truth_cq_file, 'r') as f:
        expertCQs = [line.strip().split(',.,')[1] for line in f if len(line)>0]
    with open(gen_cq_file, 'r') as f:
        try:
            genCQs = [line.strip().split('. ')[1] for line in f if len(line)>0]
        except:
            print(f'###failed to import {gen_cq_file}')
        # print(f'genCQs: {genCQs}')
    return genCQs,expertCQs


def main(gen_cq_file, ground_truth_cq_file,rag_file_count, iteration, all_cos_results_file, bestcq_output_file):
    # if len(sys.argv) != 4:
    #     print("ERROR!! Usage: python similarity.py <gen_cq.txt> <ground_truth_cq.txt> <iteration>")
    #     sys.exit(1)
    # gen_cq_file = sys.argv[1]
    # ground_truth_cq_file = sys.argv[2]
    # iteration = sys.argv[3]

    # create output folders for intermediate and final results
    os.makedirs('all_cos_results', exist_ok=True)
    os.makedirs('highest_cos_results', exist_ok=True)
    os.makedirs('metric_results', exist_ok=True)


    genCQs, expertCQs= get_cqs(gen_cq_file, ground_truth_cq_file) 
    print(f"gen CQ: {genCQs[0]}")
    print(f"expert CQ: {expertCQs[0]}")

    # CQ embeddings  
    model = SentenceTransformer("all-MiniLM-L6-v2")
    genCQs_embeddings = model.encode(genCQs)
    expertCQs_embeddings = model.encode(expertCQs)

    # Compute cosine similarity between all pairs
    cos_sim = util.cos_sim(genCQs_embeddings, expertCQs_embeddings)

    # Add all pairs to a list with their cosine similarity score
    all_sentence_combinations = [] 
    for genCQs_idx in range(len(genCQs)):
        for expertCQs_idx in range(len(expertCQs)):
            all_sentence_combinations.append([cos_sim[genCQs_idx][expertCQs_idx], genCQs_idx, expertCQs_idx])

    # Sort list by the highest cosine similarity score
    all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)
    # print(all_sentence_combinations[0]) # element such as [tensor(0.8403), 1, 11]

    # print("Top-5 most similar pairs:")
    # for score, genCQs_idx, expertCQs_idx in all_sentence_combinations[0:5]:
    #     print("{} \t {} \t {:.4f}".format(genCQs[genCQs_idx], expertCQs[expertCQs_idx], cos_sim[genCQs_idx][expertCQs_idx]))

    # save cosine similarity score and the corresponding CQ pairs(n*m) to a csv file
    genCQ_ls = []
    expertCQ_ls = []
    score_ls = []
    n = len(all_sentence_combinations)
    for score, genCQs_idx, expertCQs_idx in all_sentence_combinations[0:n]:
        # print("{} \t {} \t {:.4f}".format(genCQs[genCQs_idx], expertCQs[expertCQs_idx], cos_sim[genCQs_idx][expertCQs_idx]))
        # print(f"{score.item():.4f}")
        # print(genCQs[genCQs_idx])
        # print(expertCQs[expertCQs_idx])
        genCQ_ls.append(genCQs[genCQs_idx])
        expertCQ_ls.append(expertCQs[expertCQs_idx])
        score_ls.append(f"{score.item():.4f}")
    cos_sim_df = pd.DataFrame()
    cos_sim_df['genCQ'] = genCQ_ls
    cos_sim_df['expertCQ'] = expertCQ_ls
    cos_sim_df['cos_score'] = score_ls

    output_folder = f'all_cos_results/rag-file-count-{rag_file_count}'
    os.makedirs(output_folder, exist_ok=True)
    output_file = f'{output_folder}/{all_cos_results_file}'
    cos_sim_df.to_csv(output_file)

    # calculate the highest cosine similarity for each genCQ or each expertCQ
    data = pd.read_csv(output_file)
    ###### for each expertCQ, find the most similar genCQ
    highest_score_expertCQs = pd.DataFrame()
    scores = []
    best_genCQs = []
    for i in expertCQs:
        # print(i)
        filtered_data = data[data['expertCQ'] == i]
        sorted_data = filtered_data.sort_values(by='cos_score', ascending=False)
        cos = list(sorted_data['cos_score'])[0]
        best_genCQ = list(sorted_data['genCQ'])[0]
        best_genCQs.append(best_genCQ)
        scores.append(cos)
        # print(best_genCQ, cos)
    highest_score_expertCQs['expertCQs'] = expertCQs
    highest_score_expertCQs['best_genCQs'] = best_genCQs
    highest_score_expertCQs['best_cos_score'] = scores
    relevant_best_genCQs = highest_score_expertCQs[highest_score_expertCQs['best_cos_score'] >= 0.6]
    precision_0 = len(relevant_best_genCQs)/len(genCQs)
    print(relevant_best_genCQs)
    if len(relevant_best_genCQs['best_genCQs']) != 0:
        recall_0 = len(set(relevant_best_genCQs['best_genCQs']))/len(relevant_best_genCQs['best_genCQs'])
    else:
        recall_0 = 0
    print(f'\nprecision for (expertCQ, best_genCQ): {len(relevant_best_genCQs)}/{len(genCQs)}={precision_0:0.4f}')
    print(f"recall for (expertCQ, best_genCQ): {len(set(relevant_best_genCQs['best_genCQs']))}/{len(relevant_best_genCQs['best_genCQs'])} = {recall_0:0.4f}")
    
    output_folder = f'highest_cos_results/best_gen_cq_4_each_expert_cq/rag-file-count-{rag_file_count}'
    os.makedirs(output_folder, exist_ok=True)
    output_file = f'{output_folder}/{bestcq_output_file}.csv'
    highest_score_expertCQs.to_csv(output_file)
    print('#############')

    ###### for each genCQ, find the most similar expertCQ
    highest_score_genCQs = pd.DataFrame()
    scores = []
    best_expertCQs = []
    for i in genCQs:
        # print(i)
        filtered_data = data[data['genCQ'] == i]
        sorted_data = filtered_data.sort_values(by='cos_score', ascending=False)
        cos = list(sorted_data['cos_score'])[0]
        best_expertCQ = list(sorted_data['expertCQ'])[0]
        best_expertCQs.append(best_expertCQ)
        scores.append(cos)
    highest_score_genCQs['genCQs'] = genCQs
    highest_score_genCQs['best_expertCQs'] = best_expertCQs
    highest_score_genCQs['best_cos_score'] = scores
    relevant_best_expertCQs = highest_score_genCQs[highest_score_genCQs['best_cos_score'] >= 0.6]
    precision_1 = len(relevant_best_expertCQs)/len(expertCQs)
    print(relevant_best_expertCQs)
    if len(relevant_best_expertCQs['best_expertCQs']) != 0:
        a = len(set(relevant_best_expertCQs.best_expertCQs))
        b = len(relevant_best_expertCQs.best_expertCQs)
        recall_1 = a/b
        print(f"recall for (genCQ, best_expertCQ): {a}/{b} = {recall_1:0.4f}")
    else:
        recall_1 = 0
    print(f"\nprecision for (genCQ, best_expertCQ): {len(relevant_best_expertCQs)}/{len(expertCQs)} = {precision_1:0.4f}")
    print(f"recall for (genCQ, best_expertCQ): {recall_1:0.4f}")
    
    output_folder = f'highest_cos_results/best_expert_cq_4_each_gen_cq/rag-file-count-{rag_file_count}'
    os.makedirs(output_folder, exist_ok=True)
    highest_score_genCQs.to_csv(output_file)
    return [precision_0, recall_0, precision_1, recall_1]

if __name__ == "__main__":
    main()

