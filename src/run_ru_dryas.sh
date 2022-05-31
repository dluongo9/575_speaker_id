#!/bin/sh
echo create database
cd ../config
python create_multilingual_db.py

echo verify experiment ru
cd ../src
verify.py ubm_ru_config.py

echo collect results ru
collect_results.py -vv --directory ../output/ru/ --sort -o ../results/ru/collect_results_ru.txt

echo evaluate ru
evaluate.py -d ../output/ru/output/ru/None/nonorm/scores-dev -e ../output/ru/output/ru/None/nonorm/scores-eval -D ../results/ru/DET-ru.pdf -c EER > ../results/ru/evaluate_results.txt

