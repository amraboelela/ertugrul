# Learn language from Ertugrul

Learn Turkish and other languages through Ertugrul TV series

## Setup

```
$ sudo mkdir -p /usr/local/bin
$ sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
$ sudo chmod a+rx /usr/local/bin/youtube-dl
$ vim translation_key.py
key = "<PUT THE KEY FROM YOUR GOOGLE TRANSLATE API ACCOUNT>"
$ sudo easy_install pip
$ sudo pip3 install requests
$ sudo pip3 install gTTS
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
$ brew install ffmpeg
$ brew install handbrake
```

To install latest version of ffmpeg:

[ffmpeg install in macOS](https://trac.ffmpeg.org/wiki/CompilationGuide/macOS)

```
$ cd resources
$ git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
$ cd ffmpeg
$ ./configure  --prefix=/usr/local --enable-gpl --enable-nonfree --enable-libass \
--enable-libfdk-aac --enable-libfreetype --enable-libmp3lame \
--enable-libtheora --enable-libvorbis --enable-libvpx --enable-libx264 --enable-libx265 --enable-libopus --enable-libxvid \
--samples=fate-suite/
$ make
$ sudo make install

```

## Usage

###Turkish

- To build episode 1 - 3 and translate from English to Turkish:

```
$ ./build.sh 1 3 en tr
$ ./clean 1 3 en tr
```

**Title:** Learn Turkish from Ertugrul Subtitles, 1 - 1

**Description:**

Learn Turkish language by listening to the conversation in Resurrection Ertugrul TV series, Season 1, Episode 1, in Turkish, and see the meaning in English of the subtitles.
Check also Ertugrul dictionary: https://github.com/amraboelela/ertugrul/blob/master/build/dictionary-tr.txt

###Arabic

- To build episode 1 - 3 and translate from English to Arabic:

```
$ ./build.sh 1 3 en ar
$ ./clean 1 3 en ar
```

**Title:** Learn Arabic from Ertugrul, 1 - 1

**Description:**

Learn Arabic language by listening to the conversation in Resurrection Ertugrul TV series, Season 1, Episode 1, in English then in Arabic. 
Check also Ertugrul dictionary: https://github.com/amraboelela/ertugrul/blob/master/build/dictionary-ar.txt

