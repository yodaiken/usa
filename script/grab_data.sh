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
	X="rsync -avz --delete --delete-excluded --exclude **/text-versions/ \
				govtrack.us::govtrackdata/congress/$c/bills data/$c"
	echo ${bold}$X${normal}
	eval $X
	X="rsync -avz --delete --delete-excluded --exclude **/text-versions/ \
				govtrack.us::govtrackdata/congress/$c/votes data/$c"
	echo ${bold}$X${normal}
	eval $X
done
