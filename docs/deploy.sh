#!/bin/bash
set -e

MSG="Docs build for `git log -1 --pretty=short --abbrev-commit`"
git clone git@github.com:SDM-TIB/diefpy.git _tmp
cd _tmp
git switch gh-pages
git rm -rf --ignore-unmatch --quiet .
cp -R ../build/html/. .
touch .nojekyll
git add --all
git commit -m "$MSG"
git push origin gh-pages
cd ..
rm -rf _tmp
