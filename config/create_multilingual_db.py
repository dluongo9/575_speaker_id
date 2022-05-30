import os
import pandas as pd
import sys
import random
import copy
from collections import defaultdict

# PATHS = {'norm': ['train_world.lst'],
#          'dev': ['for_models.lst', 'for_probes.lst'],
#          'eval': ['for_models.lst', 'for_probes.lst']}


def main():
    # pandas display settings
    # pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    ubm_data_duration, per_model_duration, duration_threshold = .1, 1.0, .5  # hours, minutes, seconds  # TODO update
    if len(sys.argv) > 1:
        ubm_data_duration = int(sys.argv[1])
    if len(sys.argv) > 2:
        per_model_duration = int(sys.argv[2])
    if len(sys.argv) > 3:
        duration_threshold = int(sys.argv[3])

    # make unit conversions
    ubm_data_duration *= 3600.0  # convert hours to seconds
    per_model_duration *= 60.0  # convert minutes to seconds
    make_lst(ubm_data_duration, per_model_duration, duration_threshold)


def make_lst(ubm_data_duration, per_model_duration, duration_threshold):
    """
    :param ubm_data_duration: hours
    :param per_model_duration: minutes
    :param duration_threshold: seconds
    :return:
    """

    # russian
    if 'ubm-ru' not in os.listdir('../../databases'):
        os.mkdir('../../databases/ubm-ru')
        os.mkdir('../../databases/ubm-ru/')
        os.mkdir('../../databases/ubm-ru/dev')
        os.mkdir('../../databases/ubm-ru/eval')
    open('../../databases/ubm-ru/norm/train_world.lst', 'w').close()
    open('../../databases/ubm-ru/dev/for_models.lst', 'w').close()
    open('../../databases/ubm-ru/dev/for_probes.lst', 'w').close()
    open('../../databases/ubm-ru/eval/for_models.lst', 'w').close()
    open('../../databases/ubm-ru/eval/for_probes.lst', 'w').close()

    # tamil
    if 'ubm-ta' not in os.listdir('../../databases'):
        os.mkdir('../../databases/ubm-ta')
        os.mkdir('../../databases/ubm-ta/norm')
        os.mkdir('../../databases/ubm-ta/dev')
        os.mkdir('../../databases/ubm-ta/eval')
    open('../../databases/ubm-ta/norm/train_world.lst', 'w').close()
    open('../../databases/ubm-ta/dev/for_models.lst', 'w').close()
    open('../../databases/ubm-ta/dev/for_probes.lst', 'w').close()
    open('../../databases/ubm-ta/eval/for_models.lst', 'w').close()
    open('../../databases/ubm-ta/eval/for_probes.lst', 'w').close()

    validated_ru, validated_ta, validated_dv = preprocess_df()

    ages = set(validated_ru['age'].unique()) & set(validated_ta['age'].unique())
    genders = {'male', 'female'}  # not other /: (we don't know what that means in this data)

    primary_list_metrics = dict()

    primary_list_metrics['ages'] = dict()
    for key in ages:
        primary_list_metrics['ages'][key] = 0

    primary_list_metrics['genders'] = dict()
    for key in genders:
        primary_list_metrics['genders'][key] = 0

    primary_list_metrics['duration'] = 0.0

    mirror_list_metrics = copy.deepcopy(primary_list_metrics)

    # ubm_ru_norm, ubm_ta_norm = [], []
    #
    # while primary_list_metrics['duration'] < ubm_data_duration:
    #     print('ubm total (hours):', primary_list_metrics['duration'] / 3600.0, sep='\t')
    #     sample_idx, mirror_sample_idx = find_next_candidates(primary_list_metrics,
    #                                                          validated_ru, validated_ta,
    #                                                          duration_threshold)
    #     primary_sample = validated_ru.loc[[sample_idx]]
    #     mirror_sample = validated_ta.loc[[mirror_sample_idx]]
    #
    #     # update metrics in dictionaries
    #     primary_list_metrics['ages'][primary_sample['age'].values[0]] += 1
    #     primary_list_metrics['genders'][primary_sample['gender'].values[0]] += 1
    #     primary_list_metrics['duration'] += float(primary_sample['duration'].values[0])
    #     mirror_list_metrics['ages'][mirror_sample['age'].values[0]] += 1
    #     mirror_list_metrics['genders'][mirror_sample['gender'].values[0]] += 1
    #     mirror_list_metrics['duration'] += float(mirror_sample['duration'].values[0])
    #
    #     # put strings in list to later write to .lst files
    #     ubm_ru_norm.append(validated_ru.loc[sample_idx, 'path'][:-4] + '\t' +
    #                        validated_ru.loc[sample_idx, 'client_id'])
    #     ubm_ta_norm.append(validated_ta.loc[mirror_sample_idx, 'path'][:-4] + '\t' +
    #                        validated_ta.loc[mirror_sample_idx, 'client_id'])
    #
    #     # update data frames
    #     validated_ru.drop(labels=sample_idx, axis='index', inplace=True)
    #     validated_ta.drop(labels=mirror_sample_idx, axis='index', inplace=True)
    #
    # print("\nPrimary list metrics:", primary_list_metrics, sep='\t')
    # print("Mirror list metrics:", mirror_list_metrics, '\n', sep='\t')
    #
    # write_to_lst('../../databases/ubm-ru/norm/train_world.lst', ubm_ru_norm)
    # write_to_lst('../../databases/ubm-ta/norm/train_world.lst', ubm_ta_norm)

    speakers, genders, ages, durations = [], [], [], []
    for speaker in validated_dv['client_id'].unique():
        speakers.append(speaker)
        genders.append(validated_dv[validated_dv['client_id'] == speaker]['gender'].values[0])
        ages.append(validated_dv[validated_dv['client_id'] == speaker]['age'].values[0])
        durations.append(sum(validated_dv[validated_dv['client_id'] == speaker]['duration']))
    sorted_dv = pd.DataFrame(list(zip(speakers, genders, ages, durations)),
                             columns=['client_id', 'gender', 'age', 'duration'])
    sorted_dv.sort_values(by=['duration'], inplace=True)
    sorted_dv.reset_index(drop=True, inplace=True)
    # print('sorted_dv (cumulative per speaker):\n', sorted_dv)
    # print('\n\nall rows sorted by duration per clip:\n', validated_dv.sort_values(by=['duration']))

    demog_duration = defaultdict(int)
    for i in sorted_dv.index:
        gender, age = sorted_dv.loc[i, 'gender'], sorted_dv.loc[i, 'age']
        demog_duration[(age, gender)] += sorted_dv.loc[i, 'duration']
    # print('demographics x duration:')
    # [print(f'{key}:\t{demog_duration[key]}') for key in demog_duration if 'twenties' in key or 'thirties' in key]

    # print(sorted_dv[sorted_dv['age'] == 'fourties']['gender'].value_counts())

    make_dv_samples(validated_dv)


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


