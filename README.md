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
$ sudo pip install gTTS
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew install ffmpeg
$ brew install handbrake
```

To install latest version of ffmpeg:

```
$ git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
$ cd ffmpeg
$ ./configure --enable-gpl --enable-libfreetype --enable-libmp3lame --enable-libvorbis --enable-libvpx --enable-libx264 --enable-nonfree --enable-shared 
$ make -j8
$ sudo make install

```

## Usage

###Turkish

- To build episode 1 - 3 and translate from English to Turkish:

```
$ ./build.sh 1 3 en tr
$ ./clean 1 3 en tr
```

- For simplified version, which has only scense of at least 3 seconds of no talking

```
$ ./build-s.sh 1 3 en tr
```

**Title:** Learn Turkish from Ertugrul, 1 - 1

**Description:**

Learn Turkish language by listening to the conversation in Resurrection Ertugrul TV series, Season 1, Episode 1, in English then in Turkish. 
Check also Ertugrul dictionary: https://github.com/amraboelela/ertugrul/blob/master/build/dictionary-tr.txt

###Arabic

- To build episode 1 - 3 and translate from English to Arabic:

```
$ ./build.sh 1 3 en ar
$ ./clean 1 3 en ar
```

Or

```
$ ./build-s.sh 1 3 en ar
```

**Title:** Learn Arabic from Ertugrul, 1 - 1

**Description:**

Learn Arabic language by listening to the conversation in Resurrection Ertugrul TV series, Season 1, Episode 1, in English then in Arabic. 
Check also Ertugrul dictionary: https://github.com/amraboelela/ertugrul/blob/master/build/dictionary-ar.txt

