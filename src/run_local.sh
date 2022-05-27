#!/bin/sh
echo create database
cd ../config
python create_database_legacy.py

echo selective convert py
python selective_convert.py

echo selective convert sh
./selective_convert.sh

echo verify experiment
cd ../src
verify.py experiment.py

echo collect results
collect_results.py -vv --directory ../output/test_exp --sort -o ../results/collect_results.txt

echo evaluate
evaluate.py -d ../output/test_exp/output/None/nonorm/scores-dev -e ../output/test_exp/output/None/nonorm/scores-eval -D ../results/DET.pdf
