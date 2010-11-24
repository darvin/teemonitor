#!/bin/sh

while [ 1 ]
do
	echo '---- CRON JOB STARTED ----'
	./bin/django refreshteeservers
	sleep 8
done
