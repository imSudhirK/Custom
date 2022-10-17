#!/bin/bash

# file number 
num=1

# directory to be renamed should not be empty
if [ ! -n "$1" ]
then
	echo "Error: wrong set arguments provided"
	echo "usage: $0   <files_dir>"
	echo "usage: $0   <files_dir>   <prefix>"
	echo "usage: $0   <files_dir>   <prefix>   <extension>"

# directory to be renamed should exists
elif [ ! -d "$1" ]
then
	echo "Error: file_dir <$1> doesn't exists"

# lets rename files
else
	for file in $1/*
	do
		# check extension of each file
		ext=$([[ "$file" = *.* ]] && echo ".${file##*.}" || echo '')
		# if extension is given in argument reset it
		if [ -n "$3" ]
		then
			ext=.$3
		fi

		# if new_name file already exit, increment counter
		while [ -f "$1/$2$num$ext" ]
		do
			num=$((num+1))
		done

		#finally rename apart
		mv $file $1/$2$num$ext
		num=$((num+1))
	done
fi


