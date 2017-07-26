## Simple directory list command with filename wildcard support  
Originally published: 2016-12-02 20:52:55  
Last updated: 2016-12-02 20:52:56  
Author: Vasudev Ram  
  
This recipe shows a simple directory listing program. It can accept multiple command-line arguments specifying filenames. These filenames can include wildcard characters like * (asterisk) and ? (question mark), as is common in OS command shells like bash (Unix) and CMD (Windows). Tested on Windows but should work on Unix too, since it uses no OS-specific functions, or rather, it does use them, but that happens under the hood, within the libraries used.
