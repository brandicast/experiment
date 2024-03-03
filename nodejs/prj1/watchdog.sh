#!/bin/bash

if pgrep -x "node" 
then
	echo "gateway is running !"
else

	echo "gateway is stopped !"
	cd /home/brandon/Dropbox/workbench/nodejs/prj1/
        ./gateway.sh
fi
