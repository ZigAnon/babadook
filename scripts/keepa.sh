#!/usr/bin/env /bin/bash

PID=`cat /{some_folder}/your_app.pid`

if ! ps -p $PID > /dev/null
then
	rm /{some_folder}/your_app.pid
	{your_python_command} & echo $! >>/{some_folder}/your_app.pid
fi
