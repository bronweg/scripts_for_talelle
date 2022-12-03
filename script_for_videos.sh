youtube-dl -f 'best[height<=480]' --external-downloader=aria2c --external-downloader-args '--min-split-size=1M --max-connection-per-server=16 --max-concurrent-downloads=16 --split=16' -ia list --exec "ffpb -i {} -c:v libx265 -crf 26 -preset fast -c:a aac -b:a 128k {}_h265.mp4"
#detox -v ./*
#export todelete
#while read file; do todelete+=($file); done <<< $(ls -1 -I list -I "*_h265*")
#for file in ${todelete[@]}; do rm -f $file; done


#youtube-dl --external-downloader=aria2c --external-downloader-args '--min-split-size=1M --max-connection-per-server=16 --max-concurrent-downloads=16 --split=16' -ia list --merge-output-format mp4
#find -name "* *" -type f | rename 's/ /_/g'
#for file in $(ls -1 -I list -I "*_h265*"); do ffpb -i ${file} -c:v libx265 -crf 26 -preset fast -c:a aac -b:a 128k ${file%.*}_h265.mp4; if [[ $? == 0 ]]; then todelete+=($file); else echo -e "Error!\nCannot convert ${file}"; fi; done

#for file in $(ls -1 -I "^list$"); do ffmpeg -i ${file} -c:v libx265 -crf 26 -preset fast -c:a aac -b:a 128k ${file%.*}_h265.mp4; done
#find . ! -name '*_h265.mp4' ! -name list -maxdepth 1 -type f -delete
