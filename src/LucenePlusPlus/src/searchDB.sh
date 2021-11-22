#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2021-11-22 01:51:54 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

KEYWORD=$1

#DB="../../../database/"
DB=$2

#cd ../build/ # relative to bash script
cd LucenePlusPlus/build/ # relative to python script

echo "Indexing database files..."
echo
./src/demo/indexfiles/indexfiles ${DB} ${DB}

echo
echo "Running search..."
echo
./src/demo/searchfiles/searchfiles -index ${DB}<<EndofSearch
$1
EndofSearch

