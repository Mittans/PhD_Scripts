#!/bin/bash
cd "~/RedditExperimentsPt2/"
touch DonCommentsInit.dat
touch DonKarmaInit.dat
touch ShowerCommentsInit.dat
touch ShowerKarmaInit.dat
touch DonCommentsFinal.dat
touch DonKarmaFinal.dat
touch ShowerCommentsFinal.dat
touch ShowerKarmaFinal.dat

touch AvgShowerThoughtsKarma.dat
touch AvgDonaldKarma.dat
touch AvgShowerThoughtsComments.dat
touch AvgDonaldComments.dat

InitCommentsShower=~/RedditExperimentsPt2/ShowerCommentsInit.dat
InitCommentsDon=~/RedditExperimentsPt2/DonCommentsInit.dat
InitKarmaShower=~/RedditExperimentsPt2/ShowerKarmaInit.dat
InitKarmaDon=~/RedditExperimentsPt2/DonKarmaInit.dat

FinalCommentsShower=~/RedditExperimentsPt2/ShowerCommentsFinal.dat
FinalCommentsDon=~/RedditExperimentsPt2/DonCommentsFinal.dat
FinalKarmaShower=~/RedditExperimentsPt2/ShowerKarmaFinal.dat
FinalKarmaDon=~/RedditExperimentsPt2/DonKarmaFinal.dat

test1=~/RedditExperimentsPt2/AvgShowerThoughtsKarma.dat
test2=~/RedditExperimentsPt2/AvgDonaldKarma.dat

test3=~/RedditExperimentsPt2/AvgShowerThoughtsComments.dat
test4=~/RedditExperimentsPt2/AvgDonaldComments.dat

test5=~/RedditExperimentsPt2/AvgShowerThoughtsHot.dat
test6=~/RedditExperimentsPt2/AvgDonHot.dat

Reddit[0]="Showerthoughts"
Reddit[1]="Donald"

#minutes in
#f2 uvote
#f3 contro

for i in {01..31}
do
    cd "~/RedditExperimentsPt2/E$i"
    echo "$i\t" | tee -a  $InitCommentsShower $InitCommentsDon $InitKarmaShower $InitKarmaDon $FinalCommentsShower $FinalCommentsDon $FinalKarmaShower $FinalKarmaDon
    
    sed -n 3p DonaldfileComments.dat | cut -f2 -z >> $InitCommentsDon
    echo -e -n "\t" >> $InitCommentsDon
    sed -n 3p DonaldfileComments.dat | cut -f3 -z >> $InitCommentsDon
    echo -e -n "\n" >> $InitCommentsDon
    
    sed -n 114p DonaldfileComments.dat | cut -f2 -z >> $FinalCommentsDon
    echo -e -n "\t" >> $FinalCommentsDon
    sed -n 114p DonaldfileComments.dat | cut -f3 -z >> $FinalCommentsDon
    echo -e -n "\n" >> $FinalCommentsDon
    
    sed -n 3p DonaldfileKarma.dat | cut -f2 -z >> $InitKarmaDon
    echo -e -n "\t" >> $InitKarmaDon
    sed -n 3p DonaldfileKarma.dat | cut -f3 -z >> $InitKarmaDon
    echo -e -n "\n" >> $InitKarmaDon
    
    sed -n 114p DonaldfileKarma.dat | cut -f2 -z >> $FinalKarmaDon
    echo -e -n "\t" >> $FinalKarmaDon
    sed -n 114p DonaldfileKarma.dat | cut -f3 -z >> $FinalKarmaDon
    echo -e -n "\n" >> $FinalKarmaDon
    
    
    
    sed -n 3p ShowerthoughtsfileComments.dat | cut -f2 -z >> $InitCommentsShower
    echo -e -n "\t" >> $InitCommentsShower
    sed -n 3p ShowerthoughtsfileComments.dat | cut -f3 -z >> $InitCommentsShower
    echo -e -n "\n" >> $InitCommentsShower
    
    sed -n 114p ShowerthoughtsfileComments.dat | cut -f2 -z >> $FinalCommentsShower
    echo -e -n"\t" >> $FinalCommentsShower
    sed -e -n 114p ShowerthoughtsfileComments.dat | cut -f3 -z >> $FinalCommentsShower
    echo -e  -n "\n" >> $FinalCommentsShower
    
    sed -n 3p ShowerthoughtsfileKarma.dat | cut -f2 -z >> $InitKarmaShower
    echo -e -n "\t" >> $InitKarmaShower
    sed -n 3p ShowerthoughtsfileKarma.dat | cut -f3 -z >> $InitKarmaShower
    echo -e -n "\n" >> $InitKarmaShower
    
    sed -n 114p ShowerthoughtsfileKarma.dat | cut -f2 -z >> $FinalKarmaShower
    echo -e -n "\t" >> $FinalKarmaShower
    sed -n 114p ShowerthoughtsfileKarma.dat | cut -f3 -z >> $FinalKarmaShower
    echo -e -n "\n" >> $FinalKarmaShower
