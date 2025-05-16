#!/bin/bash

with_Am_Pm=$(date +%r)

echo "$with_Am_Pm - Starting media request script"

cd /home/vanchondo/requestMedia

python3 requestMedia.py

wait

with_Am_Pm=$(date +%r)

echo "$with_Am_Pm - All media request completed"