from pydub import AudioSegment
from os import path

def convert(input_file: str):
    try:
        output_file = f'./content/temp/{path.splitext(path.basename(input_file))[0]}.wav'

        audio = AudioSegment.from_mp3(input_file)
        audio.export(output_file, format="wav")

        return output_file
    except:
        return FileNotFoundError