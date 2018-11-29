#!/usr/bin/env bash

# Replace with your version
pythonVersion='python3.6'

PWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PY3=$(which $pythonVersion)
PID=`cat $PWD/../logs/main.pid`
PURGE=`find $PWD/../logs/db/ -mtime +10 -type f ! -name README -delete`

echo "Checking"
echo $(date)

if ! ps -p $PID > /dev/null
then
	rm $PWD/../logs/main.pid
	cd $PWD/../
	$PY3 $PWD/main.py & echo $! >> $PWD/logs/main.pid
	echo "Restarting"
fi
