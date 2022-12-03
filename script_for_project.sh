#!/bin/bash
export file="project.mp4"
if [[ -n $1 ]]; then
  outputFile=$1
else
#  outputFile=$(date +%Y.%m.%d.mp4)
   outputFile="$(basename ${PWD}).mp4"
fi
echo "Output file is ${outputFile}"
ffpb -i ${file} -c:v libx265 -crf 26 -preset fast -c:a aac -b:a 128k $outputFile
