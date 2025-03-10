import whisper

# Load a Whisper model (choose a model size like "small", "base", etc.)
# available model sizes: tiny, base, small, medium	and large
model = whisper.load_model("large")

# Transcribe the audio file (ensure 'audio.mp3' is available in your working directory)
result = model.transcribe("sample.wav")

# Print the transcribed text
print(result["text"])


# It also requires the command-line tool ffmpeg to be installed on your system, which is
# available from most package managers:
# # on Ubuntu or Debian
# sudo apt update && sudo apt install ffmpeg
#
# # on Arch Linux
# sudo pacman -S ffmpeg
#
# # on MacOS using Homebrew (https://brew.sh/)
# brew install ffmpeg
#
# # on Windows using Chocolatey (https://chocolatey.org/)
# choco install ffmpeg
#
# # on Windows using Scoop (https://scoop.sh/)
# scoop install ffmpeg