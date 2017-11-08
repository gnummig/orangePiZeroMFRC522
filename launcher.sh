#!/bin/sh
# launches the doorscript

cd /root/orangePiZeroMFRC522/
while true; do 
	killall python 
	python door.py
done

