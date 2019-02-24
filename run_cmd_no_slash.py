#!/usr/bin/env python3
import sys
import subprocess

if any(map(lambda x: '/' in x, sys.argv)):
	exit(1)

import run_cmd
