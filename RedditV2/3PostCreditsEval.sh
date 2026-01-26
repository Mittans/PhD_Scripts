#!/bin/bash
#AskReddit Pressure Grade

Reddit[0]="Showerthoughts"
Reddit[1]="The_Donald"

Tab[0]="hot"
#Tab[1]="rising"

FileCommentsShowerthoughts="../${Reddit[0]}fileComments.dat"
FileCommentsThe_Donald="../DonaldfileComments.dat"
FileKarmaShowerthoughts="../${Reddit[0]}fileKarma.dat"
FileKarmaThe_Donald="../DonaldfileKarma.dat"
FileCountHotShowerthoughts="../${Reddit[0]}HotThreads.dat"
FileCountHotThe_Donald="../DonaldHotThreads.dat"


echo "$(basename `pwd`)
00:00:00" | 
  (read later_time; read former_time;
    former_seconds=$(date --date="$former_time" +%s);
    later_seconds=$(date --date="$later_time" +%s);
    echo -e -n $(((later_seconds-former_seconds)/60))'\t') | tee -a $FileCommentsShowerthoughts $FileCommentsThe_Donald $FileKarmaShowerthoughts $FileKarmaThe_Donald $FileCountHotShowerthoughts $FileCountHotThe_Donald

for i in "${Reddit[@]}"
do

    
    filename1="../$i-Newest-Boosted"
    filename2="../$i-Newest-Control"

#Contatenates ALL files starting with [subreddit]-hot into a single file called hotstuff
#find ./  -name "${Reddit[0]}-hot*" -exec cat {} \; > hotstuff

#Contatenates ALL files starting with [subreddit]-rising into a single file called risingstuff

touch $i-upVotedThreadScores.txt
touch $i-controlThreadScores.txt

    for k in "${Tab[@]}"
    
    do

        find ./  -name "$i-$k*" -exec cat {} \; > "$i-$k-stuff"

#creates a number of files we're about to write to
touch $i-countUpVoted-$k.txt
touch $i-countControl-$k.txt



varCommentPointsUp=0
varScorePointsUp=0

while read p; do 


p1=$(grep 'comments/....../' -o <<< "$p" | cut -d '/' -f 2)

#for each line in $filename1 (the boosed thread list, counts the number of times it appears in HOTSTUFF and outputs each instance to subreddit-countUpVotedHot. i.e. if the thread listed in hotstuff doesn't exist in the TOP-X number of

grep "$p1" -o "$i-$k-stuff" | wc -l | cat >> "$i-countUpVoted-$k.txt"


var1=$(grep 'comments": \(\S\+\?\)' -o "$i/$p1.txt" | head -1 | grep -Eo '[0-9]{1,}')
varCommentPointsUp=$(($var1 + $varCommentPointsUp))
var2=$(grep '"score": \(\S\+\?\)' -o "$i/$p1.txt" | head -1 | grep -Eo '[0-9]{1,}')
echo "Current points: $var2"
varScorePointsUp=$(( $var2 + $varScorePointsUp))
echo "$p comments: $var1" | cat >> $i-upVotedThreadScores.txt
echo "$p score: $var2" | cat >> $i-upVotedThreadScores.txt
echo $varCommentPointsUp
echo $varScorePointsUp

done < $filename1


echo "Total comments: $varCommentPointsUp" | cat >> $i-upVotedThreadScores.txt
echo "Total points: $varScorePointsUp" | cat >> $i-upVotedThreadScores.txt

echo -e -n "$varCommentPointsUp\t" | cat >> $(eval 'echo $FileComments'$i)
echo -e -n "$varScorePointsUp\t" | cat >> `eval 'echo $FileKarma'$i`

grep -c [^0] $i-countUpVoted-$k.txt | xargs echo "Total found: " | cat >> "$i-countUpVoted-$k.txt"
grep -c [0] $i-countUpVoted-$k.txt | xargs echo "Total not found: " | cat >> "$i-countUpVoted-$k.txt"

#add count of hot threads to the dat total
var94=$((`grep -c [^0] $i-countUpVoted-$k.txt`-2))
echo -e -n "$var94\t" | cat >> $(eval 'echo $FileCountHot'$i)

varCommentPointsControl=0
varScorePointsControl=0

while read q; do 

q1=$(grep 'comments/....../' -o <<< "$q" | cut -d '/' -f 2)


grep "$q1" -o "$i-$k-stuff" | wc -l | cat >> "$i-countControl-$k.txt"


var3=$(grep 'comments": \(\S\+\?\)' -o "$i/$q1.txt" | head -1 | grep -Eo '[0-9]{1,}')
varCommentPointsControl=$(($var3 + $varCommentPointsControl))
var4=$(grep '"score": \(\S\+\?\)' -o "$i/$q1.txt" | head -1 | grep -Eo '[0-9]{1,}')

varScorePointsControl=$(( $var4 + $varScorePointsControl))
echo "$q comments: $var3" | cat >> $i-controlThreadScores.txt
echo "$q score: $var4" | cat >> $i-controlThreadScores.txt

done < $filename2


echo "Total comments: $varCommentPointsControl" | cat >> $i-controlThreadScores.txt
echo "Total points: $varScorePointsControl" | cat >> $i-controlThreadScores.txt



grep -c [^0] $i-countControl-$k.txt | xargs echo "Total found: " | cat >> "$i-countControl-$k.txt"
grep -c [0] $i-countControl-$k.txt | xargs echo "Total not found:" | cat >> "$i-countControl-$k.txt"

var94=$((`grep -c [^0] $i-countControl-$k.txt`-2)) 
echo -e -n "$var94\n" | cat >> $(eval 'echo $FileCountHot'$i)

#Time elapsed (in mins) from 00:00:00. -> Upvoted Counts -> Control Counts

echo -e -n "$varCommentPointsControl\n" | cat >> `eval 'echo $FileComments'$i`
echo -e -n "$varScorePointsControl\n" | cat >> `eval 'echo $FileKarma'$i`

        done

    done
