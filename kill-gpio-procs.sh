#!/usr/bin/env bash
procs=$(lsof | grep gpio-line | awk '{print $2}' | sort -u) 
if [ ! -z "$procs" ]; then
	num_proc=$(echo procs | wc -l)
	echo "$procs" | xargs -n1 kill -9
	echo "Killed $num_proc procs"
else
	echo "No procs killed"
fi