def remove_duplicates(df):
    """
    Remove samples from speakers who belong to more than one demographic group.
    :param df: data frame to process
    :return: df without the time traveling or transitioning speaker
    """
    # key = client_id, value = set of demog tuples
    demogs = dict()
    for i in df.index:
        if df.loc[i, 'client_id'] not in demogs:
            demogs[df.loc[i, 'client_id']] = {(df.loc[i, 'age'], df.loc[i, 'gender'])}
        else:
            demogs[df.loc[i, 'client_id']].add((df.loc[i, 'age'], df.loc[i, 'gender']))
    for speaker in demogs:
        if len(demogs[speaker]) > 1:
            df = df[df['client_id'] != speaker]
    return df


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
    validated_ru = remove_duplicates(validated_ru)
    validated_ru.reset_index(drop=True, inplace=True)

    # validated_ta.sort_values(by=['duration'], ascending=False)
    validated_ta.drop(columns=['sentence', 'up_votes', 'down_votes', 'accents', 'locale', 'segment'], inplace=True)
    validated_ta.dropna(axis='index', how='any', inplace=True)
    validated_ta = remove_duplicates(validated_ta)
    validated_ta.reset_index(drop=True, inplace=True)

    # validated_dv.sort_values(by=['duration'], ascending=False)
    validated_dv.drop(columns=['sentence', 'up_votes', 'down_votes', 'accents', 'locale', 'segment'], inplace=True)
    validated_dv.dropna(axis='index', how='any', inplace=True)
    validated_dv = remove_duplicates(validated_dv)
    validated_dv.reset_index(drop=True, inplace=True)

    return validated_ru, validated_ta, validated_dv


