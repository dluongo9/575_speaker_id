#!/bin/bash

# Usage: $0 lang_folder

cd $1
mkdir wav

cd clips
for file in *.mp3
do
	ffmpeg -i "$file" "../wav/${file%.*}.wav"
done
