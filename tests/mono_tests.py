import unittest
from ezwav import Wav

class TestWav(unittest.TestCase):
    wav_path = './local_testing/bear_growl_y.wav'

    def test_wav_creation(self):
        try:
            wav_obj = Wav(self.wav_path)
        except Exception as e:
            self.fail(f"Failed to create Wav object: {e}")
        self.assertIsNotNone(wav_obj, "Wav object should not be None")

    def test_amplitude_list_uninitialized(self):
        wav_obj = Wav(self.wav_path)
        with self.assertRaises(Exception) as context:
            _ = wav_obj.amplitude_list
        
        exception_message = str(context.exception)
        self.assertIn('The amplitude list has not yet been set', exception_message)

    def test_amplitude_list_initialized(self):
        wav_obj = Wav(self.wav_path)
        wav_obj.init_amplitude_list('S')
        
        amplitude_list = wav_obj.amplitude_list
        self.assertIsNotNone(amplitude_list, "Amplitude list should not be None after initialization")
        self.assertIsInstance(amplitude_list, list, "Amplitude list should be a list")
        self.assertGreater(len(amplitude_list), 0, "Amplitude list should not be empty after initialization")

if __name__ == '__main__':
    unittest.main()
