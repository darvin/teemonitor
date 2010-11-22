#!/bin/sh

while [ 1 ]
do
	echo '---- CRON JOB STARTED ----'
	./manage.py refreshteeservers
	sleep 8
done
