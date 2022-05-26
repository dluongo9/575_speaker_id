import os

import pandas as pd


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

            validated = pd.read_csv(os.path.join(dir, 'validated.tsv'), sep='\t', header=0)
            num_rows = len(validated['client_id'])
            print(f'{lang}: {len(validated["client_id"].unique())} voices, {num_rows} rows')

            # TODO update in-line with our final breakdown of train vs. dev vs. eval
            with open('../../databases/toy_database/norm/train_world.lst', 'w') as file:
                writer = []
                for i in range(len(validated['path']))[:200]:  # slice to shorten
                    path, client_id = validated['path'][i][:-4], validated['client_id'][i]
                    writer.append(path + '\t' + client_id)
                file.write('\n'.join(writer))

            with open('../../databases/toy_database/dev/for_models.lst', 'w') as file:
                writer = []
                for i in range(len(validated['path']))[200:230]:
                    path, client_id = validated['path'][i][:-4], validated['client_id'][i]
                    writer.append(path + '\t' + client_id + '\t' + client_id)
                file.write('\n'.join(writer))

            with open('../../databases/toy_database/dev/for_probes.lst', 'w') as file:
                writer = []
                for i in range(len(validated['path']))[230:260]:
                    path, client_id = validated['path'][i][:-4], validated['client_id'][i]
                    writer.append(path + '\t' + client_id)
                file.write('\n'.join(writer))

            with open('../../databases/toy_database/eval/for_models.lst', 'w') as file:
                writer = []
                for i in range(len(validated['path']))[260:290]:
                    path, client_id = validated['path'][i][:-4], validated['client_id'][i]
                    writer.append(path + '\t' + client_id + '\t' + client_id)
                file.write('\n'.join(writer))
            with open('../../databases/toy_database/eval/for_probes.lst', 'w') as file:
                writer = []
                for i in range(len(validated['path']))[290:320]:
                    path, client_id = validated['path'][i][:-4], validated['client_id'][i]
                    writer.append(path + '\t' + client_id)
                file.write('\n'.join(writer))


if __name__ == "__main__":
    main()
