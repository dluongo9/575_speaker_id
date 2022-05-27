#!/bin/sh

lang=$1

echo $lang lengths
start="date +%s"
cd ../../databases/corpora/untarred/$lang/clips/
for file in *.mp3
do
  duration=$(ffprobe "$file" 2>&1 | awk '/Duration/ { print $2 }')
  echo -e "$duration\t$file"
  #echo -e "$file"
done > ../../../../../575_speaker_id/config/"$lang"_len.txt
end="date +%s"
runtime=$((end-start))
echo $lang runtime: $runtime

#echo ru lengths
#start="date +%s"
#cd ../../ru
#for file in *.mp3
#do
#  duration=$(ffprobe "$file" 2>&1 | awk '/Duration/ { print $2 }')
#  echo -e "$duration\t$file"
#  #echo -e "$file"
#done > ../../../../../575_speaker_id/config/ru_len.txt
#end="date +%s"
#runtime=$((end-start))
#echo ru runtime: $runtime
#
#echo ta lengths
#start="date +%s"
#cd ../../ta
#for file in *.mp3
#do
#  duration=$(ffprobe "$file" 2>&1 | awk '/Duration/ { print $2 }')
#  echo -e "$duration\t$file"
#  #echo -e "$file"
#done > ../../../../../575_speaker_id/config/ta_len.txt
#end="date +%s"
#runtime=$((end-start))
#echo ta runtime: $runtime
