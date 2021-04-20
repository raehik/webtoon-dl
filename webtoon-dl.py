#!/usr/bin/env python3
#
# Download all images from a LINE Webtoon comic episode.
#

import sys
import argparse
import os
from bs4 import BeautifulSoup, FeatureNotFound
from urllib import request
import shutil
from http.cookiejar import MozillaCookieJar

img_referer = 'http://www.webtoons.com'
FILENAME = sys.argv[0]

"""Argparse override to print usage to stderr on argument error."""
class ArgumentParserUsage(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help(sys.stderr)
        sys.exit(2)

"""Print usage and exit depending on given exit code."""
def usage(exit_code):
    if exit_code == 0:
        pipe = sys.stdout
    else:
        # if argument was non-zero, print to STDERR instead
        pipe = sys.stderr

    parser.print_help(pipe)
    sys.exit(exit_code)

"""Log a message to a specific pipe (defaulting to stdout)."""
def log_message(message, pipe=sys.stdout):
    print("{}: {}".format(FILENAME, message), file=pipe)

"""If verbose, log an event."""
def log(message):
    if not args.verbose:
        return
    log_message(message)

"""Log an error. If given a 2nd argument, exit using that error code."""
def error(message, exit_code=None):
    log_message("error: " + message, sys.stderr)
    if exit_code:
        sys.exit(exit_code)

parser = ArgumentParserUsage(description="Download all images from a LINE Webtoon comic episode.")
parser.add_argument("-v", "--verbose", action="store_true", help="be verbose")
parser.add_argument("-d", "--dir", default=".",
                    help="directory to store downloaded images in (default: .)")
parser.add_argument("-e", "--episodes", action="store_true",
                    help="download episodes in separate directories "
                    "regardless the provided episode")
parser.add_argument("url", metavar="URL", help="Webtoon comic URL")
args = parser.parse_args()

# force verbosity for now
args.verbose = True

jar = MozillaCookieJar("cookies.txt")
jar.load()

def get_soup(url):
    """Retrieve a page and return it as a BeautifulSoup object"""
    log("Downloading url {}".format(url))
    req = request.Request(url)
    jar.add_cookie_header(req)
    page = request.urlopen(req)
    try:
        soup = BeautifulSoup(page, "lxml")
    except FeatureNotFound:
        log("lxml not found, using html.parser instead")
        soup = BeautifulSoup(page, "html.parser")
    return soup
    
def get_image_urls(soup):
    """Retrieve all image URLs to download."""
    img_dl_urls = []

    imgs = soup.find_all(class_="_images")
    for img in imgs:
        # get image URL, remove the lower quality bit GET
        img_url = img["data-url"].replace("?type=q90", "")
        img_dl_urls.append(img_url)

    return img_dl_urls

def get_episodes_urls(soup):
    """Retrieve the URLs of the others episodes"""
    ep_list = soup.find(class_="episode_cont")
    return [ep.find("a")["href"] for ep in ep_list.ul.findAll("li")]
    
def download_images(urls, outdir):
    """Download each image in urls to existing directory outdir."""
    referer_header = { "Referer": img_referer }
    count = 0
    for url in urls:
        log("Downloading image {} at {}".format(count, url))
        count += 1
        req = request.Request(url, headers=referer_header)
        with request.urlopen(req) as response, open("{}/{:03}.jpg".format(outdir, count), "wb") as outfile:
            shutil.copyfileobj(response, outfile)

def download_episode(url, outdir):
    img_urls = get_image_urls(get_soup(url))
    download_images(img_urls, outdir)
            
if os.path.exists(args.dir):
    if not os.path.isdir(args.dir):
        error("not a directory: {}".format(args.dir), 1)
else:
    os.makedirs(args.dir, exist_ok=True)

if args.episodes:
    for no,url in enumerate(get_episodes_urls(get_soup(args.url))):
        outdir = os.path.join(args.dir, "{:03}".format(no))
        os.makedirs(outdir, exist_ok=True)
        download_episode(url, outdir)
else:
    download_episode(args.url, args.dir)
