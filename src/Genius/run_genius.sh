#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2021-12-21 05:42:10 trottar"
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

echo "${CALC}"
