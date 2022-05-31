#!/bin/bash
# Make sure that the `pre-commit` and `flake8` packages are already
# installed in the running environment.

pre-commit run -a

if test $? -eq 0 # Check status code of last command
then
  # if the last command was success, try the next one
  flake8 .
else
  exit 1
fi
