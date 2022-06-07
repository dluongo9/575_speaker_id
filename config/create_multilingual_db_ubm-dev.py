import os
import pandas as pd
import sys
import random
import copy
from collections import defaultdict

# PATHS = {'norm': ['train_world.lst'],
#          'dev': ['for_models.lst', 'for_scores.lst'],
#          'eval': ['for_models.lst', 'for_scores.lst']}


def main():
    # pandas display settings
    # pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # defaults
    num_impostor_clips_per_dev_model, num_impostor_clips_per_eval_model, num_enrollment_samples = 6, 15, 20
    ubm_data_duration, duration_threshold = 1, .5  # hours, seconds

    if len(sys.argv) > 1:
        ubm_data_duration = float(sys.argv[1])
    if len(sys.argv) > 2:
        num_impostor_clips_per_dev_model = int(sys.argv[2])
    if len(sys.argv) > 3:
        num_impostor_clips_per_eval_model = int(sys.argv[3])
    if len(sys.argv) > 4:
        num_enrollment_samples = int(sys.argv[4])
    if len(sys.argv) > 5:
        duration_threshold = float(sys.argv[5])

    # TODO: can we write all results to the same file?
    with open('../logs/db_hyperparameters.txt', 'w') as file:
        file.write(f'{ubm_data_duration} hour{"s" if ubm_data_duration != 1.0 else ""} of data for the UBM' + '\n')
        file.write(f'10 impostors with {num_impostor_clips_per_dev_model} samples each used for dev.' + '\n')
        file.write(f'4 impostors with {num_impostor_clips_per_eval_model} samples each used for evaluation.' + '\n')
        file.write(f'{num_enrollment_samples} true speaker samples used for enrollment models in both dev and eval'
                   + '\n')
        file.write(f'{num_impostor_clips_per_eval_model * 4} true speaker samples used for probes' + '\n')
        file.write(f'duration threshold: {duration_threshold} seconds' + '\n')

    # make unit conversions
    ubm_data_duration *= 3600.0  # convert hours to seconds
    make_lst(ubm_data_duration, num_impostor_clips_per_dev_model, num_impostor_clips_per_eval_model,
             num_enrollment_samples, duration_threshold)

    print('all .lst files written\n')


def make_lst(ubm_data_duration, num_impostor_clips_per_dev_model, num_impostor_clips_per_eval_model,
             num_enrollment_samples, duration_threshold):
    """
    :param ubm_data_duration: hours
    :param num_impostor_clips_per_dev_model: number of impostor clips per dev model
    :param num_impostor_clips_per_eval_model: number of impostor clips per eval model
    :param num_enrollment_samples: number of samples to create a model
    :param duration_threshold: seconds
    :return:
    """

    # russian
    if 'ubm-ru' not in os.listdir('../../databases'):
        os.mkdir('../../databases/ubm-ru')
        os.mkdir('../../databases/ubm-ru/norm')
        os.mkdir('../../databases/ubm-ru/dev')
        os.mkdir('../../databases/ubm-ru/eval')
    open('../../databases/ubm-ru/norm/train_world.lst', 'w').close()
    open('../../databases/ubm-ru/dev/for_models.lst', 'w').close()
    open('../../databases/ubm-ru/dev/for_scores.lst', 'w').close()
    open('../../databases/ubm-ru/eval/for_models.lst', 'w').close()
    open('../../databases/ubm-ru/eval/for_scores.lst', 'w').close()

    # tamil
    if 'ubm-ta' not in os.listdir('../../databases'):
        os.mkdir('../../databases/ubm-ta')
        os.mkdir('../../databases/ubm-ta/norm')
        os.mkdir('../../databases/ubm-ta/dev')
        os.mkdir('../../databases/ubm-ta/eval')

    open('../../databases/ubm-ta/norm/train_world.lst', 'w').close()
    open('../../databases/ubm-ta/dev/for_models.lst', 'w').close()
    open('../../databases/ubm-ta/dev/for_scores.lst', 'w').close()
    open('../../databases/ubm-ta/eval/for_models.lst', 'w').close()
    open('../../databases/ubm-ta/eval/for_scores.lst', 'w').close()

    validated_ru, validated_ta, validated_dv = preprocess_df()

    make_norm(validated_ru, validated_ta, ubm_data_duration, duration_threshold)

    make_dev(validated_ru, validated_ta, num_impostor_clips_per_dev_model, num_enrollment_samples)
    make_eval(validated_dv, num_impostor_clips_per_eval_model, num_enrollment_samples)

    # validate('ubm-ru')
    # validate('ubm-ta')


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


