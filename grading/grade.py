#!/usr/bin/env python3
# Somehow grade the output based on something.
# This example script do a string compare using `diff -daZB` on each
# test output and reference output.

# YOU CAN CHANGE THIS SCRIPT HOWEVER YOU WANT PROVIDED YOU DON'T PRINT TO CONSOLE
# AND USING SUPPLIED Judging() TO REPORT STUDENT SCORES
# unless you know what you are doing.

from utils import *
from sys import argv
from pathlib import Path
with Judging() as e:
	for i in range(0, int(argv[1]) + 1):
		# We do not catch any exceptions, because there is few reasonable
		# way to deal with it.
		# Better pop it up out to the frontend.
		err_path = "/judge/output/err{}".format(i)
		if Path(err_path).exists():
			t = open(err_path)
			# Please consult /run.py on what this err can be
			err=int(t.read().strip(" \n\r"))
			t.close()
			# This will declare a testcase that worth 1 point, but the student's program errored for some reason.
			# Unless you made a drastical change like change to use Java, you aren't too likely to change this part.
			e.add_errored_testcase(err,1)
		else:
			passed = compare_file("/test/{}".format(i), "/judge/tests/output/{}".format(i))
			# If your test case is simple passed/failed, use add_boolean_testcase
			# This will declare a testcase that worth 1 point.
			# If you want to make it more than 1 point, or want to award partial success, 
			# e.g. give 1 point for a 2 points testcase, use e.add_scored_testcase
			# For demonstration purpose, we don't use add_boolean_testcase here, but it is 
			# 100% valid to use it here.
			# e.add_boolean_testcase(passed)
			e.add_scored_testcase(10 if passed else 0, 10)
