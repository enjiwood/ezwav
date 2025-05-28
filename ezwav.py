from scipy.io import wavfile
import wave
import numpy as np
import matplotlib.pyplot as plt

class WAV:
    wav : str = None
    samplerate : int = None
    data : np.ndarray = None
    time : np.ndarray = None
    volumes : list = None

    def __init__(self, file):
        try:
            self.wav = file
            self.samplerate, self.data = wavfile.read(self.wav)
            self.time = np.linspace(0., self.data.shape[0] / self.samplerate, self.data.shape[0])
        except Exception as e:
            raise Exception(f'There was an error initializing the WAV object: {e}')
    
    def __volnorm(self):
        dataleft = self.data[:, 0]
        dataright = self.data[:, 1]
        np.multiply(dataleft, 100 / np.max(np.abs(dataleft)), out=dataleft, casting='unsafe')
        np.multiply(dataright, 100 / np.max(np.abs(dataright)), out=dataright, casting='unsafe')
        return np.abs(dataleft), np.abs(dataright)

    def plot(self):
        plt.plot(self.time, self.data[:, 0], label="Left channel")
        plt.plot(self.time, self.data[:, 1], label="Right channel")
        plt.legend('')
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()
    
    def initvolumelist(self):
        seconds = int(max(self.time))

        left, right = self.__volnorm()

        volumes = [0] * seconds
        for i in range(seconds):
            data_idx = i * self.samplerate
            vol = max(left[data_idx], right[data_idx])
            volumes[i] = int(vol)

        self.volumes = volumes
    
    def getvolumelist(self):
        return self.volumes