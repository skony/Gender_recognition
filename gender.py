import scipy.io.wavfile
import wave
import contextlib
from pylab import *
from numpy import *
from scipy import *

fname = "train/046_K.wav"
with contextlib.closing(wave.open(fname,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print(duration)	

w, signal = scipy.io.wavfile.read(fname)
signal = [s[0] for s in signal]   #Tylko pierwszy kanal

signal1 = fft(signal)
signal1 = abs(signal1)

print "SRUUU"

freqs = linspace(0, len(signal1)-1, len(signal1), endpoint=False)
subplot(212)
stem(freqs[0:1000], signal1[0:1000], '-*')
xlabel("frequency[Hz]")
ylabel("value")

print "GG"

subplot(211)
t = linspace(0, duration, len(signal), endpoint=False)
plot(t, signal)
xlabel("time[s]")
ylabel("value")

#stem(freqs[0:1000], signal1[0:1000], '-*')
#yscale('log')


show()
