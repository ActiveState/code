#!/usr/bin/env python
""" 
This little script presents new heise-news-articles individually by title
and asks if it should download the corresponding mp3-file.
"""
import threading
import Queue
import os
import feedparser
from urllib import urlretrieve
#-----------------------------------------------------------------------------#
n_threads = 10
feed_url = "http://www.heise.de/newsticker/heise.rdf"
left_link = "http://www.heise.de/fastbin/audio_download" \
    "?meldung=http://www.heise.de/newsticker/meldung/"
try:
    archive_filename = "%s/.heise" % os.environ["HOME"]
except KeyError:
    archive_filename = "%s%sheise_archive" % (os.environ["HOMEPATH"], os.sep)
#-----------------------------------------------------------------------------#
class Downloader(threading.Thread):
    """ Class for worker-threads that download files. Don't tell Marx! """
    def __init__(self, links_filenames):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.links_filenames = links_filenames
        self.start()
    #-------------------------------------------------------------------------#
    def run(self):
        while True:
            link, filename = self.links_filenames.get()
            urlretrieve(link, filename)
            self.links_filenames.task_done()
#-----------------------------------------------------------------------------#
class Archive(object):
    def __init__(self):
        feed = feedparser.parse(feed_url)
        try:
            archive_file = open(archive_filename)
            old_links = archive_file.readlines()
            self.old_links = [link.strip() for link in old_links]
            archive_file.close()
        except IOError:
            self.old_links = []
        self.entries_i = range(len(feed["entries"]))
        self.feed_links = [feed["entries"][entry_i]["link"].encode("utf-8")
                           for entry_i in self.entries_i]
        self.feed = feed
    #-------------------------------------------------------------------------#
    def get_new_entries(self):
        new_links = [link for link in self.feed_links 
                     if link not in self.old_links]
        titles = [self.feed["entries"][entry_i]["title"].encode("utf-8")
                  for entry_i in self.entries_i
                  if self.feed["entries"][entry_i]["link"].encode("utf-8")
                  in new_links]
        # the article_id is in the link between "meldung/" and "/from"
        article_ids = [link.split("meldung/")[1].split("/from")[0]
                       for link in new_links]
        return new_links, titles, article_ids
    #-------------------------------------------------------------------------#
    def store(self):
        archive_file = open(archive_filename, "w")
        archive_file.writelines("\n".join(self.feed_links))
        archive_file.close()
#-----------------------------------------------------------------------------#
def prepare_workers():
    links_filenames = Queue.Queue() 
    return [Downloader(links_filenames) for ii in range(n_threads)][0]
#-----------------------------------------------------------------------------#
def start_download(link, title, id, downloader):
    for bad, good in zip(("/", ":", " ", '"', "?"), ("", "", "_", "", "")):
        title = title.replace(bad, good)
    filename = "heise_%s_%s.mp3" % (id, title)
    mp3_link = left_link + id
    downloader.links_filenames.put((mp3_link, filename))
#-----------------------------------------------------------------------------#
if __name__ == "__main__":
    downloader = prepare_workers()

    feed_archive = Archive()
    links, titles, ids = feed_archive.get_new_entries()

    for link, title, id in zip(links, titles, ids):
        download_yn = None
        while download_yn != "y" and download_yn != "n" and download_yn != "c":
            print title
            download_yn = raw_input('Download mp3? (y/[n]/c)')
            if download_yn == "":
                download_yn = "n"
        if download_yn == "y":
            start_download(link, title, id, downloader)
        if download_yn == "c":
            break

    if links:
        print "Waiting for downloads to end..."
        downloader.links_filenames.join()
        feed_archive.store()
