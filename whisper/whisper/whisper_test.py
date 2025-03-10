
import os
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import torch
import numpy as np
import openai
from dotenv import load_dotenv
load_dotenv()
import pyperclip

def record():

    print(sd.query_devices())
    print(sd.check_input_settings())
    # to sett correctly fs, for windows refer to this:
    # https://stackoverflow.com/questions/57467633/why-do-i-get-a-invalid-device-error-when-recording-a-device-using-wasapi-and-t
    fs = 44100  
    
    #sd.default.device = 'digital output'

    #recording duration in seconds
    seconds = 8  
    
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    print("Record in progress, start speaking")
    sd.wait()  # Wait until recording is finished
    print("recording finished")
    write('output.mp3', fs, myrecording)  # Save as MP3 file

def speechtotext():

    # code below is fow windows
    # torch.cuda.is_available()
    # DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    # code below for Apple Silicon (M1, M2)
    DEVICE = "mps"  if torch.backends.mps.is_available() else "cpu"
    
    # no way to make it work on Apple Silicon :(
    # backing up to cpu :( :( :(
    # DEVICE = "cpu"
    print(DEVICE)
    # whishper model list https://github.com/openai/whisper/blob/main/README.md#available-models-and-languages
    # MODEL IS DOWLOADED IN Users/gp/.cache/whisper
    model = whisper.load_model("large", device=DEVICE)
    print(
        f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
        f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
    )
    wishper.lo
    audio = whisper.load_audio('output.mp3')
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)
    print(result.text)
    return result.text
    #result = model.transcribe('output.mp3', options)
    #print(result["text"])
    #return result["text"]

def generate_mail(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Write a kind email for this: I can not come to work today because im really sick\n\nHi there,\n\nI'm sorry for the short notice, but I won't be able to come in to work today. I'm really sick and need to rest. I'll be back to work tomorrow. Hope you all have a wonderful day.\n\nThanks,\n\n[Your Name]\n\n\nWrite a kind email for this: {text}",
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text

def main():
    #record() # in seconds
    text = speechtotext()
    #email = generate_mail(text)
    #print(email)
    #pyperclip.copy(email)

if __name__ == "__main__":
    main()