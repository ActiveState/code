# Control iTunes from TCL using TCOM package on Windows

# [http://www.vex.net/~cthuang/tcom/](http://www.vex.net/~cthuang/tcom/)
package require tcom

# start iTunes or take over existing iTunes application if already running
set i [::tcom::ref createobject "iTunes.Application"]

# get iTunes version
$i Version
	9.0.3.15

# set volume (0 to 100)
$i SoundVolume 75

# play the currently selected track
$i Play
$i Stop

$i Pause
$i Resume

$i PreviousTrack
$i NextTrack

# get current song play position (seconds)
$i PlayerPosition

# set song position (seconds)
$i PlayerPosition 96

# Track info
set track [$i CurrentTrack]
$track Name
$track Album
$track Artist
$track Time
$track BPM
$track Year
$track Comment
$track Kind
$track KindAsString

# Example track:
foreach t {Artist Name Time Album Year BPM Comment KindAsString} {puts [format "%-12s: %s" $t [$track $t]]}
	Artist      : The Fixx
	Name        : Saved By Zero
	Time        : 3:26
	Album       : React
	Year        : 1987
	BPM         : 90
	Comment     : TCL rocks
	KindAsString: MPEG audio file


# GET ALL AVAILABLE ITUNES METHODS
set iid [::tcom::info interface $i]
$iid methods

# dump a sorted list of all itunes tcom calls
foreach m [lsort -index 2 -unique [$iid methods]] {puts [lindex $m 2]}
	AppCommandMessageProcessingEnabled
	Authorize
	BackTrack
	BrowserWindow
	CanSetShuffle
	CanSetSongRepeat
	CheckVersion
	ConvertFile
	ConvertFile2
	ConvertFiles
	ConvertFiles2
	ConvertOperationStatus
	ConvertTrack
	ConvertTrack2
	ConvertTracks
	ConvertTracks2
	CreateEQPreset
	CreateFolder
	CreateFolderInSource
	CreatePlaylist
	CreatePlaylistInSource
	CurrentEQPreset
	CurrentEncoder
	CurrentPlaylist
	CurrentStreamTitle
	CurrentStreamURL
	CurrentTrack
	CurrentVisual
	EQEnabled
	EQPresets
	EQWindow
	Encoders
	FastForward
	ForceToForegroundOnDialog
	FullScreenVisuals
	GetITObjectByID
	GetITObjectPersistentIDs
	GetPlayerButtonsState
	GotoMusicStoreHomePage
	ITObjectPersistentIDHigh
	ITObjectPersistentIDLow
	LibraryPlaylist
	LibrarySource
	LibraryXMLPath
	Mute
	NextTrack
	OpenURL
	Pause
	Play
	PlayFile
	PlayPause
	PlayerButtonClicked
	PlayerPosition
	PlayerState
	PreviousTrack
	Quit
	Resume
	Rewind
	SelectedTracks
	SetOptions
	SoundVolume
	SoundVolumeControlEnabled
	Sources
	Stop
	SubscribeToPodcast
	UpdateIPod
	UpdatePodcastFeeds
	Version
	VisualSize
	Visuals
	VisualsEnabled
	Windows