def whittle(df):
    """
    Remove samples from speakers who belong to more than one demographic group.
    Removed duplicates, NaNs, 'other' gender
    :param df: data frame to process
    :return: df without the multiplicitous speakers
    """
    # key = client_id, value = set of demog tuples
    df = df[df['duration'] >= 1.0]  # nothing less than 1 second
    df = df[df['gender'] != 'other']  # drop 'other' gender
    for age in ['sixties', 'seventies', 'eighties']:
        df = df[df['age'] != age]  # drop each age

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
    validated_ru = whittle(validated_ru)
    validated_ru.reset_index(drop=True, inplace=True)

    # validated_ta.sort_values(by=['duration'], ascending=False)
    validated_ta.drop(columns=['sentence', 'up_votes', 'down_votes', 'accents', 'locale', 'segment'], inplace=True)
    validated_ta.dropna(axis='index', how='any', inplace=True)
    validated_ta = whittle(validated_ta)
    validated_ta.reset_index(drop=True, inplace=True)

    # validated_dv.sort_values(by=['duration'], ascending=False)
    validated_dv.drop(columns=['sentence', 'up_votes', 'down_votes', 'accents', 'locale', 'segment'], inplace=True)
    validated_dv.dropna(axis='index', how='any', inplace=True)
    validated_dv = whittle(validated_dv)
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


def make_norm(validated_ru, validated_ta, ubm_data_duration, duration_threshold):
    print('making norm .lst files\n')
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

    ubm_ru_norm, ubm_ta_norm = [], []

    # Fill UBMs with samples
    print('filling ubm:')
    while primary_list_metrics['duration'] <= ubm_data_duration:
        print('ubm total (hours):', primary_list_metrics['duration'] / 3600.0, sep='\t')
        sample_idx, mirror_sample_idx = find_next_candidates(primary_list_metrics,
                                                             validated_ru, validated_ta,
                                                             duration_threshold)
        primary_sample = validated_ru.loc[[sample_idx]]
        mirror_sample = validated_ta.loc[[mirror_sample_idx]]

        # update metrics in dictionaries
        primary_list_metrics['ages'][primary_sample['age'].values[0]] += 1
        primary_list_metrics['genders'][primary_sample['gender'].values[0]] += 1
        primary_list_metrics['duration'] += float(primary_sample['duration'].values[0])
        mirror_list_metrics['ages'][mirror_sample['age'].values[0]] += 1
        mirror_list_metrics['genders'][mirror_sample['gender'].values[0]] += 1
        mirror_list_metrics['duration'] += float(mirror_sample['duration'].values[0])

        # put strings in list to later write to .lst files
        ubm_ru_norm.append(validated_ru.loc[sample_idx, 'path'][:-4] + '\t' +
                           validated_ru.loc[sample_idx, 'client_id'])
        ubm_ta_norm.append(validated_ta.loc[mirror_sample_idx, 'path'][:-4] + '\t' +
                           validated_ta.loc[mirror_sample_idx, 'client_id'])

        # update data frames
        validated_ru.drop(labels=sample_idx, axis='index', inplace=True)
        validated_ta.drop(labels=mirror_sample_idx, axis='index', inplace=True)
    print('ubm full\n')

    with open('../logs/demographic_metrics.txt', 'w') as out:
        for demog in primary_list_metrics:
            out.write(f"{demog}:" + '\n')
            if demog != 'duration':
                for key in primary_list_metrics[demog]:
                    out.write(f'\t{key}:\t' + '\n')
                    out.write(f'\t\t{primary_list_metrics[demog][key]}' + '\n')
                    out.write(f'\t\t{mirror_list_metrics[demog][key]}' + '\n')
            else:
                out.write(f'\t{demog}:\t' + '\n')
                out.write(f'\t\t{primary_list_metrics[demog]}' + '\n')
                out.write(f'\t\t{mirror_list_metrics[demog]}' + '\n')

    write_to_lst('../../databases/ubm-ru/norm/train_world.lst', ubm_ru_norm)
    write_to_lst('../../databases/ubm-ta/norm/train_world.lst', ubm_ta_norm)
    print('norm .lst files written\n')


