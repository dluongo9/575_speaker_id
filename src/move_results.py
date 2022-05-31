from datetime import datetime
import os
time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # 2022-05-30_22-34-02

os.mkdir(f'../all_results/{time}')

# move hyperparameters file
os.system(f'cp ../logs/db_hyperparameters.txt ../all_results/{time}/db_hyperparameters.txt')

# copy demographic metrics file
os.system(f'cp ../logs/demographic_metrics.txt ../all_results/{time}/demographic_metrics.txt')


# copy ru DET, evaluation and collect results files
os.system(f'cp ../results/ru/evaluate_results.txt ../all_results/{time}/ru-evaluate_results.txt')
os.system(f'cp ../results/ru/DET-ru.PDF ../all_results/{time}/DET-ru.pdf')
os.system(f'cp ../results/ru/collect_results_ru.txt ../all_results/{time}/ru-collect_results.txt')

# copy ta DET, evaluation and collect results files
os.system(f'cp ../results/ta/evaluate_results.txt ../all_results/{time}/ta-evaluate_results.txt')
os.system(f'cp ../results/ta/DET-ta.PDF ../all_results/{time}/DET-ta.pdf')
os.system(f'cp ../results/ta/collect_results_ta.txt ../all_results/{time}/ta-collect_results.txt')

# copy experiment.info files
os.system(f'cp ../output/ru/output/ru/None/Experiment.info ../all_results/{time}/ru-Experiment.info')
os.system(f'cp ../output/ta/output/ta/None/Experiment.info ../all_results/{time}/ta-Experiment.info')
