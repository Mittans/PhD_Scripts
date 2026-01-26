#!/bin/bash

#This file saves the json data from the rising and hot tabs of Reddit for the specificed Subreddits
#This file is the first step of a two step process
#This step collects the threads in the Rising and Hot tabs of Reddit
#This second step (another file) compares the 

cd "$(dirname "$0")";

curDir=$(pwd)

filename='file'
STR66=$(date '+%X')
mkdir "$curDir/$STR66"

STR=$"rising$(date '+%X')"
STR1=$"hot$(date '+%X')"

Reddit[0]="Showerthoughts"
Reddit[1]="The_Donald"
#Subreddits go HERE
NumPages=3
#number of pages to consider "relevant". 3's probably a good number

Tab[0]="hot"
#Tab[1]="rising"

#Get top X pages of the Rising & Hot Subreddit

for i in "${Reddit[@]}"
do
    mkdir "$curDir/$STR66/$i"

    for k in "${Tab[@]}"
    
    do
    
        wget "https://www.reddit.com/r/$i/$k/.json" -O "$curDir/$STR66/$i-$k-page0.txt"
PIPE=$(grep -o 'after\": \".........' "$curDir/$STR66/$i-$k-page0.txt" | grep -o ".........$")

        for ((j=1;j<NumPages;j++))

        do
    
            wget "https://www.reddit.com/r/$i/$k/.json?count=$[25*j]&after=$PIPE" -O "$curDir/$STR66/$i-$k-page$j.txt"
PIPE=$(grep -o 'after\": \".........' "$curDir/$STR66/$i-$k-page$j.txt" | grep -o ".........$")

        done

    done
    
    
echo Start
while read p; do 
STR19=$(echo $p | tr '\\' ' ' | grep -o "comments/......" | grep -o "......$")
wget "$p.json" -O "$curDir/$STR66/$i/$STR19.txt"
echo $p
done < "$curDir/$i-Newest-0"   
        
done

cp ./3PostCreditsEval.sh "$curDir/$STR66"/3PostCreditsEval1.sh
cd "$curDir/$STR66/"
bash ./3PostCreditsEval1.sh

