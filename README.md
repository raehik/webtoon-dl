# WEBTOON / Naver Webtoon / LINE Manga comic downloader
A set of Python scripts that can parse [WEBTOON](https://www.webtoons.com/en)
RSS feeds, download comic episodes, and place the images into an HTML page
similar to the display on the WEBTOON site.

Originally written in 2016 targeting the English WEBTOON site (then LINE
Webtoon) to temporarily archive some comics.

## Usage


## Dependencies
Python 3, plus the following libraries:

  * Beautiful Soup (`pip install bs4`)
  * *(optional)* lxml (`pip install lxml`): if present, used as the HTML parser

## Authors
Originally created by [@raehik](https://twitter.com/raehik).

Many thanks to [adud](https://github.com/adud) for their fixes and improvements.

## Contributing
This was originally written by an underexperienced raehik in 2016-7 and wasn't
all that clear. Any PRs to improve or extend the project will be gladly
received!

## Compliance with WEBTOON's terms and conditions
[webtoon-toc]: http://www.webtoons.com/en/terms

*Correct as of 2021-04-27, TOCs last updated 2020-12-16.*

IANAL, this does not constitute legal advice.

To the authors' knowledge, this software does not breach WEBTOON's TOCs. No DRM
circumvention or bypassing is attempted -- the software acts as an autonomous,
but otherwise regular browser.

All users are encouraged to read the [WEBTOON terms and conditions][webtoon-toc]
and confirm that their usage is abiding.
