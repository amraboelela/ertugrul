#!/bin/bash

cd "$(dirname "$0")/.."
python3 scripts/build.py ertugrul 1 $1 $2 $3 $4
