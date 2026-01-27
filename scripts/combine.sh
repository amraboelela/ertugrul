ffmpeg -y -i OUTPUT.mp4 -i OUTPUT2.mp4 -filter_complex [0:v][1:v]concat=n=2:v=1 combinedFile.mp4
