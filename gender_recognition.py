#from __future__ import division
#from matplotlib import pylab as plt
import numpy as np
import scipy.io.wavfile as sc
from scipy.signal import kaiser, decimate
from copy import copy
import os, re

countrights = 0

def genderRecognition(filename):
  global countrights
  try:
    rate, signal = sc.read(filename)
  except:
    print("")
  else:
    frames = len(signal)
    dur = float(frames) / rate
    if not isinstance(signal[0], np.int16):
      signal = [s[0] for s in signal]
    try:
      signal = signal * kaiser(frames, 30)
    except:
      print("")
    else:
      
      signal1 = abs(np.fft.rfft(signal))#np.log(abs(np.fft.rfft(signal)))
      signal2 = copy(signal1)
      
      for h in np.arange(2, 6):
        decsignal = decimate(signal1, h)
        signal2[:len(decsignal)] += decsignal
      
      speak = 50 * dur
      peak = np.argmax(signal2[speak:])
      freq = (speak + peak) / dur

      if freq < 180:
        result = 'M'
      elif 180 <= freq:
        result = 'K'

      truth = re.search('([KM])\.wav', filename).group(1)

      if truth == result:
        countrights += 1


files = os.listdir('train')
for name in files:
  genderRecognition('train/' + name)

accuracy = float(countrighs) / len(files)
print("Guessed " + str(countrights) + " out of "+ str(len(files)) + " correctly ("+str(accuracy * 100)+"%)")


