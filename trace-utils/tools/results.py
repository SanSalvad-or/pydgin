#=========================================================================
# results.py
#=========================================================================
# Author : Shreesha Srinath
# Date   : October 6th, 2017
#
# Quick and dirty script to parse results

import os
import sys
import re
import subprocess

from collections import defaultdict

#-------------------------------------------------------------------------
# Utility Function
#-------------------------------------------------------------------------

def execute(cmd):
  try:
    #print cmd
    return subprocess.check_output(cmd, shell=True)
  except  subprocess.CalledProcessError, err:
    print "ERROR: " + err.output

#-------------------------------------------------------------------------
# Global variable
#-------------------------------------------------------------------------

app_short_name_dict = {
  'pbbs-bfs-deterministicBFS'    : 'bfs-d',
  'pbbs-bfs-ndBFS'               : 'bfs-nd',
  'pbbs-csort-quickSort'         : 'qsort',
  'pbbs-csort-quickSort-1'       : 'qsort-1',
  'pbbs-csort-quickSort-2'       : 'qsort-2',
  'pbbs-csort-sampleSort'        : 'sampsort',
  'pbbs-csort-sampleSort-1'      : 'sampsort-1',
  'pbbs-csort-sampleSort-2'      : 'sampsort-2',
  'pbbs-dict-deterministicHash'  : 'dict',
  'pbbs-hull-quickHull'          : 'hull',
  'pbbs-isort-blockRadixSort'    : 'radix-1',
  'pbbs-isort-blockRadixSort-1'  : 'radix-2',
  'pbbs-knn-octTree2Neighbors'   : 'knn',
  'pbbs-mis-ndMIS'               : 'mis',
  'pbbs-nbody-parallelBarnesHut' : 'nbody',
  'pbbs-rdups-deterministicHash' : 'rdups',
  'pbbs-sa-parallelRange'        : 'sarray',
  'pbbs-st-ndST'                 : 'sptree',
  'cilk-cholesky'                : 'clsky',
  'cilk-cilksort'                : 'cilksort',
  'cilk-heat'                    : 'heat',
  'cilk-knapsack'                : 'ksack',
  'cilk-matmul'                  : 'matmul',
}

#-------------------------------------------------------------------------
# results_summary()
#-------------------------------------------------------------------------

def results_summary():
  resultsdir_path = '../results-minpc-small'
  with open('results.csv', 'w') as out:
    out.write('app,config,stat,value\n')
    subfolders = os.listdir( resultsdir_path )
    for subfolder in subfolders:
      trace_file =  resultsdir_path + '/' + subfolder + '/trace-analysis.txt'
      cmd = "grep -r -A 5 Overall %(out)s" % { 'out' : trace_file }
      lines = execute( cmd )
      stats = defaultdict(list)
      for line in lines.split('\n'):
        line = line.split(':')
        line = [ re.sub('%', '', token).rstrip() for token in line ]
        if 'savings' in line[0]:
          stats['savings'].append( line[1] )
        elif 'steps' in line[0]:
          stats['steps'].append( line[1] )

      app = re.sub("-parc", '', subfolder)
      app = re.sub("-small", '', app)

      out.write('{},{},{},{}\n'.format(app,'maxshare','savings',stats['savings'][0]))
      out.write('{},{},{},{}\n'.format(app,'minpc','savings',stats['savings'][1]))
      out.write('{},{},{},{}\n'.format(app,'maxshare','steps',stats['steps'][0]))
      out.write('{},{},{},{}\n'.format(app,'minpc','steps',stats['steps'][1]))

results_summary()
