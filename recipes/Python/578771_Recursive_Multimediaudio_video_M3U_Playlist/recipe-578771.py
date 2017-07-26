#!/usr/bin/env python
#-*- coding:utf-8 -*-

#---------
# IMPORT
#---------
import mimetypes, argparse, os, subprocess, re, urllib, sys, \
    errno, logging

#---------
# DEFINE
#---------
description = """
Generate an m3u playlist searching recursively
for multimedia files (video or audio) in the given
directory.
Information from ID3 tags will be extracted for audio
files with FFmpeg available.
"""

__doc__     = description 
__author__  = "Xian Jacobs <manobastardo@gmail.com>"
__date__    = "24 11 2013"
__version__ = "0.0"

options = [
    {
        "options": ["directory"],
        "help"  :
            "Directory to search recursively for multimedia "
            "files."
    },
    {
        "options": ["-p", "--play"],
        "action" : "store_true",
        "help"   :
            "Open the playlist located in the output "
            "directory."
    },
    {
        "options": ["-r", "--relative"],
        "action" : "store_true",
        "help"   :
            "Generate the playlist with local pathnames "
            "relative to the M3U file location."
    },
    {
        "options": ["-s", "--simulate"],
        "action" : "store_true",
        "help"   :
            "Dry run, don't write the playlist to a file."
    },
    {
        "options": ["-v", "--verbose"],
        "action" : "store_true",
        "help"   :
            "Print the files that would be used to generate "
            "the playlist."
    },
    {
        "options": ["-d", "--output-directory"],
        "action" : "store",
        "help"   : "Specify the output directory."
    },
    {
        "options": ["-f", "--output-filename"],
        "action" : "store",
        "help"   : "Specify the output file name."
    }
]

MARKER_FORMAT = "#EXTM3U"
MARKER_RECORD = "#EXTINF"

FORMAT_FILENAME = "{name}.m3u"
FORMAT_M3U      = "{marker}\n{playlist}"
FORMAT_INFO     = "{marker}:{duration},{artist} - {title}"
FORMAT_IOERROR  = "Invalid Output Directories {directories}"

REGEX_DURATION = re.compile(
    r"(.*Duration: )([0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9])",
    re.MULTILINE|re.DOTALL
)

stripnulls    = lambda data: data.replace("\00", "").strip()
filetitle     = lambda filePath: os.path.splitext(os.path.basename(filePath))[0]
alphatonum    = lambda text: int(text) if text.isdigit() else text 
alphanumkey   = lambda key: [alphatonum(c) for c in re.split("([0-9]+)", key)]

def sortAlphanum(items, index=0):
    return sorted(items, key=lambda x: alphanumkey(x[index]))

def timeSeconds(time):
    return int(sum(
        float(x) * 60 ** i
        for i,x in enumerate(reversed(time.split(":")))
    ))

