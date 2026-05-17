#!/bin/bash
while true; do
  git add .
  git commit -m "Auto-commit: Project implementation in progress"
  git push origin dev
  sleep 10
done
