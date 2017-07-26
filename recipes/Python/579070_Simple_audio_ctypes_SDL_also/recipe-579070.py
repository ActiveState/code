import ctypes
from ctypes.util import find_library
import os


_sdl_audio_init=False
_sdl_audio_music=None
_sdl_audio_sounds={}

_libsdl=None
_libsdl_mixer=None

def sdl_audio_load(snd,fn=None,reload=False):
 global _sdl_audio_sounds,_libsdl,_libsdl_mixer
 if snd not in _sdl_audio_sounds or reload:
  sdl_audio_init()
  if snd in _sdl_audio_sounds: _libsdl_mixer.Mix_FreeChunk(_sdl_audio_sounds[snd])
  rw=_libsdl.SDL_RWFromFile(fn,'rb')
  _sdl_audio_sounds[snd]=_libsdl_mixer.Mix_LoadWAV_RW(rw,1)

def sdl_audio_play(snd,loop=0,channel=-1):
 global _sdl_audio_sounds,_libsdl_mixer
 sdl_audio_load(snd)
 _libsdl_mixer.Mix_PlayChannelTimed(channel,_sdl_audio_sounds[snd],loop,-1)

def sdl_audio_stop(channel=-1):
 global _libsdl_mixer
 return _libsdl_mixer.Mix_HaltChannel(channel)

def sdl_audio_volume(volume=-1,channel=-1):
 global _libsdl_mixer
 if type(volume) is type(.1): volume=int(volume*128)
 return _libsdl_mixer.Mix_Volume(channel,volume)


def sdl_audio_init():
 global _sdl_audio_init,_libsdl,_libsdl_mixer
 if _sdl_audio_init: return None

 try: _libsdl=ctypes.cdll.SDL
 except:
  name=find_library('SDL')
  if name is None: return False
  _libsdl=ctypes.cdll.LoadLibrary(name)
 
 try: _libsdl_mixer=ctypes.cdll.SDL_mixer
 except:
  name=find_library('SDL_mixer')
  if name is None: return False
  _libsdl_mixer=ctypes.cdll.LoadLibrary(name)
 
 _libsdl.SDL_Init(0)
 _libsdl.SDL_InitSubSystem(0x00000010)# Init audio subsystem
 _libsdl_mixer.Mix_Init()
 _libsdl_mixer.Mix_OpenAudio(44100,0x8010,2,512)
 _sdl_audio_init=True
 return True


def sdl_audio_playmusic(fn,loop=1):
 global _sdl_audio_music,_libsdl_mixer
 sdl_audio_init()
 sdl_audio_stopmusic()
 _sdl_audio_music=_libsdl_mixer.Mix_LoadMUS(os.path.realpath(fn))
 _libsdl_mixer.Mix_PlayMusic(_sdl_audio_music,loop)

def sdl_audio_pausemusic():
 global _sdl_audio_music,_libsdl_mixer
 if _sdl_audio_music is not None:
  if _libsdl_mixer.Mix_PlayingMusic(): _libsdl_mixer.Mix_PauseMusic()

def sdl_audio_stopmusic():
 global _sdl_audio_music,_libsdl_mixer
 sdl_audio_pausemusic()
 _libsdl_mixer.Mix_HaltMusic()
 _libsdl_mixer.Mix_FreeMusic(_sdl_audio_music)
 _sdl_audio_music=None

def sdl_audio_volumemusic(volume=-1):
 global _libsdl_mixer
 if type(volume) is type(.1): volume=int(volume*128)
 return _libsdl_mixer.Mix_VolumeMusic(volume)

def sdl_audio_quit():
 global _sdl_audio_init,_sdl_audio_sounds,_libsdl,_libsdl_mixer
 if not _sdl_audio_init: return False
 sdl_audio_stopmusic()
 sdl_audio_stop()
 map(lambda chunk: _libsdl_mixer.Mix_FreeChunk(chunk),_sdl_audio_sounds.values())
 _libsdl_mixer.Mix_CloseAudio()
 _libsdl_mixer.Mix_Quit()
 _libsdl.SDL_Quit()
 return True
