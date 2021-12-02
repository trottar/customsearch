#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2021-12-02 00:45:26 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

INPUT=$1

CALC=$(genius<<EndofGenius
${INPUT}
EndofGenius
)

echo
echo "${INPUT} is equal to..."
echo 
echo "${CALC}"
