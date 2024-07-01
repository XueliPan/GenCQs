# from generate import main
from chatGenerate import main

temp = [0.5, 0.75, 1.0, 1.25, 1.5]
rag_file_count = [1,2,3,4,5]
iteration = [i for i in range(0,10)]
for i_count in rag_file_count:
    for i_temp in temp:
        for i_iteration in iteration:
            main(rag_file_count=i_count, 
                 tempterature=i_temp, 
                 iteration=i_iteration)

