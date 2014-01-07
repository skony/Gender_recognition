import wave
import os
from numpy.fft import rfft
import numpy as np
import pylab as pl
import scipy

class GenderRecognizer:
	def __init__(self, dir):
		self._dir = dir
		self._hits = 0

	def readData(self, name):
		self._realGender = name[4]
		wavFile = wave.open(self._dir + name, 'rb')
		width = wavFile.getsampwidth()
		fr = wavFile.getframerate()

		#fft should get only one channel
		step = wavFile.getnchannels() * 2
		frames = wavFile.getnframes()
		data = []
		tmp = wavFile.readframes(frames)
		for i in range(1,len(tmp),step):
			data.append((int.from_bytes(tmp[i:i+width], byteorder='big', signed=True)))
		wavFile.close()
		return data, fr

	def recognize(self, data, fr):
		a = np.abs(rfft(data, n=int(fr/2-20)))
		#pl.plot(a)
		x = a[85:180]
		x[np.argmax(x)] = 0
		y = a[165:255]
		y[np.argmax(y)] = 0
		gender = 'M' if (np.average(x) > np.average(y)) else 'K'
		if (gender == self._realGender):
			self._hits += 1
		self._realGender = gender

	def run(self):
		n = 0
		for name in os.listdir(self._dir):
		#for name in ['002_M.wav']:
			n += 1
			data, fr = self.readData(name)
			self.recognize(data, fr)
			print(name + ' ' + self._realGender)
		print(self._hits / n)
		#pl.show()

if __name__ == '__main__':
	gr = GenderRecognizer('wav/')
	gr.run()