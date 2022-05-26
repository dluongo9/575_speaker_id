import pandas as pd
import os


def main():
    results_dir = '../results/test_exp/output/None/nonorm'
    dev_scores = pd.read_csv(os.path.join(results_dir, 'scores-dev'), header=None, delim_whitespace=True)
    #print(dev_scores)
    sorted = dev_scores.sort_values(by=[2])
    #print(sorted)
    print(sorted[2].value_counts())

    eval_scores = pd.read_csv(os.path.join(results_dir, 'scores-eval'), header=None, delim_whitespace=True)
    sorted = eval_scores.sort_values(by=[2])
    # print(sorted)
    print(sorted[2].value_counts())


if __name__ == "__main__":
    main()