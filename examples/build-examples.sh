#!/bin/bash
cd `dirname $0`

set -e

EXAMPLES=("bigdemo" "hello-world" "page_numbers")

for example in "${EXAMPLES[@]}"; do
  pushd "$example" && python3 "$example".py && popd || exit 1
done
