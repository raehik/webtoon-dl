"""Create a webpage (same as make-page but in python)"""

from sys import argv
from argparse import ArgumentParser
from os.path import dirname, basename, splitext, join
from os import listdir

from bs4 import BeautifulSoup

DIRNAME = dirname(argv[0])
EXT = ".jpg"

parser = ArgumentParser(
    description="Create a webpage to display a comic in browser")

parser.add_argument("-t", "--title", help="page title")
parser.add_argument("-s", "--style", help="the style sheet",
                    default=join(DIRNAME, "main.css"))
parser.add_argument("-o", "--outfile", help="outfile name", default="./")
parser.add_argument("-v", "--verbose", help="be verbose")


def guess_files(d):
    """guess files that are probably comic panels"""
    return [x for x in listdir(d)
            if splitext(basename(x))[0].isdecimal()]


def make_episode(flist, title, css):
    """return the soup of a webpage containing an episode
    title: the list of the episodes
    flist: the list of the images"""
    with open(join(DIRNAME, "template.html")) as _f:
        soup = BeautifulSoup(_f)
    soup.head.title.string = title
    soup.head.link["href"] = css
    soup.body.extend([soup.new_tag("img", src=f) for f in flist])
    return soup


if __name__ == "__main__":
    args = parser.parse_args()
    print(make_episode(guess_files(args.outdir), args.title, args.style))
