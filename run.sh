#!/bin/sh
cd ~/PycharmProjects/stocks-report || exit
source env/bin/activate
python stock_track.py --send-report -s vdy.to hdiv.to amzn vymi
