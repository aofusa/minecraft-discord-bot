#! /bin/bash

echo "[$(date)] register cron */5 * * * * /home/minecraft/observer.sh"
(crontab -l | grep -v -F "/home/minecraft/observer.sh" ; echo "*/5 * * * * /home/minecraft/observer.sh >> /var/log/minecraft-observer.log 2>&1")| crontab -

