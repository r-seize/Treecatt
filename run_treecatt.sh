#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH}"

# Remove Python warnings (production mode)
export PYTHONWARNINGS="ignore"

# OR redirect to a log file (debug mode)
# python3 -m treecatt.main "$@" 2>"${SCRIPT_DIR}/dev.log"

# Production mode (without warnings)
python3 -m treecatt.main "$@" 2>/dev/null

# Dev mode (keep actual errors but not warnings)
# python3 -W ignore::RuntimeWarning -m treecatt.main "$@"