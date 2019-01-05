# Word Replace 
This is a fun project I started after I realized the idea with a friend of mine. It is a script written in python and makes use of Worknik API for some translations.

It takes a block of text from a text file (input.txt) and produces a new block of text (output.txt), where each word from the original has been replaced with it's phonetic spelling. Punctuation is handled and included in output in correct place.

## Using this script

To use you must have a key for Wordnik API, which can be found [here](https://developer.wordnik.com/). I need to change some things around for use without it and offline.

This script is run from command line and takes 1 argument (ipa: for IPA translation, ahd: for AHD translation).

## Two options for phonetic alphabets/notations
[Internation Phonetic Alphabet (IPA)](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet)
- Stored locally and loaded into a dict, so this runs quickly.
- If no suitible replacement is found, then original word is unchanged.
- Produces translations that aren't as intuitive to read, but is more internationally useable.

[American Heritage Dictionary phonetic notation (AHD)](https://en.wikipedia.org/wiki/Phonetic_notation_of_the_American_Heritage_Dictionary)
- Uses Wordnik API for translations, which it means it runs much slower than the previous option.
- If no suitible replacement is found, then original word is unchanged. 
- Produces the most readable translations. Also, the most fun to try and read.

## Possible future improvements
* Find english to AHD notation data that could be stored locally.
  - This would speed up translation a great deal.

* Add other alphabets and notations.
  - There are others that could be implemented.

* Implement GUI.
  - Idea for more fleshed out app?
* Optimize.
