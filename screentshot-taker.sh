#!/bin/bash

typeset -i val=$(</home/sudhir/Custom/screentshot-counter.txt)

ss_dir="/home/sudhir/Pictures/screenShot"
if [ ! -d "$ss_dir" ]; then
  mkdir $ss_dir
fi

import -window root "/home/sudhir/Pictures/screenShot/img${val}.png"

val=$((val+1))
echo "$val" > "/home/sudhir/Custom/screentshot-counter.txt"