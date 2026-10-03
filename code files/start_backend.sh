#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -x "venv/bin/python" ]; then
  echo "Virtual environment not found. Run: python3 -m venv venv && venv/bin/pip install -r requirements.txt"
  exit 1
fi
exec venv/bin/python -m uvicorn main:app --reload
