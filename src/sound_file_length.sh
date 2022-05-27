#!/bin/sh

cd ../../databases/corpora/untarred/ru/clips/
for file in *.mp3
do
  duration=$(ffprobe "$file" 2>&1 | awk '/Duration/ { print $2 }')
  echo -e "$duration\t$file"
  #echo -e "$file"
done > ../../../../../575_speaker_id/config/ru_len.txt

cd ../../ta
for file in *.mp3
do
  duration=$(ffprobe "$file" 2>&1 | awk '/Duration/ { print $2 }')
  echo -e "$duration\t$file"
  #echo -e "$file"
done > ../../../../../575_speaker_id/config/ta_len.txt

cd ../../dv
for file in *.mp3
do
  duration=$(ffprobe "$file" 2>&1 | awk '/Duration/ { print $2 }')
  echo -e "$duration\t$file"
  #echo -e "$file"
done > ../../../../../575_speaker_id/config/dv_len.txt
