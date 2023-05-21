#!/bin/bash

if [ $# -lt 2 ]; then
  echo "Usage: $0 <source_file> <output_name>"
  exit 1
fi

if [ ! -f $1 ]; then
  echo "Error: $1 does not exist"
  exit 1
fi

SOURCE=$1
BASENAME=$(basename $SOURCE .cpp)
OUTPUT=$2

g++ $SOURCE utils.cpp -o $OUTPUT -lcrypto -std=c++2a

if [ $? -ne 0 ]; then
  echo "Error: compilation failed"
  exit 1
fi