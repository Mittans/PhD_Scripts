Reddit[0]="Showerthoughts"
Reddit[1]="The_Donald"

#!/bin/bash
DonKarma="DonaldfileKarma.dat"
DonComments="DonaldfileComments.dat"
AskRedditComments="${Reddit[0]}fileComments.dat"
AskRedditKarma="${Reddit[0]}fileKarma.dat"
AskRedditHotThreads="${Reddit[0]}HotThreads.dat"
DonHotThreads="DonaldHotThreads.dat"


currentComments=$DonComments
currentKarma=$DonKarma
currentHotCount=$DonHotThreads

gnuplot -e "set ylabel 'Comments'; set xlabel 'Elapsed Time (minutes)'; set xrange[0:1410];  plot '$currentComments' using (\$1):(\$2) title 'Comments Boosted' with lines, \
'$currentComments' using (\$1):(\$3) title 'Comments Control' with lines; set terminal png; set output 'DonCommentsImage.png'; replot;"

gnuplot -e "set ylabel 'Karma'; set xlabel 'Elapsed Time (minutes)'; set xrange[0:1410]; plot '$currentKarma' using 1:2 title 'Karma Boosted' with lines, \
'$currentKarma' using 1:3 title 'Karma Control' with lines; set terminal png; set output 'DonKarmaImage.png'; replot;"

gnuplot -e "set ylabel 'Hot Threads'; set yrange [0:10]; set xlabel 'Elapsed Time (minutes)'; set xrange[0:1410]; plot '$currentHotCount' using 1:2 title 'Hot Threads Boosted' with lines, \
'$currentHotCount' using 1:3 title 'Hot Threads Control' with lines; set terminal png; set output 'DonHotThreadsImage.png'; replot;"

currentComments=$AskRedditComments
currentKarma=$AskRedditKarma
currentHotCount=$AskRedditHotThreads

gnuplot -e "set ylabel 'Comments'; set xlabel 'Elapsed Time (minutes)'; set xrange[0:1410]; plot '$currentComments' using (\$1):(\$2) title 'Comments Boosted' with lines, \
'$currentComments' using (\$1):(\$3) title 'Comments Control' with lines; set terminal png; set output '${Reddit[0]}CommentsImage.png'; replot;"

gnuplot -e "set ylabel 'Karma'; set xlabel 'Elapsed Time (minutes)'; set xrange[0:1410]; plot '$currentKarma' using 1:2 title 'Karma Boosted' with lines, \
'$currentKarma' using 1:3 title 'Karma Control' with lines; set terminal png; set output '${Reddit[0]}KarmaImage.png'; replot;"

gnuplot -e "set ylabel 'Hot Threads'; set yrange [0:10]; set xlabel 'Elapsed Time (minutes)'; set xrange[0:1410]; plot '$currentHotCount' using 1:2 title 'Hot Threads Boosted' with lines, \
'$currentHotCount' using 1:3 title 'Hot Threads Control' with lines; set terminal png; set output '${Reddit[0]}HotThreadsImage.png'; replot;"
