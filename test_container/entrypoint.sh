#!/bin/bash

# Erwartet: /app/user_script.py existiert
echo "Running user script tests..."

pytest tests/test_user_script.py --tb=short --maxfail=1 --disable-warnings --json-report --json-report-file=report.json

exit $?