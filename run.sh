#!/bin/sh
cd ~/projects/stocks-report
source env/bin/activate
python stock_track.py -s hsbc amzn vymi
