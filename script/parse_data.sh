#!/bin/bash

if [ "$#" -ne 2 ]
then
	echo "usage: $0 start end (congresses)" >&2
	exit 1
fi

bold=`tput bold`
normal=`tput sgr0`

for c in $(seq $1 $2)
do
	X="script/parse_one.py data/$c data/$c.json"
	echo ${bold}$X${normal}
	eval $X
done
