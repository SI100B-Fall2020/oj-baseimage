#!/usr/bin/env python3
# Part of this file is lifted from the original judger repository.
# GeekPie and/or its affiliated parties does not claim ownership not any
# copyright over these material.
from pathlib import Path
import json
import subprocess

UNLIMITED = -1
VERSION = 0x020101

RESULT_SUCCESS = 0
RESULT_WRONG_ANSWER = -1
RESULT_CPU_TIME_LIMIT_EXCEEDED = 1
RESULT_REAL_TIME_LIMIT_EXCEEDED = 2
RESULT_MEMORY_LIMIT_EXCEEDED = 3
RESULT_RUNTIME_ERROR = 4
RESULT_SYSTEM_ERROR = 5

ERROR_INVALID_CONFIG = -1
ERROR_FORK_FAILED = -2
ERROR_PTHREAD_FAILED = -3
ERROR_WAIT_FAILED = -4
ERROR_ROOT_REQUIRED = -5
ERROR_LOAD_SECCOMP_FAILED = -6
ERROR_SETRLIMIT_FAILED = -7
ERROR_DUP2_FAILED = -8
ERROR_SETUID_FAILED = -9
ERROR_EXECVE_FAILED = -10
ERROR_SPJ_ERROR = -11


def run(max_cpu_time,
		max_real_time,
		max_memory,
		max_stack,
		max_output_size,
		max_process_number,
		exe_path,
		input_path,
		output_path,
		error_path,
		args,
		env,
		log_path,
		seccomp_rule_name,
		uid,
		gid,
		memory_limit_check_only=0):
	str_list_vars = ["args", "env"]
	int_vars = ["max_cpu_time", "max_real_time",
				"max_memory", "max_stack", "max_output_size",
				"max_process_number", "uid", "gid", "memory_limit_check_only"]
	str_vars = ["exe_path", "input_path", "output_path", "error_path", "log_path"]

	proc_args = ["/usr/lib/judger/libjudger.so"]

	for var in str_list_vars:
		value = vars()[var]
		if not isinstance(value, list):
			raise ValueError("{} must be a list".format(var))
		for item in value:
			if not isinstance(item, str):
				raise ValueError("{} item must be a string".format(var))
			proc_args.append("--{}={}".format(var, item))

	for var in int_vars:
		value = vars()[var]
		if not isinstance(value, int):
			raise ValueError("{} must be a int".format(var))
		if value != UNLIMITED:
			proc_args.append("--{}={}".format(var, value))

	for var in str_vars:
		value = vars()[var]
		if not isinstance(value, str):
			raise ValueError("{} must be a string".format(var))
		proc_args.append("--{}={}".format(var, value))

	if not isinstance(seccomp_rule_name, str) and seccomp_rule_name is not None:
		raise ValueError("seccomp_rule_name must be a string or None")
	if seccomp_rule_name:
		proc_args.append("--seccomp_rule={}".format(seccomp_rule_name))

	proc = subprocess.Popen(proc_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = proc.communicate()
	if err:
		return 0, ValueError("Error occurred while calling judger: {}".format(err))
	return json.loads(out.decode("utf-8")), 0

def mb(count):
	return count * 1024 * 1024


norm, err = run(
	16, 							# 16 sec CPU time
	16, 							# 16 src real time
	mb(256),						# 256 mem
	mb(16),							# 16 MB stack
	mb(1),							# 1MB output max
	1,								# no sub process
	"/test/executable",			# the compiled binary
	"/test/input",					# STDIN
	"/test/output",					# STDOUT
	"/dev/null",				# STDERR, discarded
	[],								# argv
	[],								# env
	"/dev/stdout",					# judger log path
	"c_cpp", 						# or general, predefined seccomp profile
	1,								# setuid 1
	1								# setgid 1
)

if err < 0:
	print(-err+100)
else:
	print(err)

