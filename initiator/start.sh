#!/bin/sh
cd ./initiator
sleep 5
#which python
#pip list
#ldd /usr/local/lib/libquickfix.so | grep -q libpq
echo "Start"
python main.py
