$1~/apt/ {
	print "run_cmd.py apt-get install -y -- " $2
}
$1~/pip3/ {
	print "run_cmd_no_slash.py pip3 install -- " $2
}
$1~/pip3-requirement/ {
	print "run_cmd.py pip3 install -- /submission/"
}
