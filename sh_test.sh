#!/usr/bin bash


#!/bin/bash
# Basic while loop
#import time

counter=1
while [ $counter -le 10 ]
do
echo $counter
((counter++))
sleep 5s
done
echo All done

# import time
#
# n_loops = 3
#
# for i in range(n_loops):
#     print(i)
#     time.sleep(5)
