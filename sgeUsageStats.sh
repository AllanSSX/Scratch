#!/bin/bash

qacct -b 201101010000 -o |grep -v "====" | egrep -v "^ren|^ops|^dte" | sed -e 's/\./,/g' | perl -p -e 's/\x20+/\;/g' > acces-cluster-2011-2012.csv
