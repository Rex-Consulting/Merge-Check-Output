#!/usr/bin/python
#
# rex_merge_check.py
# 1/10/2018
#
# Description: Runs and merges multiple checks together and does an operation on the results
#
# Jeremy Diaz
# Copyright 2018, Rex Consulting., ALL RIGHTS RESERVED
#
import sys
import os
import argparse
import re

parser = argparse.ArgumentParser(description='Merges multiple checks')
parser.add_argument('--output1', '-o1', required=True, help='first check output to parse')
parser.add_argument('--output2', '-o2', required=True, help='second check output to parse')
parser.add_argument('--reg1', '-r1', required=True, help='regex for output1, needs to contain 1 capture group with a value')
parser.add_argument('--reg2', '-r2', required=True, help='regex for output2, needs to contain 1 capture group with a value')
parser.add_argument('--operation', '-op', required=True, help='operating to perform on captured values, supported: add (a)')
parser.add_argument('--message', '-mm', required=False, help='optional message, can be formatted by placing {0} (index needs to be included inside curly braces) which will be substituted for the value')
parser.add_argument('--warning', '-w', required=False, help='Optional warning threshold')
parser.add_argument('--critical', '-c', required=False, help='Optional critical threshold')

parser.set_defaults(debug=False)
args = parser.parse_args()

# Parse the outputs using regex capture groups
if args.reg1:
    captured_1 = re.findall(args.reg1, args.output1)[0]
if args.reg2:
    captured_2 = re.findall(args.reg2, args.output2)[0]

# Convert captured values to operation types
if captured_1:
    res_1 = float(captured_1)
if captured_2:
    res_2 = float(captured_2)

basic_output = "{0}"
if args.message:
    basic_output = args.message

arg_flag = False
# Perform operation and output value
if args.operation:
    if args.operation == "a":
        arg_flag = True
        result = res_1 + res_2
        print basic_output.format(str(res_1 + res_2))

if arg_flag and args.warning and args.critical:
    warning = float(args.warning)
    critical = float(args.critical)

    if result > critical:
        print "CRITICAL - " + basic_output.format(str(result)) + " | result=" + str(result) + ";" + args.warning + ";" + args.critical + ";;"
        sys.exit(2)
    elif result > warning:
        print "WARNING - " + basic_output.format(str(result)) + " | result=" + str(result) + ";" + args.warning + ";" + args.critical + ";;"
        sys.exit(1)
    else: 
        print "OK - " + basic_output.format(str(result)) + " | result=" + str(result) + ";" + args.warning + ";" + args.critical + ";;"
        sys.exit(0)
else:
    if arg_flag:
        print "OK - " + basic_output.format(str(result)) + " | result=" + str(result)
        sys.exit(0)
    else:
        print "UNKNOWN - Unable to read output"
        sys.exit(3)

