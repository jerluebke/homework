#!/bin/bash

csplit Q-vs-L.csv /^$/ {*}

for f in $(ls xx*); do
    sed -r '/^\s*$/d' $f > ${f}.csv
    rm $f
done
