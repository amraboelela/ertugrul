# ertugrul
Learn Turkish and other languages through Ertugrul TV series

## Usage

- Do this part in MacOS:

```
$ python clean ertugrul-1-01-en.vtt > ertugrul-1-01-en.txt
```

Then manually inspect the text file and remove some of the lines. Then continue, as following:

```
$ python translate ertugrul-1-01-en.txt tr 
$ python say ertugrul-1-01-en.txt
$ python say ertugrul-1-01-tr.txt
$ zip -r ertugrul-1-01.zip ertugrul-1-01
$ scp ertugrul-1-01.zip amr@amrpro.loca:ertugrul
```

- Then do this part in Linux (Ubuntu)

```
$ unzip ertugrul-1-01.zip
$ python combine.py ertugrul-1-01
```

- Then test the audio file in MacOS:

```
$ scp amr@amrpro.local:ertugrul/ertugrul-1-01-en.m4a .
```

- Then generate the video file in Linux:

```
$ ./video ertugrul-1-01
```

- Then test the video file in MacOS:

```
$ scp amr@amrpro.local:ertugrul/ertugrul-1-01-en.mp4 .
```

