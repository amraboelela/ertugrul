# Learn language from Ertugrul, while you sleep

Learn Turkish and other languages through Ertugrul TV series

## Using computer voice

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
$ mv Resurrection\ Ertugrul\ Season\ 1\ Episode\ 1-dnZcS74eg5U.en-GB.vtt ertugrul-1-01-en.vtt
$ ./build 1 1 10 en tr
```

## Turkish

- Title: Learn Turkish from Ertugrul, while you sleep, 1 - 1

- Description:

Learn Turkish language by listening to the conversation in Resurrection Ertugrul TV series, Season 1, Episode 1, in English then in Turkish. It can help you sleep faster :)

## Arabic

- Title: Learn Arabic from Ertugrul, while you sleep, 1 - 1

- Description:

Learn Arabic language by listening to the conversation in Resurrection Ertugrul TV series, Season 1, Episode 1, in English then in Arabic. It can help you sleep faster :)

## Using original voice

```
$ ./download -o https://www.youtube.com/watch?v=5fJXATpIiUQ
```

$ ffmpeg -i ertugrul-1-01-original.m4a -acodec copy -ss 00:02:12 -to 00:02:15 ertugrul-1-01-original-001.m4a
$ ffmpeg -i ertugrul-1-01-original.m4a -acodec copy -ss 00:08:47 -to 00:08:50 ertugrul-1-01-original-100.m4a

