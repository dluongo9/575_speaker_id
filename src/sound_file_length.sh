#!/bin/sh

for file in ../../databases/corpora/untarred/ru/clips/*.mp3
do
  duration=$(ffprobe "$file" 2>&1 | awk '/Duration/ { print $2 }')
  echo -e "$duration\t$file"
  #echo -e "$file"
done
