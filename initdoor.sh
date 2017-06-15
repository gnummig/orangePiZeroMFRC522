#!/bin/bash
### BEGIN INIT INFO
# Provides:          initscript
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Kurze Beschreibung
# Description:       Bechreibung
### END INIT INFO

exec /usr/bin/python /root/orangePiZeroMFRC522/door.py &
exit 0
