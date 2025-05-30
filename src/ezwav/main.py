from scipy.io import wavfile
import wave
import numpy as np
import matplotlib.pyplot as plt
from .utils import normalize, Time_Unit

class Wav:
    """
    A class for reading and analyzing WAV audio files.

    This class provides methods for loading a WAV file, accessing its data 
    (e.g. duration, sample rate), extracting amplitude and loudness data, 
    and plotting the waveform. It supports both mono and multichannel audio.

    Parameters
    ----------
    file : str
        Path to the WAV file to load.

    Attributes
    ----------
    file : str
        The file path of the loaded WAV file.
    samplerate : int
        The sample rate of the audio (samples per second).
    duration : float
        The duration of the audio in seconds.
    data : np.ndarray
        The raw audio data as a NumPy array.
    time : np.ndarray
        An array representing the time axis for the audio samples.
    amplitude_list : list
        A list of peak amplitudes sampled over time, based on channel maximums.
    audio_mode : str
        Describes the channel configuration: 'mono', 'stereo', or '{n}-channel'.

    Methods
    -------
    __len__()
        Returns the duration of the audio in seconds as an integer.
    plot()
        Plots the waveform of the audio file. If stereo, both channels are shown.
    init_amplitude_list(time_unit='', norm=True)
        Initializes a list of amplitude values over time. Can normalize values and
        specify resolution in seconds, milliseconds, or microseconds.
    """
    def __init__(self, file: str):
        try:
            self._file: str = file
            self._samplerate, self._data  = wavfile.read(self.file)
            self._time: np.ndarray = np.linspace(0., self.data.shape[0] / self.samplerate, self.data.shape[0])
            self._num_channels: int = self._data.ndim
            self._duration: float = float(max(self._time))
            self._amplitude_list: list = None
            #self._loudness_list: list = None       #TO-DO
            self._channels: list = self._split_channels()
        except Exception as e:
            raise Exception(f'There was an error initializing the Wav object: {e}')
    
    def __len__(self):
        return int(self._duration)
    
    def _split_channels(self, norm: bool=False, absolute: bool=False):
        """
        Splits the audio data into separate channels with optional normalization and absolute value conversion.

        This method processes the raw audio data (`self._data`) and stores each audio channel as a 
        separate array in `self._channels`. Mono audio is wrapped in a list to maintain a consistent structure.

        Parameters
        ----------
        norm : bool, optional
            If True, normalizes each channel using the `normalize` function to the range [0, 100]. Default is False.
        
        absolute : bool, optional
            If True, converts all channel sample values to their absolute values. This is applied 
            after normalization or copying. Default is False.

        Returns
        -------
        None
            The result is stored in the instance variable `self._channels`.

        Notes
        -----
        - For mono audio, a single array is wrapped in a list for consistency.
        - If `norm` is True, normalization occurs before absolute value conversion.
        - Normalization uses the full dynamic range of the individual channel.
        """
        if norm:
            if self._num_channels > 1:
                self._channels = [normalize(channel, [0, 100]) for channel in self._data]
            else:
                self._channels = [normalize(self._data, [0, 100])]
        else:
            if self._num_channels > 1:
                self._channels = [channel for channel in self._data]
            else:
                self._channels = [self._data]
        
        if absolute:
            self._channels = [np.abs(channel) for channel in self._channels]

    def plot(self):
        plt.plot(self.time, self.data, label="Left channel")
        if self._channels == 2:
            plt.plot(self.time, self.data[:, 1], label="Right channel")
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()
    
    def init_amplitude_list(self, time_unit: str | None=None, norm: bool=True):
        """
        Initializes a list of amplitude values sampled across time.

        This method analyzes the audio signal across all channels, samples the
        maximum amplitude at evenly spaced intervals, and stores the result in
        `self._amplitude_list`. It supports normalization and a configurable time step.

        Parameters
        ----------
        time_unit : str, optional
            The unit of time resolution for sampling. Accepted values are:
            - 's'  : seconds
            - 'ms' : milliseconds
            - 'us' : microseconds
            If not provided, the number of samples defaults to the number of time steps in the audio.
        
        norm : bool, optional
            If True, the amplitude values are normalized to [0, 100] before sampling. Default is True.

        Returns
        -------
        None
            The results are stored in the instance variable `self._amplitude_list`.

        Notes
        -----
        - If the audio is multi-channel, the maximum amplitude across all channels is used per sample.
        - Normalization scales each channel individually before sampling if `norm` is True.
        """
        if time_unit:
            num_samples = int(max(self._time)) * Time_Unit[time_unit].value
        else:
            num_samples = len(self.time) 

        self._split_channels(norm, True)

        amplitude_list = [0] * num_samples
        for i in range(num_samples):
            # Scale index to channel length
            data_idx = int(i * len(self._channels[0]) / num_samples)
            # Get the peak amplitude at point
            vol = int(max([channel[data_idx] for channel in self._channels]))
            amplitude_list[i] = vol

        self._amplitude_list = amplitude_list

    # Properties
    @property
    def file(self) -> str:
        """Path to the loaded WAV file."""
        return self._file

    @property
    def samplerate(self) -> int:
        """Sample rate of the audio."""
        return self._samplerate

    @property
    def duration(self) -> float:
        """Duration of the audio in seconds."""
        return self._duration
    
    @property
    def data(self) -> np.ndarray:
        """Raw audio data as a NumPy array."""
        return self._data

    @property
    def time(self) -> np.ndarray:
        """Time axis for the audio samples."""
        return self._time

    @property
    def amplitude_list(self) -> list | Exception:
        """List of peak amplitude values per time unit."""
        if self._amplitude_list:
            return self._amplitude_list
        else:
            raise Exception("The amplitude list has not yet been set. Initialize it using 'init_amplitude_list'.")

    
    @property
    def num_channels(self) -> int:
        """Number of audio channels (1=mono, 2=stereo, etc.)."""
        return self._num_channels

    @property
    def channels(self) -> list:
        """List of per-channel audio data arrays (split during processing)."""
        return self._channels

    @property
    def audio_mode(self) -> str:
        """Text label describing the audio mode ('mono', 'stereo', or '{n}-channel')."""
        match self._num_channels:
            case 1:
                return 'mono'
            case 2:
                return 'stereo'
            case _:
                return f'{self._num_channels}-channel'