import os
import pandas as pd
import sys


IGNORE_FILES = ['.DS_Store']
LANGS = ['ru', 'ta', 'dv']
PATHS = {'norm': ['train_world.lst'],
         'dev': ['for_models.lst', 'for_probes.lst'],
         'eval': ['for_models.lst', 'for_probes.lst']}


def main():
    ubm_data_duration, per_model_duration, duration_threshold = 1, 1, 5
    if len(sys.argv) > 1:
        ubm_data_duration = int(sys.argv[1])
    if len(sys.argv) > 2:
        per_model_duration = int(sys.argv[2])
    if len(sys.argv) > 3:
        duration_threshold = int(sys.argv[3])
    make_lst(ubm_data_duration, per_model_duration, duration_threshold)
    # create_database()


def make_lst(ubm_data_duration, per_model_duration, duration_threshold):
    """
    :param ubm_data_duration: hours
    :param per_model_duration: minutes
    :param duration_threshold: seconds
    :return:
    """
    # pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # TODO defaultdict for counts of demographics for each high resource UBM

    # russian
    if 'ubm-ru' not in os.listdir('../../databases'):
        os.mkdir('../../databases/ubm-ru')
        os.mkdir('../../databases/ubm-ru/norm')
        os.mkdir('../../databases/ubm-ru/dev')
        os.mkdir('../../databases/ubm-ru/eval')

    # tamil
    if 'ubm-ta' not in os.listdir('../../databases'):
        os.mkdir('../../databases/ubm-ta')
        os.mkdir('../../databases/ubm-ta/norm')
        os.mkdir('../../databases/ubm-ta/dev')
        os.mkdir('../../databases/ubm-ta/eval')

    validated_ru, validated_ta, validated_dv = preprocess_df()

    ages = set(validated_ru['age'].unique()) & set(validated_ta['age'].unique())
    genders = {'male', 'female'}  # not other /:

    primary_list = []
    mirror_list = []
    primary_list_metrics = dict()

    primary_list_metrics['ages'] = dict()
    for key in ages:
        primary_list_metrics['ages'][key] = 0

    primary_list_metrics['genders'] = dict()
    for key in genders:
        primary_list_metrics['genders'][key] = 0

    primary_list_metrics['duration'] = 0

    mirror_list_metrics = dict(zip(primary_list_metrics.keys(), primary_list_metrics.values()))

    # while primary_list_metrics['duration'] < ubm_data_duration:
    # sample, mirror_sample = find_next_candidates(primary_list_metrics, mirror_list_metrics,
    #                                              validated_ru, validated_ta,
    #                                              duration_threshold)
    # TODO

    print("Primary list metrics:", primary_list_metrics, sep='\t')
    print("Mirror list metrics:", mirror_list_metrics, sep='\t')


def create_metrics_dict():
    pass


def preprocess_durations(lang):
    with open(f'{lang}_len.txt', 'r') as lens:
        lens = [line.strip().split() for line in lens.readlines() if len(line.strip().split()) > 1]

    durations, filenames = [], []
    for row in lens:
        # print(row)
        duration, filename = row
        duration = list(map(float, duration.strip(',').split(':')))
        duration[0] *= 3600
        duration[1] *= 60
        duration = sum(duration)
        durations.append(duration)
        filenames.append(filename)

    return pd.DataFrame(list(zip(durations, filenames)),
                        columns=['duration', 'path'])


def preprocess_df():
    dir_ru = '../../databases/corpora/untarred/ru'
    dir_ta = '../../databases/corpora/untarred/ta'
    dir_dv = '../../databases/corpora/untarred/dv'
    pre_validated_ru = pd.read_csv(os.path.join(dir_ru, 'validated.tsv'), sep='\t', header=0, low_memory=False)
    pre_validated_ta = pd.read_csv(os.path.join(dir_ta, 'validated.tsv'), sep='\t', header=0, low_memory=False)
    pre_validated_dv = pd.read_csv(os.path.join(dir_dv, 'validated.tsv'), sep='\t', header=0, low_memory=False)

    ru_duration_df = preprocess_durations('ru')
    ta_duration_df = preprocess_durations('ta')
    dv_duration_df = preprocess_durations('dv')

    validated_ru = pd.merge(pre_validated_ru, ru_duration_df, on='path', how='inner')
    validated_ta = pd.merge(pre_validated_ta, ta_duration_df, on='path', how='inner')
    validated_dv = pd.merge(pre_validated_dv, dv_duration_df, on='path', how='inner')

    # validated_ru.sort_values(by=['duration'], ascending=False)
    validated_ru.drop(columns=['sentence', 'up_votes', 'down_votes', 'accents', 'locale', 'segment'], inplace=True)
    validated_ru.dropna(axis='index', how='any', inplace=True)
    validated_ru.reset_index(drop=True, inplace=True)

    # validated_ta.sort_values(by=['duration'], ascending=False)
    validated_ta.drop(columns=['sentence', 'up_votes', 'down_votes', 'accents', 'locale', 'segment'], inplace=True)
    validated_ta.dropna(axis='index', how='any', inplace=True)
    validated_ta.reset_index(drop=True, inplace=True)

    # validated_dv.sort_values(by=['duration'], ascending=False)
    validated_dv.drop(columns=['sentence', 'up_votes', 'down_votes', 'accents', 'locale', 'segment'], inplace=True)
    validated_dv.dropna(axis='index', how='any', inplace=True)
    validated_dv.reset_index(drop=True, inplace=True)

    return validated_ru, validated_ta, validated_dv


def find_next_candidates(primary_list_metrics, mirror_list_metrics, validated_ru, validated_ta, duration_threshold):

    age = min(primary_list_metrics['age1'], primary_list_metrics['age2'])  # TODO include all age ranges here
    if primary_list_metrics['male'] < primary_list_metrics['female']:
        gender = 'male'
    else:
        gender = 'female'
    found = False
    sample_idx = 0
    while not found:
        sample = "TODO" # TODO pull sample with gender and age
        sample_dur = 0 # TODO get sample duration
        #if age, gender, sample_dur in validated_ta: # TODO see if equivalent datapoint in mirror set
            # found = True
            # mirror_sample = "TODO" # TODO pull mirror sample
        # else:
        #     sample_idx += 1
    return sample, mirror_sample


if __name__ == "__main__":
    main()
