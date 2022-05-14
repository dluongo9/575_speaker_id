import speaker_verification_toolkit.tools as svt
mfcc = svt.extract_mfcc("res/japanese_news.mp3", samplerate=16000, winlen=0.025, winstep=0.01)
print(mfcc)