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
$ python translate.py ertugrul-1-01-en.txt tr > ertugrul-1-01-tr.txt 
$ python say.py ertugrul-1-01-en.txt
$ python say.py ertugrul-1-01-tr.txt
$ python combine.py ertugrul-1-01
$ ./video ertugrul-1-01
```