def find_next_candidates(primary_list_metrics, validated_ru_df, validated_ta_df, duration_threshold):
    # age = min(primary_list_metrics['ages'], key=primary_list_metrics['ages'].get)
    ages = sorted(primary_list_metrics['ages'].items(), key=lambda x: x[1])
    # gender = min(primary_list_metrics['genders'], key=primary_list_metrics['genders'].get)
    genders = sorted(primary_list_metrics['genders'].items(), key=lambda x: x[1])
    for gender in genders:
        gender = gender[0]
        for age in ages:
            age = age[0]
            filtered_df = validated_ru_df.loc[(validated_ru_df['age'] == age) & (validated_ru_df['gender'] == gender)]
            # print('filtered_df:', filtered_df, sep='\n')

            for sample_idx in filtered_df.index:
                sample_candidate = filtered_df.loc[[sample_idx]]
                sample_dur = sample_candidate['duration'].values[0]
                min_dur, max_dur = sample_dur - duration_threshold, sample_dur + duration_threshold
                filtered_mirror_df = validated_ta_df.loc[(validated_ta_df['age'] == age) &
                                                         (validated_ta_df['gender'] == gender)]
                filtered_mirror_df = filtered_mirror_df.loc[(min_dur <= filtered_mirror_df['duration']) &
                                                            (filtered_mirror_df['duration'] <= max_dur)]

                if len(filtered_mirror_df.index) > 0:
                    mirror_sample_idx = random.choice(seq=filtered_mirror_df.index)
                    return sample_idx, mirror_sample_idx
    raise Exception("I couldn't find a matching sample in the primary and mirror lists that matched the criteria.")


