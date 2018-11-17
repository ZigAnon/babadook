#!/usr/bin/env /bin/bash

# Replace with your version
pythonVersion='python3.6'

PWD=$(pwd)
PY3=$(which $pythonVersion)
PID=`cat $PWD/../logs/main.pid`

if ! ps -p $PID > /dev/null
then
	rm $PWD/../logs/main.pid
	$PY3 $PWD/../main.py & echo $! >>$PWD/../logs/main.pid
fi
