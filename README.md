# Merge-Check-Output
Custom check for Nagios that performs an operation on 2 different check outputs using macros

## Arguments

    —output1/-o1 : first check output to parse, should be substituted with a macro
    —output2/-o2 : second check output to parse, should be substituted with a macro
	—reg1/-r1 : regex for output1, needs to contain 1 capture group with a value
	—reg2/-r2 : regex for output2, needs to contain 1 capture group with a value
	—operation/-op : operating to perform on captured values, supported: add (a)
	—message/-mm : optional message, can be formatted by placing {0} (index needs to be included inside curly braces) which will be substituted for the value
  
## Examples

    ./rex_merge_check.py -o1 "OK - load average: 1.50, 0.99, 0.93" -o2 "OK - load average: 1.50, 0.99, 0.93" -r1 ".*: \d+.\d+, d+.\d+, (\d+.\d+)" -r2 ".*: \d+.\d+, (\d+.\d+), \d+.\d+" -op a -mm "The sum of the load averages: {0}"

    > The sum of the load averages: 1.92

## Setup Instructions

1. Download the python script and place it in a preferred location (/usr/local/nagios/libexec._dirnamehere_)
2. cd into the script location
3. Allow the script to be executable
      
       sudo chmod 755 rex_merge_check.py

4. Set up a command on your XI server that runs the script. Make sure to wrap all your argument macros in double quotes

       /usr/local/nagios/libexec._dirnamehere_/rex_merge_check.py -o1 "$ARG1$" -o2 "$ARG2$" -r1 "$ARG3$" -r2 "$ARG4$" -op "$ARG5$" -mm "$ARG6$"
    Save and apply the command
  
5. Set up the service check, be sure to substitute the macro for $ARG1$ and $ARG2$
    1. Service check macros are formatted as so: $SERVICEOUTPUT:name of host:service description$
6. For $ARG3$ and $ARG4$ a regex is needed to capture the value. Make sure the value is wrapped in a capture group. If the output from $ARG1$ or $ARG2$ only contains a numerical value use this regex: (.*)
7. $ARG5$ is the operation that will be performed on the captured value. Only add (a) is supported currently.
8. $ARG6$ is the output message. The output will replace ‘{0}’
9. Save and apply
10. Test your service check
