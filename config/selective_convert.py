import os
import sys

root = f"../../databases"
ignore = ['.DS_Store']

filenames = []

for db in os.listdir(root):
    if db not in ignore and 'ubm-' in db:
        print('db', db)
        for dir in os.listdir(root + '/' + db):
            if dir not in ignore:
                print('dir', dir)
                for file in os.listdir(root + '/' + db + '/' + dir):
                    if file not in ignore:
                        with open(root + '/' + db + '/' + dir + '/' + file, 'r') as f:
                            f = f.readlines()
                            for line in f:
                                filenames.append(line.split()[0])

with open('selective_convert.sh', 'w') as output:
    output.write('#!/bin/sh' + '\n')
    for file in filenames:
        lang = file.split('_')[2]
        output.write(f'ffmpeg -i "../../databases/corpora/untarred/{lang}/clips/{file}.mp3" "../../databases/corpora/untarred/wav/{file}.wav" -n' + '\n')

# ffmpeg -i "../../databases/corpora/untarred/ru/clips/$file" "../../databases/corpora/untarred/ru/wav/${file%.*}.wav"
