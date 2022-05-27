import os

root = '../../databases/toy_database'
path = "../../databases/corpora/untarred/ru"
with open('selective_convert.sh', 'w') as output:
    output.write('#!/bin/sh' + '\n')
    for dir in os.listdir(root):
        if dir != '.DS_Store':
            for file in os.listdir(root + '/' + dir):
                if file != '.DS_Store':
                    with open(root + '/' + dir + '/' + file, 'r') as f:
                        f = f.readlines()
                        for line in f:
                            filename = line.split()[0]
                            output.write(f'ffmpeg -i "{path}/clips/{filename}.mp3" "{path}/wav/{filename}.wav" -n' + '\n')

# ffmpeg -i "../../databases/corpora/untarred/ru/clips/$file" "../../databases/corpora/untarred/ru/wav/${file%.*}.wav"