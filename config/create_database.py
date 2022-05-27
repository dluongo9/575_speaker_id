import os
import pandas as pd
import sys


IGNORE_FILES = ['.DS_Store']
LANGS = ['ru', 'ta', 'dv']
PATHS = {'norm': ['train_world.lst'],
         'dev': ['for_models.lst', 'for_probes.lst'],
         'eval': ['for_models.lst', 'for_probes.lst']}


def main():
    make_lst()
    # create_database()


def make_lst():
    if 'toy_database' not in os.listdir('../../databases'):
        os.mkdir('../../databases/toy_database')
        os.mkdir('../../databases/toy_database/norm')
        os.mkdir('../../databases/toy_database/eval')
        os.mkdir('../../databases/toy_database/dev')
    for lang in LANGS:
        if lang == 'ru':  # TODO take out
            dir = os.path.join('../../databases/corpora/untarred', lang)
            validated = pd.read_csv(os.path.join(dir, 'validated.tsv'), sep='\t', header=0, low_memory=False)

            sorted = validated.sort_values(by=['client_id'])
            sorted.reset_index(drop=True, inplace=True)
            sorted.drop(columns=['sentence', 'up_votes', 'down_votes', 'accents', 'locale', 'segment'], inplace=True)
            # print(sorted)
            # [print(f'{col}:', sorted[col].value_counts(), sep='\n', end='\n\n\n') for col in sorted.columns]
            # speakers = dict()
            speaker_idx = dict(sorted['client_id'].value_counts())
            # print(speaker_idx)

            true_speaker = 'c77a5a202fd9ebf667e4e0253209dfba12a41e298ef6fadfbcab46df5343976a9e5a536eda641aae83dc890845eb7f53a5dfb4bc81cfe6418ff84c823aa80d00'
            true_speaker_files = sorted[sorted['client_id'] == true_speaker]
            true_speaker_files.reset_index(drop=True, inplace=True)
            true_speaker_dev_model = true_speaker_files[0:30]
            true_speaker_eval_model = true_speaker_files[30:60]
            true_speaker_eval_model.reset_index(drop=True, inplace=True)
            true_speaker_probes = true_speaker_files[60:62]
            true_speaker_probes.reset_index(drop=True, inplace=True)

            true_speaker_dev_probe = true_speaker_probes[0:1]
            true_speaker_eval_probe = true_speaker_probes[1:2]
            # print("true speaker eval probe:", true_speaker_eval_probe, sep='\n')
            true_speaker_eval_probe.reset_index(drop=True, inplace=True)
            # print(true_speaker_dev_model)
            # print(true_speaker_probes)

            impostor_speaker1 = '367647909a85ac462fd9a50478047cb29639ef175ceeb4f7af680066643613192176366edf5e5e43d91b022c0a9c10498376849a8b6e09c9e150f8850442a762'
            impostor_speaker2 = '198a312bd7727493644139df5843693a153a7c2afc3accd3b4512092907de1d8c791d348cee930468257d77c6cbe860c1725c64f0480cb764e1f8735a2d348c3'
            impostor_probe1_files = sorted[sorted['client_id'] == impostor_speaker1]
            impostor_probe1_files.reset_index(drop=True, inplace=True)
            impostor_probe2_files = sorted[sorted['client_id'] == impostor_speaker2]
            impostor_probe2_files.reset_index(drop=True, inplace=True)
            # print(impostor_probe_files)
            impostor_dev_probe1 = impostor_probe1_files[0:1]
            impostor_eval_probe1 = impostor_probe1_files[1:2]
            impostor_dev_probe2 = impostor_probe2_files[0:1]
            impostor_eval_probe2 = impostor_probe2_files[1:2]
            # print("impostor eval probe", impostor_eval_probe, sep='\n')
            impostor_eval_probe1.reset_index(drop=True, inplace=True)
            impostor_eval_probe2.reset_index(drop=True, inplace=True)
            ubm_speakers = sorted[sorted['client_id'] != impostor_speaker1]
            ubm_speakers = ubm_speakers[ubm_speakers['client_id'] != true_speaker]
            ubm_speakers.reset_index(drop=True, inplace=True)

            sample = ubm_speakers.sample(n=200, axis='index')
            sample.reset_index(drop=True, inplace=True)
            # print(sample)

            num_rows = len(validated['client_id'])
            print(f'{lang}: {len(validated["client_id"].unique())} voices, {num_rows} rows')

            # create empty .lst files or empty existing .lst files
            open('../../databases/toy_database/norm/train_world.lst', 'w').close()
            open('../../databases/toy_database/dev/for_models.lst', 'w').close()
            open('../../databases/toy_database/dev/for_probes.lst', 'w').close()
            open('../../databases/toy_database/eval/for_models.lst', 'w').close()
            open('../../databases/toy_database/eval/for_probes.lst', 'w').close()

            # create norm training
            with open('../../databases/toy_database/norm/train_world.lst', 'a') as file:
                for i in range(len(sample['client_id'])):
                    file.write(sample['path'][i][:-4] + '\t' +
                               sample['client_id'][i] + '\n')

            # create dev models
            with open('../../databases/toy_database/dev/for_models.lst', 'a') as file:
                for i in range(len(true_speaker_dev_model['client_id'])):
                    file.write(true_speaker_dev_model['path'][i][:-4] + '\t' +
                               true_speaker_dev_model['client_id'][i] + '\t' +
                               true_speaker_dev_model['client_id'][i] + '\n')

            # create dev probes
            with open('../../databases/toy_database/dev/for_probes.lst', 'a') as file:
                for i in range(len(true_speaker_dev_probe)):
                    file.write(true_speaker_dev_probe['path'][i][:-4] + '\t' +
                               true_speaker_dev_probe['client_id'][i] + '\n')
                for i in range(len(impostor_dev_probe1)):
                    file.write(impostor_dev_probe1['path'][i][:-4] + '\t' +
                               impostor_dev_probe1['client_id'][i] + '\n')
                for i in range(len(impostor_dev_probe2)):
                    file.write(impostor_dev_probe2['path'][i][:-4] + '\t' +
                               impostor_dev_probe2['client_id'][i] + '\n')

            # create eval models
            with open('../../databases/toy_database/eval/for_models.lst', 'a') as file:
                for i in range(len(true_speaker_eval_model)):
                    file.write(true_speaker_eval_model['path'][i][:-4] + '\t' +
                               true_speaker_eval_model['client_id'][i] + '\t' +
                               true_speaker_eval_model['client_id'][i] + '\n')

            # create eval probes
            with open('../../databases/toy_database/eval/for_probes.lst', 'a') as file:
                for i in range(len(true_speaker_eval_probe)):
                    # print("true speaker eval probe", true_speaker_eval_probe['client_id'][i], sep='\n')
                    file.write(true_speaker_eval_probe['path'][i][:-4] + '\t' +
                               true_speaker_eval_probe['client_id'][i] + '\n')
                for i in range(len(impostor_eval_probe1)):
                    # print("impostor eval probe", impostor_eval_probe['client_id'][i], sep='\n')
                    file.write(impostor_eval_probe1['path'][i][:-4] + '\t' +
                               impostor_eval_probe1['client_id'][i] + '\n')
                for i in range(len(impostor_eval_probe2)):
                    # print("impostor eval probe", impostor_eval_probe['client_id'][i], sep='\n')
                    file.write(impostor_eval_probe2['path'][i][:-4] + '\t' +
                               impostor_eval_probe2['client_id'][i] + '\n')


if __name__ == "__main__":
    main()
