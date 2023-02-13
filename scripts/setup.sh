#!/bin/sh

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

echo "creating venv..."
if test -d .env
then echo "venv exists"
else python -m venv .env && echo "venv created"
fi

echo ''
# Activate virtual environment
echo "activating venv..."
if test -f .env/bin/activate
then . .env/bin/activate && echo "venv activate (bin)"
elif test -f .env/Scripts/activate
then . .env/Scripts/activate && echo "venv activated (Scripts)"
else exit 1
fi

echo ''
echo "installing requirements..."
if pip install -r dev-requirements.txt
then echo "requirements installed"
else exit 1
fi

echo ''
echo "setup git hooks..."
sh scripts/setup-hooks.sh
echo "git hooks setup"

exit 0
