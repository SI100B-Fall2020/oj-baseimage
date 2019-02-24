#!/usr/bin/env bash

function stage () {
	echo "@logseg $1"
	echo "@logseg $1" 1>&2
}

function exit_trap () {
	exit 0 #$1
}
if [ "setup" == "$1" ] || [ -z "$1" ] ; then
if [ -f /submission/dependencies ] ; then 
	stage dep
	cd /judge
	awk -F: -f dep.awk /submission/dependencies | xargs -r -L 1 sh -c 'python3 $0 $@ || exit 255' || exit_trap 7
fi

cd /submission/
stage build
gcc -O2 -w -fmax-errors=3 -std=c11 /submission/main.c -lm -o /test/executable || exit_trap 6

fi

if [ "run" == "$1" ] || [ -z "$1" ] ; then
cd /judge

stage run
./run.py || exit_trap $?
fi

if [ "grade" == "$1" ] || [ -z "$1" ] ; then
stage grade
grade/grade.py < /test/output || exit_trap 0 # 0 score on grading script error
fi

