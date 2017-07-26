## Use PyAudio to play a list of WAV files  
Originally published: 2015-10-22 18:24:07  
Last updated: 2015-10-22 18:24:08  
Author: Vasudev Ram  
  
This recipe shows how to use PyAudio, a 3rd-party Python audio toolkit, to play a list of WAV files on your computer. This is an enhanced version of a basic WAV code example on the PyAudio site. You can specify either one WAV filename on the command line, like this:\n\npy pyaudio_play_wav.py chimes.wav\n\nor specify a text file containing names of WAV files to play, like this:\n\npy pyaudio_play_wav.py -f wav_fil_list.txt\n\nThe only dependency is PyAudio, which you can install with pip.\n