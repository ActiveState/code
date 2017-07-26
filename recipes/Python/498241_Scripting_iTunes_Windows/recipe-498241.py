import win32com.client

def removeDeletedTracks():
  """This function will remove every song that is not currently accessible from your iTunes library"""
  #First, we create an instance of the iTunes Application
  itunes= win32com.client.Dispatch("iTunes.Application")
  
  #The ITTrackKindFile value will be use to check if a track is a physical file
  ITTrackKindFile=1
  
  #The tracks list object is obtained from the iTunes instance  with the following expression:
  #itunes.LibraryPlaylist.Tracks
  #this tracks list object has two fields/methods of interest:
  # The Count field contain the total number of tracks in your library
  # The Item(numTrack) method will return the track with number numTrack
  #     (Be aware that the numbering of the tracks start at 1, NOT at 0)
  mainLibrary = itunes.LibraryPlaylist
  tracks = mainLibrary.Tracks
  numTracks = tracks.Count
  deletedTracks=0
  
  #(optional)We can create a log file in which the names of the deleted songs are written
  #log=open("deletedTracks.txt","w")
  
  while numTracks  !=0:
    currTrack=tracks.Item(numTracks)
    if currTrack.Kind == ITTrackKindFile:
      if currTrack.Location == "":
        #Uncomment the lines below if you want to have the name of the deleted files saved in the log file
        #name_artist=currTrack.Artist
        #name_song=currTrack.Name
        #log.write("[%s] [%s]\n"%(name_artist.encode("utf-8"),name_song.encode("utf-8")))
        currTrack.Delete()
        deletedTracks+=1
    numTracks-=1
  
  
  if deletedTracks > 0:
    if deletedTracks == 1:
      print "Removed 1 dead track."
    else:
      print "Removed " + str(deletedTracks) + " dead tracks."
  else:
    print "No dead tracks were found."


    
def updateLyricsAndCreatePlaylist():
  """The aim of this function is to automatically add lyrics to the songs in your library.
  Additionally, a playlist named "SongsWithLyrics" is created, which will contain all the songs to 
  which lyrics have been added (so that you can find them easily if you feel like Karaokeing)
  Please note that it use a (non-provided) getLyrics function that, given an artist and a song name, 
  return the lyrics of the song or the None object if the lyrics are not available.
  """
  
  #We do the usual "initialisation" stuff, like in the removeDeadTracks function
  itunes= win32com.client.Dispatch("iTunes.Application")
  ITTrackKindFile=1
  mainLibrary = itunes.LibraryPlaylist
  tracks = mainLibrary.Tracks
  nbTracks = tracks.Count
  
  #We create a playlist named "SongsWithLyrics", which will contain all the updated songs
  playlist=itunes.CreatePlayList("SongsWithLyrics")
  
  for numTrack in range(1,nbTracks+1):
    currTrack = tracks.Item(numTrack)
    #Trying to access the lyrics field of WAV files seemed to raise an exception. Hence the following condition.
    if currTrack.Kind == ITTrackKindFile and currTrack.KindAsString!=u"WAV audio file":
      name_artist=currTrack.Artist
      name_song=currTrack.Name
      lyrics=currTrack.Lyrics
      #We update only songs which do not already have a lyrics
      if len(lyrics)==0:
        #The getLyrics function return the lyrics of a song (as a unicode string). I do not provide example sources for this function (see below)
        obtainedLyrics=getLyrics(name_artist,name_song)
        if obtainedLyrics!=None:
          #if we obtained the lyrics, we add the current track to our playlist...
          playlist.AddTrack(currTrack)
          #... and we update the lyrics field of the track
          currTrack.Lyrics=obtainedLyrics
