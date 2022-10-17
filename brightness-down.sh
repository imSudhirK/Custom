#!/bin/bash

OpSys=$(xrandr | grep " connected" | cut -f1 -d " ")

val=$(</home/sudhir/Custom/brightness-counter.txt)
val=$(printf %.1f $(echo "$val-0.1" | bc -l));

xrandr --output $OpSys --brightness $val

echo "$val" > "/home/sudhir/Custom/brightness-counter.txt"
