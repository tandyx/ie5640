#!/bin/bash


if [ -z "$1" ]
  then
    echo "No notebook name supplied (without extension)"
    exit 1
fi

source .venv/bin/activate
black --line-length 80 "$1.ipynb"
jupyter nbconvert --to qtpdf "$1.ipynb"
mkdir -p exports
mv "$1.pdf" exports/
echo "Exported $1.ipynb to exports/$1.pdf"
kde-open "exports/$1.pdf"

