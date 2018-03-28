#!/usr/bin/env python

'''
        Performs n time tests on a list of python
        scripts to determine if their average run-
        time meet Lambda's runtime requirements,
        and writes the results to a tsv.

	NOTE: If running time_test in an ssh sess-
	ion, be sure to run it with nohup, 
	
	$ nohup python time_test.py file_list.txt num_test &

	if you are passing it an especially large
	number of files to test, or are testing
	them for an especially large value of 
	num-tests. Using nohup will detatch the
	process from your console instance, so it
	will continue running if the pipe breaks.	
'''


__author__ = 'sam.ryan'

import argparse
import os
import time
import pandas as pd

parser = argparse.ArgumentParser(add_help=True)
# 'scripts' is the full path to the .csv file containing the 
# python scripts
parser.add_argument('scripts', type=str,
		    help='The path of the .txt file containing the list of scripts to test.')
# 'num_tests' is the number of run-times to record
parser.add_argument('num_tests', type=int,
		    help='The number of run-times to record.')
# 'dest_path' is an optional argument
# specifying the destination of the 
# output file
parser.add_argument('--dest', nargs='?',
		    const=None, default=None,
		    help='(Optional) Specify the destination of the output file. Default behavior
			  is to write the file to the directory of time_test.py')
args = parser.parse_args()

# open file containing script list
# and remove newlines from entries
scripts = open(args.scripts).readlines()
scripts = [script.rstrip('\n') for script in scripts]
runtime_cols = []
columns_dict = {'Script': [], 'Average Case (Minutes)': []}

# populate columns_dict with num_tests pairs of
# <<Runtime {} / Run {}: Successful Exit>> columns
# 
# stash <<Runtime {}>> columns in runtime_cols for
# calculating the average cases of each script
for n in range(args.num_tests):
        columns_dict['Runtime {}'.format(str(n+1))] = []
        runtime_cols.append('Runtime {}'.format(str(n+1)))
        columns_dict['Run {}: Successful Exit'.format(str(n+1))] = []

for script in scripts:
        for n in range(args.num_tests):
                print '{0} Running ... {1} {2}/{3}'.format('\n', script,  str(n+1), args.num_tests)
                start = time.time()

                result = os.system('python {}'.format(script))
                # if os.system('python {script}') returns 0, 
                # no error was encountered.
                if result != 0:
                        columns_dict['Run {}: Successful Exit'.format(str(n+1))].append(False)
                        runtime = time.time() - start
                        columns_dict['Runtime {}'.format(str(n+1))].append(runtime)
                        print '{0} Error encountered while running {1} --- executed in {2:.2f} seconds {0}'.format('\n', script, runtime)
                else:
			columns_dict['Run {}: Successful Exit'.format(str(n+1))].append(True)
                        runtime = time.time() - start
                        columns_dict['Runtime {}'.format(str(n+1))].append(runtime)
                        print '{0} Done executing {1} --- executed in {2:.2f} seconds {0}'.format('\n', script, runtime)

        # get the average performance for the script, in minutes
        columns_dict['Average Case (Minutes)'].append((sum([columns_dict[x][-1] for x in runtime_cols]) / args.num_tests) / 60.0)
        columns_dict['Script'].append(script)

columns_dict['Under time limit'] = [(True if z < 5.0 else False) for z in columns_dict['Average Case (Minutes)']]
df = pd.DataFrame(columns_dict)

# orders the columns corresponding to
# each run so they follow the pattern -
# Runtime {} | Runtime {}: Successful Exit
exit_statuses = [x for x in df.columns.tolist() if 'Successful' in x]
exit_statuses.sort()
runtimes = [y for y in df.columns.tolist() if 'Runtime' in y]
runtimes.sort()

cols = ['Script']
for n in range(args.num_tests):
        cols.append(runtimes.pop(0))
        cols.append(exit_statuses.pop(0))
cols.append('Average Case (Minutes)')
cols.append('Under time limit')

df = df[cols]
print df

from datetime import datetime
curr_date = datetime.now().date()
curr_date = str(curr_date)

if args.dest is None:
	df.to_csv('{1}_time_test_results.tsv'.format(curr_date), sep='\t', index=False)
else:
	df.to_csv('{0}/{1}_time_test_results.tsv'.format(args.dest, curr_date), sep='\t', index=False)

