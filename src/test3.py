import bob.bio.spear as spear
import bob.ap
import scipy.io.wavfile
import numpy as np
win_length_ms = 20 # The window length of the cepstral analysis in milliseconds
win_shift_ms = 10 # The window shift of the cepstral analysis in milliseconds
n_filters = 24 # The number of filter bands
n_ceps = 19 # The number of cepstral coefficients
f_min = 0. # The minimal frequency of the filter bank
f_max = 4000. # The maximal frequency of the filter bank
delta_win = 2 # The integer delta value used for computing the first and second order derivatives
pre_emphasis_coef = 1.0 # The coefficient used for the pre-emphasis
dct_norm = True # A factor by which the cepstral coefficients are multiplied
mel_scale = True # Tell whether cepstral features are extracted on a linear (LFCC) or Mel (MFCC) scale
rate, signal = scipy.io.wavfile.read("../res/japanese_news_mono.wav")
signal = np.mean(signal, axis=1)
#scipy.io.wavfile.write("../res/japanese_news_mono.wav", rate, signal)
c = bob.ap.Ceps(rate, win_length_ms, win_shift_ms, n_filters, n_ceps, f_min, f_max, delta_win, pre_emphasis_coef, mel_scale, dct_norm)
signal = np.cast['float'](signal) # vector should be in **float**
print(signal.shape)
mfcc = c(signal)
print(len(mfcc))
print(mfcc)
print(rate)

cepstral_feats = spear.extractor.Cepstral("res/japanese_news.mp3")
print(cepstral_feats)