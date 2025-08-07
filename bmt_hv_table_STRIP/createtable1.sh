#!/bin/bash

while read -r line; 
do 
    python3 ./writeTables1.py $line $1; 
done < changes.txt
