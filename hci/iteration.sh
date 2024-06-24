# for param in 0 1 2 3 4 5 6 7 8 9
# do
#     python generate.py $param
# done

for param in 0 1 2 3 4 5 6 7 8 9
do
    python similarity.py gpt-output/rag-file-count-0/gpt-4o-temp-0.5-iteration-$param.txt ground-truth-cqs.txt $param
done

