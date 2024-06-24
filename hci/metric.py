import csv
import ast

def txt_to_csv(txt_filename, csv_filename):
    with open(txt_filename, 'r') as txt_file, open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        for line in txt_file:
            # Convert string representation of list to an actual list
            row = ast.literal_eval(line.strip())
            csv_writer.writerow(row)

# Example usage
count = [0,1,2]
temp = [0.5, 0.75, 1.0, 1.25, 1.5]
for i in count:
    for j in temp:
        txt_to_csv(f"metric_results/rag-file-count-{i}-gpt-4o-temp-{j}.txt", f"rag-file-count-{i}-gpt-4o-temp-{j}.csv")
