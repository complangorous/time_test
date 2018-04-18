# time_test

Performs a number of time tests on a list of python scripts to determine if their average run-time meet AWS Lambda's runtime requirements,
and writes the results to a tsv.

## Running

`$ python time_test scripts num_tests (--dest __)`

  Currently, time_test takes up to three arguments.
  
`scripts` (path or file) A plain text file containing a newline-delimited list of scripts' full paths.

`num_tests` (int) The number of times each script will be run.

`--dest __` (keyword + path) Allows the specification of the output file's destination.

**NOTE**: If running time_test in an ssh sess-ion on linux, be sure to run it with nohup,

`$ nohup python time_test.py file_list.txt num_test &`
        
.. if you are passing it an especially large number of files to test, or are testing them for an especially large value of 
num-tests. Using nohup will detatch the process from your console instance, so it will continue running if the pipe breaks.

## TODO
**(1)** Allow for configurable testing / abstract away from Lambda-specific testing.


**(2)** Allow users to specify the number of times individual scripts can be run. Probably specify exceptions to `num_tests` in
     `scripts` file.
