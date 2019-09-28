# ertugrul
Learn Turkish and other languages through Ertugrul TV series

## Usage

```
$ ./download https://www.youtube.com/watch?v=VjC0fS7wYME
```

- If you get error, then:

```
$ sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
$ sudo chmod a+rx /usr/local/bin/youtube-dl
```

- Then do:

```
$ python clean.py ertugrul-1-01-en.vtt > ertugrul-1-01-en.txt
$ vim ertugrul-1-01-en.txt
$ ./buildAll
```

- Title: Learn Turkish from Ertugrul 1 - 1

- Description:

Learn Turkish language by listening to the conversation in Resurrection Ertugrul TV series, Season 1, Episode 1, in English then in Turkish.

