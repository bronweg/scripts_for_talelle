#!/bin/bash
if [[ $1 == "--simple" ]]; then
  python3 $(dirname $0)/create_simple_slideshow.py -a ./sources/*.mp3 -p ./sources/photos -o $(basename ${PWD}).mp4
else
  python3 $(dirname $0)/create_slideshow_picture_change_by_beat.py -a ./sources/*.mp3 -p ./sources/photos -o $(basename ${PWD}).mp4
fi
