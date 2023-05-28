# srt_translate_with_GPT

## Description

Translate text from one language to another.

## Getting Started

```
git clone https://github.com/watchakorn-18k/srt_translate_with_GPT.git

cd srt_translate_with_GPT

```

## Installation

```
# create virtualenv auto name
fenv onlyenv

# install package in requirements.txt
fenv install

```

## Usage

```
python main.py --filename <filename> --mode <mode>
```

```
usage: main.py [-h] --filename FILENAME [--mode MODE]

options:
  -h, --help           show this help message and exit
  --filename FILENAME  Example `anime\test.ass`
  --mode MODE           Example `s`,`m`  s: single <default>, m: multithread
```

```
python main.py --filename "G:\FILE_ANIME\ORC-FOR_SUBTTITLE\File_srt\lolsf-14.ass" --mode m
```

## Tree

<!--- Start Tree --->

```bash
.
└── srt_translate_with_GPT/
        └──.vscode/
                └──settings.json
        └──env_srt_translate_with_GPT/
        └──.gitignore
        └──main.py
        └──readme.md
        └──requirements.txt

```

<!--- End Tree --->

## API List

```
http://srttranslategptapi.wk18k.repl.co/
http://srttranslategptapi2.wk18k.repl.co/
http://srttranslategptapi3.wk18k.repl.co/
http://srttranslategptapi4.wk18k.repl.co/
http://srttranslategptapi5.wk18k.repl.co/
http://srttranslategptapi6.wk18k.repl.co/
```

## Make Your API

> Go to `https://replit.com/@wk18k/SRTTRANSLATEGPTAPI#main.py`

- > Then click button `Fork`<p align="lefit"><img src="https://cdn.discordapp.com/attachments/585069498986397707/1112287088969269319/image.png"></p>
- > Then rename the project as you wish and click button `Fork Repl` <p align="lefit"><img src="https://cdn.discordapp.com/attachments/585069498986397707/1112287925271531550/image.png"></p>
- > Then click button `Run` <p align="lefit"><img src="https://cdn.discordapp.com/attachments/585069498986397707/1112288445210034236/image.png"></p>
- > This is your API URL <p align="lefit"><img src="https://cdn.discordapp.com/attachments/585069498986397707/1112288649866907658/image.png"></p>
- > Add url to `url_api.json`

\*\* Change `https://....` to `http://....` for prevent errors

## Contributing

If you would like to contribute to the project, include a section on how to do so, including any guidelines and best practices.

## License

Include information about the license used for the project, such as the name of the license (e.g. MIT, Apache 2.0, etc.) and a link to the license text.
