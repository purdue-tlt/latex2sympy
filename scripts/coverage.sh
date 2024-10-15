#!/bin/sh

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

# Activate virtual environment
echo "activating venv..."
if test -f .env/bin/activate
then . .env/bin/activate && echo "venv activate (bin)"
else exit 1
fi

# Run unit test coverage
echo "starting coverage..."
if pytest --doctest-modules --cov-report=html --cov-config=.coveragerc --cov=src tests
then echo "coverage finished"
else exit 1
fi
