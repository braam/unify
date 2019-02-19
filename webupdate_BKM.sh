#!/usr/bin/env bash

URL="https://webupdate.bkm.be/Hotfix"
USER="bhav@hexacom.be"
LIST="osbiz_names.txt"

#Change working directory
cd /home/braam/_BKM_/update_server/Hotfix
#ask password without echo back
echo -n Enter Password "for $USER:" 
read -s password

#Grep osbiz_ file names from html, remove first ">" char.
wget --user=$USER --password=$password -O - $URL | grep -Eo ">osbiz_?\S+?\.tar" | cut -c 2- > $LIST
sleep 1
#Check if file not exists, then start download.
while read f; do 
    if [ ! -f "$f" ]; then
        wget --user=$USER --password=$password $URL/$f
    else
        echo $f : OK
    fi
done < $LIST

# cleanup
rm $LIST

#Download all osbiz tar files.
#wget --user=$USER --password=$password -c -r -l1 -np -A 'osbiz_*.tar' -P /home/braam/Desktop -E $URL
