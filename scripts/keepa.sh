#!/usr/bin/env bash

# Replace with your version
pythonVersion="python3.6"

PWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PY3=$(which $pythonVersion)
PID=`cat $PWD/../logs/main.pid`
PURGE=rm $(find /home/zb/zigbot/logs/db/ -mtime +2 -type f ! -name \*.roles | grep -v 'README\|*.mute\|*.roles\|*.html')

echo "Checking"
echo $(date)

if ! ps -p $PID > /dev/null
then
	rm $PWD/../logs/main.pid
	cd $PWD/../
	$PY3 $PWD/main.py & echo $! >> $PWD/logs/main.pid
	echo "Restarting"
fi