def make_dv_samples(validated_dv):
    # per demographic intersection, per speaker, number of clips > 3 seconds
    # outer keys: 4 demog, inner keys each: unique speaker, values: # clips
    clips_per_speaker = {('twenties', 'female'): defaultdict(int),
                         ('twenties', 'male'): defaultdict(int),
                         ('thirties', 'female'): defaultdict(int),
                         ('thirties', 'male'): defaultdict(int)}
    clips_per_speaker_df = validated_dv.loc[(validated_dv['age'] == 'twenties') |
                                            (validated_dv['age'] == 'thirties')]
    clips_per_speaker_df = clips_per_speaker_df.loc[(2.5 <= clips_per_speaker_df['duration']) &
                                                    (clips_per_speaker_df['duration'] <= 4.5)]
    for i in clips_per_speaker_df.index:
        age, gender = clips_per_speaker_df.loc[i, 'age'], clips_per_speaker_df.loc[i, 'gender']
        speaker = clips_per_speaker_df.loc[i, 'client_id']
        clips_per_speaker[(age, gender)][speaker] += 1
    # print(clips_per_speaker_df)
    # print(clips_per_speaker)
    dv_samples = [sorted(clips_per_speaker[key].items(),
                         key=lambda x: x[1],
                         reverse=True)[:4] for key in clips_per_speaker]  # top 4 speakers by number of clips
    [print(line) for line in dv_samples]

    dev_imp_samples, eval_imp_samples = [], []
    dev_model_samples, dev_true_probe_samples = [], []
    eval_model_samples, eval_true_probe_samples = [], []

    for demog in dv_samples:
        dev_model_sp, eval_model_sp, dev_imp_sp, eval_imp_sp = demog[0][0], demog[1][0], demog[2][0], demog[3][0]
        #print(eval_model_sp)

        # get dev_imp_samples
        dev_imp_samples_df = clips_per_speaker_df[clips_per_speaker_df['client_id'] == dev_imp_sp].sort_values(
            by=['duration'],
            ascending=False)
        dev_imp_samples += [(dev_imp_samples_df.loc[i, 'path'][:-4],  # filename
                             dev_imp_samples_df.loc[i, 'client_id'],  # model_id
                             dev_imp_samples_df.loc[i, 'client_id'],  # claimed_client_id
                             dev_imp_samples_df.loc[i, 'client_id'])  # client_id
                            for i in dev_imp_samples_df.index[-15:]]

        # get eval_imp samples
        eval_imp_samples_df = clips_per_speaker_df[clips_per_speaker_df['client_id'] == eval_imp_sp].sort_values(
            by=['duration'],
            ascending=False)
        eval_imp_samples += [(eval_imp_samples_df.loc[i, 'path'][:-4],  # filename
                              eval_imp_samples_df.loc[i, 'client_id'],  # model_id
                              eval_imp_samples_df.loc[i, 'client_id'],  # claimed_client_id
                              eval_imp_samples_df.loc[i, 'client_id'])  # client_id
                             for i in eval_imp_samples_df.index[-15:]]

        # get dev model samples and dev probe samples
        dev_model_samples_df = clips_per_speaker_df[clips_per_speaker_df['client_id'] == dev_model_sp].sort_values(
            by=['duration'],
            ascending=False)
        # print(dev_model_samples_df)
        # [print(i) for i in dev_model_samples_df.index[:10]]
        dev_model_samples += [(dev_model_samples_df.loc[i, 'path'][:-4],  # filename
                               dev_model_samples_df.loc[i, 'client_id'],  # model_id
                               dev_model_samples_df.loc[i, 'client_id'])  # client_id
                              for i in dev_model_samples_df.index[:20]]
        dev_true_probe_samples += [(dev_model_samples_df.loc[i, 'path'][:-4],  # filename
                                    dev_model_samples_df.loc[i, 'client_id'],  # model_id
                                    dev_model_samples_df.loc[i, 'client_id'],  # claimed_client_id
                                    dev_model_samples_df.loc[i, 'client_id'])  # client_id
                                   for i in dev_model_samples_df.index[-15:]]

        # get eval model samples
        eval_model_samples_df = clips_per_speaker_df[clips_per_speaker_df['client_id'] == eval_model_sp].sort_values(
            by=['duration'],
            ascending=False)
        # [print(sample) for sample in dev_model_samples]
        eval_model_samples += [(eval_model_samples_df.loc[i, 'path'][:-4],  # filename
                                eval_model_samples_df.loc[i, 'client_id'],  # model_id
                                eval_model_samples_df.loc[i, 'client_id'])  # client_id
                               for i in eval_model_samples_df.index[:20]]
        eval_true_probe_samples += [(eval_model_samples_df.loc[i, 'path'][:-4],  # filename
                                     eval_model_samples_df.loc[i, 'client_id'],  # model_id
                                     eval_model_samples_df.loc[i, 'client_id'],  # claimed_client_id
                                     eval_model_samples_df.loc[i, 'client_id'])  # client_id
                                    for i in eval_model_samples_df.index[-15:]]

    dev_model_set = set([sample[1] for sample in dev_model_samples])
    eval_model_set = set([sample[1] for sample in eval_model_samples])
    print(dev_model_set)
    print(eval_model_set)

    # print(dev_imp_samples, len(dev_imp_samples), sep="\n", end='\n\n\n')
    # print(eval_imp_samples, len(eval_imp_samples), sep="\n")

    # # write to russian dev and eval lists
    # write_to_lst('../../databases/ubm-ru/dev/for_models.lst', dev_model_samples)
    # write_to_lst('../../databases/ubm-ru/dev/for_probes.lst')
    # write_to_lst('../../databases/ubm-ru/eval/for_models.lst', eval_model_samples)
    # write_to_lst('../../databases/ubm-ru/eval/for_probes.lst')
    #
    # # write to tamil dev and eval lists
    # write_to_lst('../../databases/ubm-ta/dev/for_models.lst', dev_model_samples)
    # write_to_lst('../../databases/ubm-ta/dev/for_probes.lst')
    # write_to_lst('../../databases/ubm-ta/eval/for_models.lst', eval_model_samples)
    # write_to_lst('../../databases/ubm-ta/eval/for_probes.lst')


def write_to_lst(path, lst):
    with open(path, 'w') as file:
        file.write('\n'.join(lst))


if __name__ == "__main__":
    main()
