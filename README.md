# Learn language from Ertugrul

Learn Turkish and other languages through Ertugrul TV series

## Setup

```
$ sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
$ sudo chmod a+rx /usr/local/bin/youtube-dl
$ vim translation_key.py
key = "<PUT THE KEY FROM YOUR GOOGLE TRANSLATE API ACCOUNT>"
$ sudo easy_install pip
$ sudo pip install requests
$ brew install ffmpeg

```

## Usage

###Turkish

- To build episode 1 - 3 and translate from English to Turkish:

```
$ ./build 1 3 en tr
$ ./clean 1 3 en tr
```


**Title:** Learn Turkish from Ertugrul, 1 - 1

**Description:**

Learn Turkish language by listening to the conversation in Resurrection Ertugrul TV series, Season 1, Episode 1, in English then in Turkish. 

###Arabic

- To build episode 1 - 3 and translate from English to Arabic:

```
$ ./build 1 3 en ar
$ ./clean 1 3 en ar
```

**Title:** Learn Arabic from Ertugrul, 1 - 1

**Description:**

Learn Arabic language by listening to the conversation in Resurrection Ertugrul TV series, Season 1, Episode 1, in English then in Arabic. 