def isProgramAvailable(program):
    def isExe(filePath):
        return all([
            os.path.isfile(filePath),
            os.access(filePath, os.X_OK)
        ])

    def isRunnable(program):
        try:
            subprocess.Popen(
                [program],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

        except (OSError, e):
            if e.errno == errno.ENOENT:
                return False

            raise

        return True

    def isAvailable(program):
        if isExe(program) and isRunnable(program):
            return True

        return False

    filePath, fileName = os.path.split(program)

    if filePath:
        if isAvailable(program):
            return True

    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path        = path.strip('"')
            filePathExe = os.path.join(path, program)

            if isAvailable(filePathExe):
                return True

    logging.warning("Program Missing: {0}".format(program))

    return False

class Playlist(object):
    extensionsInclude = [".f4v"]
    extensionsExclude = [".m3u"]

    fieldsTag  = {
        "title"   : (  3,  33, stripnulls),
        "artist"  : ( 33,  63, stripnulls),
        "album"   : ( 63,  93, stripnulls),
        "year"    : ( 93,  97, stripnulls),
        "comment" : ( 97, 126, stripnulls),
        "genre"   : (127, 128, ord)
    }

    def __init__(self, arguments):
        self.rootDirectory     = None
        self.arguments         = arguments
        self.ffmpegIsAvailable = isProgramAvailable("ffmpeg")

        mimetypes.init()

        self.extensions = self.extensionsInclude + [
            extension
            for extension in mimetypes.types_map
            if mimetypes.types_map[extension].split("/")[0]
                in ["video", "audio"]
        ]

    def generate(self, pathDirectory):
        self.rootDirectory = pathDirectory
        playlistItems      = self._getPlaylistItems(pathDirectory)
        playlistFilePath   = self.getFileOutput(pathDirectory)

        if self.arguments.verbose:
            self.printPlaylistItems(playlistItems)

        if not self.arguments.simulate:
            self.writePlaylistItems(playlistFilePath, playlistItems)

        if all([
            self.arguments.play,
            os.path.exists(playlistFilePath),
            os.path.isfile(playlistFilePath)
        ]):
            self.openPlaylist(playlistFilePath)

    def openPlaylist(self, playlistFilePath):
        if sys.platform.startswith('darwin'):
            subprocess.Popen(('open', playlistFilePath))

        elif os.name == 'nt':
            os.startfile(playlistFilePath)

        elif os.name == 'posix':
            subprocess.Popen(('xdg-open', playlistFilePath))

    def printPlaylistItems(self, playlistItems):
        playlist       = playlistItems["playlist"]
        playlistSorted = self.sortPlaylist(playlist)

        for playlistInfo in playlistSorted:
            print(playlistInfo[1])

    def _getPlaylistItems(self, pathDirectory):
        return {
            "marker"   : MARKER_FORMAT,
            "playlist" : self.getPlaylistInfo(pathDirectory)
        }

    def writePlaylistItems(self, filePath, items):
        with open(filePath, "w") as fileOutput:
            fileOutput.write(self.formatPlaylistItems(items))

    def sortPlaylist(self, playlist):
        return sortAlphanum(playlist, 1)

    def formatPlaylistItems(self, playlistItems):
        playlistFormatted = map(
            lambda tags: "\n".join(tags),
            playlistItems["playlist"]
        )

        playlistItems["playlist"] = "\n".join(playlistFormatted)

        return FORMAT_M3U.format(**playlistItems)

    def flattenPlaylist(self, playlist):
        return sum(playlist, [])

    def getPlaylistInfo(self, pathDirectory):
        playlist       = self.getPlaylistsInfos(pathDirectory)
        playlistFlat   = self.flattenPlaylist(playlist)
        playlistSorted = self.sortPlaylist(playlistFlat)

        return playlistSorted

    def getPlaylistsInfos(self, pathDirectory):
        return [
            self._formatTags(tags)
            for tags in self._getInfoTags(pathDirectory)
        ] 

    def getDirectoryOutput(self, directoryPaths):
        for directoryPath in directoryPaths:
            if  directoryPath != None \
            and os.path.exists(directoryPath) \
            and os.path.isdir(directoryPath):
                return directoryPath

        raise (IOError, FORMAT_IOERROR.format(directories=directoryPaths))
        
    def getNameOutput(self, directoryPlaylist):
        if self.arguments.output_filename != None:
            name = self.arguments.output_filename

        else:
            name = os.path.basename(directoryPlaylist)

        return FORMAT_FILENAME.format(name=name)

    def getFileOutput(self, pathDirectory):
        directoryPlaylist = pathDirectory.rstrip(os.path.sep)
        directoryOutput   = self.getDirectoryOutput([
            self.arguments.output_directory,
            directoryPlaylist,
        ])
        fileName      = self.getNameOutput(directoryPlaylist)
        filePath      = os.path.join(directoryOutput, fileName)

        return filePath

    def _formatTags(self, tags):
        return [
            (FORMAT_INFO.format(**fileTags), fileTags["path"])
            for fileTags in tags
        ]

    def _getInfoTags(self, pathDirectory):
        tagsFromFilePaths = [
            self._getTagsFromFileNames(directoryPath, fileNames)
            for directoryPath, directoryNames, fileNames in os.walk(pathDirectory)
        ]

        return tagsFromFilePaths

    def _getTagsFromFileNames(self, directoryPath, fileNames):
        tagsFromFilePaths = filter(
            lambda fileTag: fileTag != None,
            self.getTagsFromFileNames(directoryPath, fileNames)
        )

        return tagsFromFilePaths

    def getTagsFromFileNames(self, directoryPath, fileNames):
        return [
            self._getTagsFromFileName(directoryPath, fileName)
            for fileName in fileNames
        ]

    def _getTagsFromFileName(self, directoryPath, fileName):
        fileTitle, fileExtension = os.path.splitext(fileName)

        tagsFromFilePath = (
            self.getTagsFromFileName(os.path.join(directoryPath, fileName))
            if all([
                fileExtension in self.extensions,
                fileExtension not in self.extensionsExclude
            ])
            else None
        )

        return tagsFromFilePath

    def getMimeType(self, filePath):
        #fileUrl      = urllib.pathname2url(filePath)
        fileUrl      = "file:///{0}".format(filePath)
        fileMimeType = mimetypes.guess_type(fileUrl)[0]

        return (
            False
            if fileMimeType == None
            else fileMimeType.split("/")[0]
        )

    def getTagData(self, filePath):
        if self.getMimeType(filePath) != "audio":
            return None

        with open(filePath, "rb", 0) as fileInput:
            fileInput.seek(-128, 2)  
  
            return fileInput.read(128)

    def getTagsFromFileName(self, filePath):
        tagData = self.getTagData(filePath)

        tagsFromFilePath = dict(
            self._validateTagData(tag, start, end, parseFunc, tagData)
            if tagData != None
            else (tag, "")
            for tag, (start, end, parseFunc) in self.fieldsTag.items()
        )

        return self._formatTagsFromFilePath(filePath, tagsFromFilePath)

    def _validateTagData(self, tag, start, end, parseFunc, tagData):
        return (
            (tag, re.sub("[\n\t]", " ", str(parseFunc(tagData[start:end]))))
            if not self.validateTagData(tagData)
            else (tag, "")
        )

    def validateTagData(self, tagData):
        if "Reference&#32" in str(tagData):
            return False

        return self.checkEncoding(tagData) != ""

    def runFFmpeg(self, filePath):
        process = subprocess.Popen(
            ["ffmpeg", "-i", filePath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        stdout, stderr = process.communicate()

        return stdout

    def formatTime(self, time):
        try:
            return str(timeSeconds(REGEX_DURATION.match(time).group(2)))

        except AttributeError:
            return 0

    def getDuration(self, filePath):
        if not self.ffmpegIsAvailable:
            return 0

        time = self.runFFmpeg(filePath)

        return self.formatTime(time)

    def checkTagTitle(self, tagTitle, filePath):
        return (
            tagTitle
            if self.checkEncoding(tagTitle) != ""
            else filetitle(filePath)
        )

    def checkTagArtist(self, tagArtist):
        return (
            tagArtist
            if self.checkEncoding(tagArtist) != ""
            else os.path.basename(self.rootDirectory).strip()
        )

    def checkEncoding(self, text):
        #try:
        #    text.decode("utf-8")

        #except UnicodeDecodeError:
        #    return ""

        return text.strip()

    def getTagPath(self, filePath):
        filePathChild = re.sub(r"^"+re.escape(self.rootDirectory), "", filePath)

        return (
            filePathChild.lstrip(os.path.sep)
            if self.arguments.relative
            else filePath
        )

    def _formatTagsFromFilePath(self, filePath, tagsFromFilePath):
        tags = {
            "marker"   : MARKER_RECORD,
            "path"     : self.getTagPath(filePath),
            "duration" : self.getDuration(filePath),
            "title"    : self.checkTagTitle(tagsFromFilePath["title"], filePath),
            "artist"   : self.checkTagArtist(tagsFromFilePath["artist"])
        }

        tagsFromFilePath.update(tags)

        return tagsFromFilePath

class Parser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
       super(Parser, self).__init__(*args, **kwargs)

    def addOption(self, option):
        options = option["options"]
        option.pop("options")

        self.add_argument(*options, **option)
        
    def parseOptions(self, options):
        for option in options:
            self.addOption(option)
            
        return super(Parser, self).parse_args()
    
#---------
# MAIN
#---------
#if __name__ == "__main__":
parser    = Parser(description=description)
arguments = parser.parseOptions(options)

if all([
	os.path.exists(arguments.directory),
	os.path.isdir(arguments.directory)
]):
	playlist = Playlist(arguments)
	playlist.generate(arguments.directory)
