# Cerca

[Cerca](http://cerca-language.herokuapp.com)

1. Remove Google Analytics script tag from index.html

2. Microsoft Translator services credentials should be stored in environment variables:
  * CERCA_MST_ID
  * CERCA_MST_SECRET

3. After deployment run in ssh shell:
`python phoneticfy.py en ./data/google-10000-english-no-swears.txt`

## Credits
* [google-1000-english](https://github.com/first20hours/google-10000-english)