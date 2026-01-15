#!/bin/sh
#Setup
#Make sure this file is chmod +X'd
#Make sure this file is crontab'd to run at midnight every night
#make sure the cron daemon is running!
#test via ps ax | grep cron, service cron start, etc.
#You can add this file to cron via crontab -e to edit, then appending 0 0 * * * /usr/bin/sh /absolute/path/to/1GrapNewSubmissions.sh
start_index=1
start_index_str=$(printf "%02d" $start_index)
#Search through Experiment folders, e.g. Experiment-01 and create the next folder in sequence, e.g. Experiment-02.
while [ -d 'Experiment-'$start_index_str ];
do
	start_index=$((start_index+1));
	start_index_str=$(printf "%02d" $start_index)
done
#Once we've made a folder, cd into it
#pwd will be location of 1GrapNewSubmissions.sh/Experiment-NN
mkdir -p -- 'Experiment-'$start_index_str
cd 'Experiment-'$start_index_str
#Use wget2 to get newest Reddit submission in JSON format. Use wget2 because regular wget has https problems and gets a 403 error
#Dump it to Showerthoughts.json
wget2 -O Showerthoughts.json "https://www.reddit.com/r/Showerthoughts/new/.json"
#Use jq library to parse json data. Make sure you have the dependency installed. eg. apt install jq
#jq itself is written in C and has no runtime dependencies https://github.com/jqlang/jq
#jq replaces some dreadful regex
cat Showerthoughts.json | jq -r '.data.children[].data.permalink' > "Showerthoughts-Newest-0"
#Use sed to prefix Reddit url to the permalink field (i.e. turn /r/Showerthoughts/comments/... into https://www.reddit.com/r/Showerthoughts/comments/...
#We need the full url to feed to the upvoting service
sed -i -e 's/^/https:\/\/www.reddit.com/' "Showerthoughts-Newest-0"
#Now, grab top 20 most recent threads from the list
#Pipe
#Randomise the order of the 20 submission links
#Pipe
#Split the randomised list into 10 line chunks. Read from '-' or Stdin, use 'Showerthoughts' prefix and decimal (-d) suffixes
#Will produce two files, Showerthoughts00, Showerthoughts01
head -n 20 Showerthoughts-Newest-0 | shuf -n 20 | split -l 10 -d - 'Showerthoughts'
#Rename them to Control and Boosted
mv 'Showerthoughts00' 'Showerthoughts-Newest-Control'
mv 'Showerthoughts01' 'Showerthoughts-Newest-Boosted'
#Copy in the other scripts from the ../pwd directory. We'll need these to setup crontab and schedule the scrapes
#Make sure all the files are chmod +X'd before copying them around
cp "../2HourlyScrape.sh" "./2HourlyScrape.sh"
cp "../3PostCreditsEval.sh" "./3PostCreditsEval.sh"
cp "../4AfterScoreGraph.sh" "./4AfterScoreGraph.sh"
#Dump current cronjob to a file, we're going to be appending our job to it.
#This step is important, because this file should also stay crontab'd to run once per day at midnight
crontab -l > cronjob
#Schedule cronjobs every 5 minutes for the first couple of hours (should be 0, 1), then every 15 minutes until the end of the day
#There's some ugly syntax with the $(( Dollar Double Parentheses )) , but what can you do
#Use date syntax in the cronjob so the data collection only happens today (start at midnight, stop after 24 hours)
#If you want to start at *not* midnight, you'll have to do some extra work so the cronjob continues into the next day. Enjoy.
echo "*/5 $(date +%H) $(date +%d) $(date +%m) * /usr/bin/sh $(pwd)/2HourlyScrape.sh" >> cronjob
echo "*/5 $(($(date +%H)+1)) $(date +%d) $(date +%m) * /usr/bin/sh $(pwd)/2HourlyScrape.sh" >> cronjob
echo "*/15 $(($(date +%H)+2))-23 $(date +%d) $(date +%m) * /usr/bin/sh $(pwd)/2HourlyScrape.sh" >> cronjob
crontab cronjob
rm cronjob
#For each line of the Boosted thread, create an upvoting service job to upvote it
#Vote's is 10
#Link is the current line of the Boosted file
#After is 0 (do votes straight away)
#Speed is 10 votes per minute
#Make sure your $TOKEN_ENV_VAR is set prior to sending the jobs off!!
while read -r line
do
	curl -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN_ENV_VAR" -d "{'link':$line, 'type': 1, 'vote': 10, 'after': 0, 'speed': 10}" -X POST "https://upvote.club/api/order/create"
	echo "Sent off $line to upvote service"
done < "Showerthoughts-Newest-Boosted"
#Now that Showerthoughts has been scraped, sorted into groups, and copied into the Experiment folder
#Do the same thing with The_Donald
#We could do this as port of a loop to reduce copy / pasting code, but, eh, there's only 2 of 'em
#Use wget2 to get newest Reddit submission in JSON format. Use wget2 because regular wget has https problems and gets a 403 error
#Dump it to The_Donald.json
wget2 -O The_Donald.json "https://www.reddit.com/r/the_donald/new/.json"
#Use jq library to parse json data. Make sure you have the dependency installed. eg. apt install jq
#jq itself is written in C and has no runtime dependencies https://github.com/jqlang/jq
#jq replaces some dreadful regex
cat The_Donald.json | jq -r '.data.children[].data.permalink' > "The_Donald-Newest-0"
#Use sed to prefix Reddit url to the permalink field (i.e. turn /r/The_Donald/comments/... into https://www.reddit.com/r/The_Donald/comments/...
#We need the full url to feed to the upvoting service
sed -i -e 's/^/https:\/\/www.reddit.com/' "The_Donald-Newest-0"
#Now, grab top 20 most recent threads from the list
#Pipe
#Randomise the order of the 20 submission links
#Pipe
#Split the randomised list into 10 line chunks. Read from '-' or Stdin, use 'The_Donald' prefix and decimal (-d) suffixes
#Will produce two files, The_Donald00, The_Donald01
head -n 20 The_Donald-Newest-0 | shuf -n 20 | split -l 10 -d - 'The_Donald'
#Rename them to Control and Boosted
mv 'The_Donald00' 'The_Donald-Newest-Control'
mv 'The_Donald01' 'The_Donald-Newest-Boosted'
#Cronjob's already scheduled, and shell scripts already copied, so let's move to upvoting The_Donald submissions.
#For each line of the Boosted thread, create an upvoting service job to upvote it
#Vote's is 10
#Link is the current line of the Boosted file
#After is 0 (do votes straight away)
#Speed is 10 votes per minute
#Make sure your $TOKEN_ENV_VAR is set prior to sending the jobs off!!
while read -r line
do
	curl -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN_ENV_VAR" -d "{'link':$line, 'type': 1, 'vote': 10, 'after': 0, 'speed': 10}" -X POST "https://upvote.club/api/order/create"
	echo "Sent off $line to upvote service"
done < "The_Donald-Newest-Boosted"
#After upvoting Showerthoughts and The_Donald, copying the scrips, and scheduling the cronjobs, we're all done.
