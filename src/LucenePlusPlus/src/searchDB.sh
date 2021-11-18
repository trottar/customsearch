#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2021-11-18 10:17:08 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

KEYWORD=$1

DB="../../../database/"

cd ../build/

echo "Indexing database files..."
echo
./src/demo/indexfiles/indexfiles ${DB} ${DB}

echo
echo "Running search..."
echo
./src/demo/searchfiles/searchfiles -index ${DB}<<EndofSearch
$1
EndofSearch
