# pronunciation-trainer
A simple app to help improve your pronunciation when learning a new language.

# Languages
| French | English |
|--------|---------|

# Installation
```
git clone https://github.com/taylorhmorris/pronunciation-trainer.git
cd pronunciation-trainer
python -m pip install -r requirements.txt
```

## Speech-To-Text
There are two possible engines to use to evaluate your speech.
### Using CMU Sphinx (offline use)
The en-US language pack is installed by default. To use with fr-FR, it is necessary to install the French language pack following [these instructions](https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst#installing-other-languages).

### Using Google Speech-To-Text (no offline use)
It is necessary to have an API key from Google

# Usage
```
python -m pronunciation_trainer
```

## Creating Lessons
The included lessons are intended solely as a demo. The real power is in creating lessons according to your own needs.

Lessons are simple text files comprised of a heading line and one or more lines containing a word/phrase pair.

The heading should be of the form `<LANGUAGE>:<TITLE>`, where `<LANGUAGE>` is one of the installed language packs and `<TITLE>` is a title of your choosing.
### Example
```
fr-FR:Numbers
```

The rest of the text file is comprised of lines of word/phrase pairs separated by a colon (`:`).

The text to the left of the colon will be displayed in the phraselist, the text to the right will be the expected phrase to be uttered. This allows you give yourself a different hint instead of the expected text (ex. the text in English when French pronunciation is being tested).

### Example
`numbers.txt`
```
fr-FR:Numbers
one:un
two:deux
three:trois
```
This will show English numbers and expect the user to speak the numbers in French.

