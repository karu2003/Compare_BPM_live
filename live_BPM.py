import sys
import librosa
import librosa.display
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from estimate_bpm import BPM_Analyzer

class Audio_plots:
    def __init__(self):
        plt.ion()
        fig, ax = plt.subplots(2)
        x = np.arange(1250)
        y = np.random.randn(1250)

        # Plot 0 is for correlation librosa
        self.axi = ax[0]
        self.li, = ax[0].plot(x, y)
        ax[0].set_xlim(0,512)
        ax[0].set_ylim(0,1)
        ax[0].set_title("Correlation Librosa")
        # Plot 1 is for the correlation WDT
        self.li2, = ax[1].plot(x, y)
        ax[1].set_xlim(0,1250)
        ax[1].set_ylim(0,32768)
        ax[1].set_title("Correlation WDT")

        plt.tight_layout()

    def normalize(self,audio_data):
        amp = 32767/np.abs(np.max(audio_data.flatten()))
        audio_data_norm = [audio_data[i] * amp for i, k in enumerate(audio_data)] 
        return audio_data_norm

    def plot_correlation1(self, onset_env, sr):
        hop_length = 512
        ac = librosa.autocorrelate(onset_env, 2 * sr // hop_length)
        freqs = librosa.tempo_frequencies(len(ac), sr=sr, hop_length=hop_length)
        self.li.set_xdata(freqs[1:])
        self.li.set_ydata(librosa.util.normalize(ac)[1:])
        plt.pause(0.001)

    def plot_correlation2(self, data):
        data_norm = self.normalize(data)
        self.li2.set_xdata(np.arange(len(data_norm)))
        self.li2.set_ydata(data_norm)
        plt.pause(0.001)

def main():
    fs = 44100      # Sample rate
    seconds = 1.5    # Duration of recording
    audio_input = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()       # Wait until recording is finished

    onset_env = librosa.onset.onset_strength(audio_input.flatten(), sr=fs)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=fs)
    audio.plot_correlation1(onset_env,fs)

    correlation, bpm = bpms.computeWindowBPM(audio_input.flatten(),fs)
    audio.plot_correlation2(correlation)
    print('{0:<20} {1:<14}'.format(str(bpm),str(tempo)) )

if __name__ == "__main__":
    audio = Audio_plots()
    bpms = BPM_Analyzer()
    # print(sd.query_devices())
    print('{0:<20} {1:<14}'.format('BPM wdt','BPM librosa') )
    while True:
        try:
            main()
        except KeyboardInterrupt:
            sys.exit('\nInterrupted by user')    