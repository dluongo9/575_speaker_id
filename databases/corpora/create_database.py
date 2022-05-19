import os
import pandas as pd


IGNORE_FILES = ['.DS_Store']
LANGS = {'russian': 'ru',
         'tamil': 'ta',
         'dhivehi': 'dv'}
PATHS = {'norm': ['train_world.lst'],
         'dev': ['for_models.lst', 'for_probes.lst'],
         'eval': ['for_models.lst', 'for_probes.lst']}


def make_lst():
  for lang in LANGS:
      if lang == 'russian':  # TODO take out
          dir = os.path.join('untarred', lang, LANG_CODES[lang])

          validated = pd.read_csv(os.path.join(dir, 'validated.tsv'), sep='\t', header=0)
          print(len(validated['client_id'].unique()), f'voices in {lang}')
          with open('../toy_database/norm/train_world.lst', 'w') as file:  # TODO update in-line with folder/file from FOLDERS
              for i in range(len(validated['path'])):
                  path, client_id = validated['path'][i][:-4], validated['client_id'][i]
                  file.write(path + ' ' + client_id + '\n')
