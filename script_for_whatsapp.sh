#!/bin/bash
export file=$1
ffmpeg -i ${file} -c:v libx264 -profile:v baseline -level 3.0 -pix_fmt yuv420p ${file%.*}_whatsapp.mp4
