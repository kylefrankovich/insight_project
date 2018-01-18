#!/usr/bin bash

counter=1
while [ $counter -le 30 ]
do
instagram-scraper tattoo --tag --maximum 100 --media-types image --destination ${HOME}/Desktop/insight_training_data --include-location
((counter++))
sleep 10m # wait 15 minutes between scrapes
done
echo All done