def make_dev(validated_ru, validated_ta, num_imp, num_enroll):
    print('making dev .lst files\n')
    dev_model_list_ru, dev_probe_list_ru = make_dev_lsts(validated_ru, num_imp, num_enroll)
    dev_model_list_ta, dev_probe_list_ta = make_dev_lsts(validated_ta, num_imp, num_enroll)

    # write to russian dev lists
    write_to_lst('../../databases/ubm-ru/dev/for_models.lst', dev_model_list_ru)
    write_to_lst('../../databases/ubm-ru/dev/for_scores.lst', dev_probe_list_ru)

    # write to tamil dev lists
    write_to_lst('../../databases/ubm-ta/dev/for_models.lst', dev_model_list_ta)
    write_to_lst('../../databases/ubm-ta/dev/for_scores.lst', dev_probe_list_ta)
    print('dev .lst files written\n')


def make_dev_lsts(df, num_imp_dev, num_enroll):
    """
    Take a data frame for a language and returns a list of data points for true speaker enrollment, true speaker probes,
    and imposter speaker probes.
    :param df: the input data frame
    :param num_imp_dev: number of dev impostors
    :param num_enroll:
    :return:
    """

    # num clips per unique speaker in each age range
    clips_per_demog_df = df.loc[(2.5 <= df['duration']) &
                                (df['duration'] <= 5.0)]

    # print('clips per demog df', clips_per_demog_df, sep='\n')

    clips_per_demog = dict()
    for i in clips_per_demog_df.index:
        age, gender = clips_per_demog_df.loc[i, 'age'], clips_per_demog_df.loc[i, 'gender']
        speaker = clips_per_demog_df.loc[i, 'client_id']
        if (age, gender) not in clips_per_demog:
            clips_per_demog[(age, gender)] = defaultdict(int)
            clips_per_demog[(age, gender)][speaker] += 1
        else:
            clips_per_demog[(age, gender)][speaker] += 1
    # print('clips per demog dict (just keys):', clips_per_demog.keys(), sep='\n')

    samples = [sorted(clips_per_demog[key].items(),
                      key=lambda x: x[1],
                      reverse=True)[:2] for key in clips_per_demog]  # top 2 speakers by number of clips
    # print('samples:')
    # [print(sample[0], sample[1], sep='\n', end='\n\n') for sample in samples]

    dev_model_samples, dev_true_probe_samples, dev_imp_samples = [], [], []
    for demog in samples:
        # extract each speaker's speaker ID.
        dev_model_sp, dev_imp_sp = demog[0][0], demog[1][0]
        # print(eval_model_sp)

        # get dev_imp_samples
        dev_imp_samples_df = clips_per_demog_df[clips_per_demog_df['client_id'] == dev_imp_sp].sort_values(
            by=['duration'],
            ascending=False)

        for i in dev_imp_samples_df.index[-num_imp_dev:]:
            path = dev_imp_samples_df.loc[i, 'path']
            dev_imp_samples.append((path[:-4],  # filename
                                    dev_imp_samples_df.loc[i, 'client_id'],  # model_id
                                    dev_imp_samples_df.loc[i, 'client_id'],  # claimed_client_id
                                    dev_imp_samples_df.loc[i, 'client_id']))  # client_id
            df = df[df['path'] != path]

        # get dev model samples and dev probe samples
        dev_model_samples_df = clips_per_demog_df[clips_per_demog_df['client_id'] == dev_model_sp].sort_values(
            by=['duration'],
            ascending=False)
        # print(dev_model_samples_df)
        # [print(i) for i in dev_model_samples_df.index[:10]]

        for i in dev_model_samples_df.index[:num_enroll]:
            path = dev_model_samples_df.loc[i, 'path']
            dev_model_samples += [(path[:-4],  # filename
                                   dev_model_samples_df.loc[i, 'client_id'],  # model_id
                                   dev_model_samples_df.loc[i, 'client_id'])]  # client_id
            df = df[df['path'] != path]

        for i in dev_model_samples_df.index[-(num_imp_dev * 10):]:  # 10 demographic groups
            path = dev_model_samples_df.loc[i, 'path']
            dev_true_probe_samples += [(path[:-4],  # filename
                                        dev_model_samples_df.loc[i, 'client_id'],  # model_id
                                        dev_model_samples_df.loc[i, 'client_id'],  # claimed_client_id
                                        dev_model_samples_df.loc[i, 'client_id'])]  # client_id
            df = df[df['path'] != path]

        # [print(sample) for sample in dev_model_samples]
    dev_model_set = set([sample[1] for sample in dev_model_samples])
    # print(dev_model_set)

    dev_probe_list = []
    for model in dev_model_set:
        # put dev impostor with claimed client Id of model into dev_imposter list
        dev_probe_list += ['\t'.join((sample[0], model, model, sample[3])) for sample in dev_imp_samples]

    # print("dev probe list len after impostors added:", len(dev_probe_list))

    dev_probe_list += ['\t'.join(sample) for sample in dev_true_probe_samples]
    dev_model_list = ['\t'.join(sample) for sample in dev_model_samples]

    # print('dev imp samples:', len(dev_imp_samples))
    # print('dev true samples:', len(dev_true_probe_samples))
    # print('dev probe list:', len(dev_probe_list))
    # print('dev model list:', len(dev_model_list))
    # print()

    return dev_model_list, dev_probe_list


