yt-dlp --external-downloader=aria2c --external-downloader-args '--min-split-size=1M --max-connection-per-server=16 --max-concurrent-downloads=16 --split=16' -ia list -x --audio-format mp3 --restrict-filenames
#youtube-dl -a list -x --audio-format mp3 --restrict-filenames
#find -name "* *" -type f | rename 's/ /_/g'
#for file in $(ls -1 -I "*.mp3"); do ffmpeg -i ${file} -vn -ar 44100 -ac 2 -b:a 192k ${file%.*}.mp3; done
#find . ! -name '*.mp3' ! -name list -type f -delete
