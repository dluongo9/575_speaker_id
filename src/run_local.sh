#!/bin/sh
echo create database
cd ../config
python create_multilingual_db_ubm-dev.py $@

echo selective convert ru + ta
python selective_convert.py

echo selective convert sh
./selective_convert.sh

echo verify experiment ru
cd ../src
verify.py ubm_ru_config.py

echo verify experiment ta
verify.py ubm_ta_config.py

echo collect results ru
collect_results.py -vv --directory ../output/ru/ --sort -o ../results/ru/collect_results_ru.txt

echo collect results ta
collect_results.py -vv --directory ../output/ta/ --sort -o ../results/ta/collect_results_ta.txt

echo evaluate ru
evaluate.py -d ../output/ru/output/ru/None/nonorm/scores-dev -e ../output/ru/output/ru/None/nonorm/scores-eval -D ../results/ru/DET-ru.pdf -c EER > ../results/ru/evaluate_results.txt

echo evaluate ta
evaluate.py -d ../output/ta/output/ta/None/nonorm/scores-dev -e ../output/ta/output/ta/None/nonorm/scores-eval -D ../results/ta/DET-ta.pdf -c EER > ../results/ta/evaluate_results.txt