def make_eval(validated_dv, num_imp_eval, num_enroll):
    print('making eval .lst files\n')
    # per demographic intersection, per speaker, number of clips > 3 seconds
    # outer keys: 4 demog, inner keys each: unique speaker, values: # clips
    clips_per_speaker = {('twenties', 'female'): defaultdict(int),
                         ('twenties', 'male'): defaultdict(int),
                         ('thirties', 'female'): defaultdict(int),
                         ('thirties', 'male'): defaultdict(int)}
    clips_per_speaker_df = validated_dv.loc[(validated_dv['age'] == 'twenties') |
                                            (validated_dv['age'] == 'thirties')]
    clips_per_speaker_df = clips_per_speaker_df.loc[(2.5 <= clips_per_speaker_df['duration']) &
                                                    (clips_per_speaker_df['duration'] <= 5.0)]
    for i in clips_per_speaker_df.index:
        age, gender = clips_per_speaker_df.loc[i, 'age'], clips_per_speaker_df.loc[i, 'gender']
        speaker = clips_per_speaker_df.loc[i, 'client_id']
        clips_per_speaker[(age, gender)][speaker] += 1
    # print(clips_per_speaker_df)
    # print('clips per speaker dict:', clips_per_speaker, sep='\n')
    dv_samples = [sorted(clips_per_speaker[key].items(),
                         key=lambda x: x[1],
                         reverse=True)[:2] for key in clips_per_speaker]  # top 2 speakers by number of clips
    # print('dv_samples:', dv_samples, sep='\n')

    eval_imp_samples, eval_model_samples, eval_true_probe_samples = [], [], []

    for demog in dv_samples:
        # extract each speaker's speaker ID.
        eval_model_sp, eval_imp_sp = demog[0][0], demog[1][0]
        # print(eval_model_sp)

        # get eval_imp samples
        eval_imp_samples_df = clips_per_speaker_df[clips_per_speaker_df['client_id'] == eval_imp_sp].sort_values(
            by=['duration'],
            ascending=False)
        eval_imp_samples += [(eval_imp_samples_df.loc[i, 'path'][:-4],  # filename
                              eval_imp_samples_df.loc[i, 'client_id'],  # model_id
                              eval_imp_samples_df.loc[i, 'client_id'],  # claimed_client_id
                              eval_imp_samples_df.loc[i, 'client_id'])  # client_id
                             for i in eval_imp_samples_df.index[-num_imp_eval:]]

        # get eval model samples
        eval_model_samples_df = clips_per_speaker_df[clips_per_speaker_df['client_id'] == eval_model_sp].sort_values(
            by=['duration'],
            ascending=False)
        # [print(sample) for sample in dev_model_samples]
        eval_model_samples += [(eval_model_samples_df.loc[i, 'path'][:-4],  # filename
                                eval_model_samples_df.loc[i, 'client_id'],  # model_id
                                eval_model_samples_df.loc[i, 'client_id'])  # client_id
                               for i in eval_model_samples_df.index[:num_enroll]]
        eval_true_probe_samples += [(eval_model_samples_df.loc[i, 'path'][:-4],  # filename
                                     eval_model_samples_df.loc[i, 'client_id'],  # model_id
                                     eval_model_samples_df.loc[i, 'client_id'],  # claimed_client_id
                                     eval_model_samples_df.loc[i, 'client_id'])  # client_id
                                    for i in eval_model_samples_df.index[-(num_imp_eval * 4):]]

    eval_model_set = set([sample[1] for sample in eval_model_samples])
    # print('eval model set:', eval_model_set, sep='\n')
    eval_true_probe_set = set([sample[1] for sample in eval_true_probe_samples])
    # print('eval true probe set:', eval_true_probe_set, sep='\n')
    eval_imp_set = set([sample[1] for sample in eval_imp_samples])
    # print('eval imp set:', eval_imp_set, sep='\n')

    eval_probe_list = []
    for model in eval_model_set:
        # put eval impostor with claimed client Id of model into eval_imposter list
        eval_probe_list += ['\t'.join((sample[0], model, model, sample[3])) for sample in eval_imp_samples]

    eval_probe_list += ['\t'.join(sample) for sample in eval_true_probe_samples]
    eval_model_list = ['\t'.join(sample) for sample in eval_model_samples]

    # print(f'eval imp samples (#={len(eval_imp_samples)}):', eval_imp_samples, sep='\n')

    # write to russian eval lists
    write_to_lst('../../databases/ubm-ru/eval/for_models.lst', eval_model_list)
    write_to_lst('../../databases/ubm-ru/eval/for_scores.lst', eval_probe_list)

    # write to tamil eval lists
    write_to_lst('../../databases/ubm-ta/eval/for_models.lst', eval_model_list)
    write_to_lst('../../databases/ubm-ta/eval/for_scores.lst', eval_probe_list)
    print('eval .lst files written\n')