done

for j in {3..114}
do
    echo -e -n "OBSERVATION $j / 111 \n" >> $test1
    for k in {01..31}
    do
        cd ~/RedditExperimentsPt2/E$k
        sed -n ${j}p ShowerthoughtsfileKarma.dat | cut -f2 -z | tr -d $'\n' >> $test1
        echo -e -n "\t" >> $test1
        sed -n ${j}p ShowerthoughtsfileKarma.dat | cut -f3 -z | tr -d $'\n' >> $test1
        echo -e -n "\n" >> $test1
    done
    echo -e -n "\n" >> $test1
done

for j in {3..114}
do
    echo -e -n "OBSERVATION $j / 111 \n" >> $test3
    for k in {01..31}
    do
        cd ~/RedditExperimentsPt2/E$k
        sed -n ${j}p ShowerthoughtsfileComments.dat | cut -f2 -z | tr -d $'\n' >> $test3
        echo -e -n "\t" >> $test3
        sed -n ${j}p ShowerthoughtsfileComments.dat | cut -f3 -z | tr -d $'\n' >> $test3
        echo -e -n "\n" >> $test3
    done
    echo -e -n "\n" >> $test3
done

for j in {3..114}
do
    echo -e -n "OBSERVATION $j / 111 \n" >> $test2
    for k in {01..31}
    do
        cd ~/RedditExperimentsPt2/E$k
        sed -n ${j}p DonaldfileKarma.dat | cut -f2 -z | tr -d $'\n' >> $test2
        echo -e -n "\t" >> $test2
        sed -n ${j}p DonaldfileKarma.dat | cut -f3 -z | tr -d $'\n' >> $test2
        echo -e -n "\n" >> $test2
    done
    echo -e -n "\n" >> $test2
done


for j in {3..114}
do
    echo -e -n "OBSERVATION $j / 111 \n" >> $test4
    for k in {01..31}
    do
        cd ~/RedditExperimentsPt2/E$k
        sed -n ${j}p DonaldfileComments.dat | cut -f2 -z | tr -d $'\n' >> $test4
        echo -e -n "\t" >> $test4
        sed -n ${j}p DonaldfileComments.dat | cut -f3 -z | tr -d $'\n' >> $test4
        echo -e -n "\n" >> $test4
    done
    echo -e -n "\n" >> $test4
done
        
    #Upvoted --> NonUpvoted

for j in {3..114}
do
    echo -e -n "OBSERVATION $j / 111 \n" >> $test5
    for k in {01..31}
    do
        cd ~/RedditExperimentsPt2/E$k
        sed -n ${j}p ShowerthoughtsHotThreads.dat | cut -f2 -z | tr -d $'\n' >> $test5
        echo -e -n "\t" >> $test5
        sed -n ${j}p ShowerthoughtsHotThreads.dat | cut -f3 -z | tr -d $'\n' >> $test5
        echo -e -n "\n" >> $test5
    done
    echo -e -n "\n" >> $test5
done
    
for j in {3..114}
do
    echo -e -n "OBSERVATION $j / 111 \n" >> $test6
    for k in {01..31}
    do
        cd ~/RedditExperimentsPt2/E$k
        sed -n ${j}p DonaldHotThreads.dat | cut -f2 -z | tr -d $'\n' >> $test6
        echo -e -n "\t" >> $test6
        sed -n ${j}p DonaldHotThreads.dat | cut -f3 -z | tr -d $'\n' >> $test6
        echo -e -n "\n" >> $test6
    done
    echo -e -n "\n" >> $test6
done
    
    
    
    
