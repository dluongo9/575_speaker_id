from pydub import AudioSegment
import sys, os, ffmpeg
sys.path.append('../../../../../ffmpeg')
print(os.listdir(('../../../../../ffmpeg')))
#print(os.environ['PATH'])
input_directory = sys.argv[1]
output_directory = sys.argv[2]
for file in os.listdir(input_directory):
    print(os.path.join(input_directory, file))
    sound = AudioSegment.from_mp3(os.path.join(input_directory, file))
    file = file[:-3]
    sound.export(os.path.join(output_directory, file + "wav"), format="wav")