def write_to_lst(path, lst):
    with open(path, 'w') as file:
        file.write('\n'.join(lst) + '\n')


def validate(ubm):
    print(f'validating {ubm[-2:]}:')
    dev_models = pd.read_csv(f'../../databases/{ubm}/dev/for_models.lst', sep='\t', header=None, low_memory=False,
                             names=['filename', 'model_id', 'client_id'])
    dev_probes = pd.read_csv(f'../../databases/{ubm}/dev/for_scores.lst', sep='\t', header=None, low_memory=False,
                             names=['filename', 'model_id', 'claimed_client_id', 'client_id'])
    eval_models = pd.read_csv(f'../../databases/{ubm}/eval/for_models.lst', sep='\t', header=None, low_memory=False,
                              names=['filename', 'model_id', 'client_id'])
    eval_probes = pd.read_csv(f'../../databases/{ubm}/eval/for_scores.lst', sep='\t',header=None, low_memory=False,
                              names=['filename', 'model_id', 'claimed_client_id', 'client_id'])

    dev_model_dict = dict()
    # 10 speaker models with 20 samples each
    for i in dev_models.index:
        client_id, model_id = dev_models.loc[i, 'client_id'], dev_models.loc[i, 'model_id']
        if model_id not in dev_model_dict:
            dev_model_dict[model_id] = defaultdict(int)
            dev_model_dict[model_id][client_id] += 1
        else:
            dev_model_dict[model_id][client_id] += 1
    print('\ndev models:', dev_model_dict, sep='\n')

    dev_probes_dict = dict()
    for i in dev_probes.index:
        client_id, claim = dev_probes.loc[i, 'client_id'], dev_probes.loc[i, 'claimed_client_id']
        if client_id not in dev_probes_dict:
            dev_probes_dict[client_id] = defaultdict(int)
            dev_probes_dict[client_id][claim] += 1
        else:
            dev_probes_dict[client_id][claim] += 1
    print('\ndev probes:', dev_probes_dict, sep='\n')

    # check that model ids and dev probe
    # print(f'\ndev probes and models disjoint? '
    #       f'intersection={len(dev_model_dict.keys() & dev_probes_dict.keys())} and '
    #       f'sum={len(dev_model_dict.keys()) + len(dev_probes_dict.keys())}')

    eval_model_dict = dict()
    for i in eval_models.index:
        client_id, model_id = eval_models.loc[i, 'client_id'], eval_models.loc[i, 'model_id']
        if model_id not in eval_model_dict:
            eval_model_dict[model_id] = defaultdict(int)
            eval_model_dict[model_id][client_id] += 1
        else:
            eval_model_dict[model_id][client_id] += 1
    print('\neval models:', eval_model_dict, sep='\n')

    eval_probes_dict = dict()
    for i in eval_probes.index:
        client_id, claim = eval_probes.loc[i, 'client_id'], eval_probes.loc[i, 'claimed_client_id']
        if client_id not in eval_probes_dict:
            eval_probes_dict[client_id] = defaultdict(int)
            eval_probes_dict[client_id][claim] += 1
        else:
            eval_probes_dict[client_id][claim] += 1
    print('\neval probes:', eval_probes_dict, sep='\n')


if __name__ == "__main__":
    main()
