import csv
import ast
from similarity import main

def write_list_to_file(filename, lst):
    with open(filename, 'w') as file:
        for item in lst:
            file.write(f"{item}\n")

def txt_to_csv(txt_filename, csv_filename):
    with open(txt_filename, 'r') as txt_file, open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        for line in txt_file:
            # Convert string representation of list to an actual list
            row = ast.literal_eval(line.strip())
            csv_writer.writerow(row)


temp = [0.5, 0.75, 1, 1.25, 1.5]
rag_file_count = [1,2,3,4,5,10]
iteration = [i for i in range(0,10)]

ground_truth_cq_file = 'ground-truth-cqs.txt'
gpt_model = 'gpt-4o'
for i_count in rag_file_count:
    metrics_temp = {}
    for i_temp in temp:
        metrics_each_temp = []
        for i_iteration in iteration:
            gen_cq_file = f'gpt-output/rag-file-count-{i_count}/gpt-4o-temp-{float(i_temp)}-iteration-{i_iteration}.txt'
            all_cos_result_file = f'{gpt_model}-temp-{i_temp}-{i_iteration}.csv'
            bestcq_output_file = f'gpt-4o-temp-{float(i_temp)}-iteration-{i_iteration}'
            metrics = main(gen_cq_file, ground_truth_cq_file, i_count, i_iteration, all_cos_result_file, bestcq_output_file)
            metrics_each_temp.append(metrics)
            
        print(f'metrics for temperature{float(i_temp)}:\n{metrics_each_temp}')
        file = f'metric_results/rag-file-count-{i_count}-gpt-4o-temp-{float(i_temp)}.txt'
        write_list_to_file(file, metrics_each_temp)
        metrics_temp[i_temp] = metrics_each_temp
    # print(metrics_temp)




        
        
            