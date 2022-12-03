#!/bin/bash
export counter=01
ls -1 | while read file; do mv "${file}" source_$(printf %03d $counter)_source.jpeg; (( counter++ )); done
#EOF
