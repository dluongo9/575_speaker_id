#!/bin/sh
echo create database
cd ../config
python create_multilingual_db.py

echo verify experiment ta
cd ../src
verify.py ubm_ta_config.py

echo collect results ta
collect_results.py -vv --directory ../output/ta/ --sort -o ../results/ta/collect_results_ta.txt

echo evaluate ta
evaluate.py -d ../output/ta/output/ta/None/nonorm/scores-dev -e ../output/ta/output/ta/None/nonorm/scores-eval -D ../results/ta/DET-ta.pdf -c EER > ../results/ta/evaluate_results.txt

