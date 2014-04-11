#!/bin/bash

if [ "$#" -ne 2 ]
then
	echo "usage: $0 start end (congresses)" >&2
	exit 1
fi

bold=`tput bold`
normal=`tput sgr0`

X="script/grab_data.sh $1 $2"
echo ${bold}$X${normal}
eval $X | sed "s/^/    /"

X="script/parse_data.sh $1 $2"
echo ${bold}$X${normal}
eval $X | sed "s/^/    /"
