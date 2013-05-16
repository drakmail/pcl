#!/bin/bash

# WSGI mode launcher. Launching wsgi.py in screen, restart it,
# kill it.

PID=""
SCREEN_NAME="pcl-wsgi-mode"

function get_pid {
   PID=`screen -list | grep ${SCREEN_NAME} | cut -f1 -d'.' | sed 's/\W//g'`
}

function stop {
   get_pid
   if [ -z $PID ]; then
      echo "PCL is not running"
      exit 1
   else
      echo "Stopping PCL WSGI server..."
      kill $PID
      screen -wipe > /dev/null
      sleep 1
      echo "PCL WSGI server stopped."
   fi
}

function start {
   get_pid
   if [ -z $PID ]; then
      echo "Starting PCL WSGI server..."
      screen -d -m -S ${SCREEN_NAME} ./wsgi.py
      get_pid
      echo "PCL WSGI server started with PID $PID."
   else
      echo "PCL WSGI server is already running with pid PID=$PID"
   fi
}

function restart {
   echo  "Restarting PCL WSGI server..."
   get_pid
   if [ -z $PID ]; then
      start
   else
      stop
      start
   fi
}


function status {
   get_pid
   if [ -z  $PID ]; then
      echo "PCL WSGI server is not running."
      exit 1
   else
      echo "PCL WSGI server is running with PID $PID"
   fi
}

case "$1" in
   start)
      start
   ;;
   stop)
      stop
   ;;
   restart)
      restart
   ;;
   status)
      status
   ;;
   *)
      echo "Usage: $0 {start|stop|restart|status}"
esac