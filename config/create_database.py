import os
import pickle

import pandas as pd
import bob.bio.base


IGNORE_FILES = ['.DS_Store']
LANGS = {'russian': 'ru',
         'tamil': 'ta',
         'dhivehi': 'dv'}
PATHS = {'norm': ['train_world.lst'],
         'dev': ['for_models.lst', 'for_probes.lst'],
         'eval': ['for_models.lst', 'for_probes.lst']}


def main():
    make_lst()
    # create_database()


def make_lst():
    for lang in LANGS:
        if lang == 'russian':  # TODO take out
            dir = os.path.join('../databases/corpora/untarred', lang, LANGS[lang])

            validated = pd.read_csv(os.path.join(dir, 'validated.tsv'), sep='\t', header=0)
            print(len(validated['client_id'].unique()), f'voices in {lang}')

            with open('../../databases/toy_database/norm/train_world.lst', 'w') as file:  # TODO update in-line with folder/file from FOLDERS
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


# def create_database():
#     db = bob.bio.base.database.FileListBioDatabase('../toy_database', 'toy')
#     print(db)
#     objects = db.objects()
#     with open('our_database_pickled', 'wb') as output:
#         pickle.dump(db, output)
#     print(objects)


if __name__ == "__main__":
    main()
