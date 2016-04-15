#!/usr/bin/env python

'''
   The entry point of this script is parse_args() method which calls
   other methods to collect user supplied arguments, parses and
   verifies them, and at the end returns those arguments as a dictionary.
   Description of these methods are the following:
   

   parse_args:
      This method calls the methods described below and returns the final 
      dictionary containing the user supplied arguments to the Benchmark 
      or Verify program at the calling point.

   collect_args:
       This method collects the user supplied arguments. The method takes
       a string argument which can take two string values 'benchmark' or
       'verify'. The string value 'benchmark' indicates that the method is
        invoked by Benchmark program and 'verify' indicates that the
        method is invoked by Verify program. When this method is invoked
        by Benchmark program, the method gives user an option to provide
        an output file name. On the other hand, when the method is invoked
        by Verify program, the method accepts a mandatory benchmark file
        name as the user argument.

   extract_args:
       This method puts the user supplied arguments into an ordered
       dictionary which it returns at the end.

   check_args:
       This method verifies the correctness of the user supplied
       arguments and puts them into an ordered dictionary which the method 
       returns at the end. 
'''

import os
import sys
import argparse
import re
from collections import OrderedDict

def collect_args(prog='benchmark'):
    """ 
    This method collects the user supplied arguments and returns 
    them at the end.
    """
    if prog == 'benchmark':
        parser = argparse.ArgumentParser(description='Creates benchmark ' + \
                    'sets from two annotation files at two time points')
    elif prog == 'verify':
        parser = argparse.ArgumentParser(description='Verifies benchmark ' + \
                    'sets generated by Benchrmark Creation Tool ')

    parser.add_argument('-I1', '--input1', help='Specifies path to the ' + \
                    'first input file. This opton is mandatory.')
    parser.add_argument('-I2', '--input2', help='Specifies path to the ' +  \
                    'second input file. This option is mandatory.')
    if prog == 'benchmark':
        parser.add_argument('-O', '--output', default='', help='Provides ' + \
            'user an option to specify an output filename.')
    elif prog == 'verify':
        parser.add_argument('-I3', '--input3', help='Specifies path to ' + \
           'one of the SIX benchmark files. This option is mandaroty.')
    parser.add_argument('-G','--organism',nargs='*', default=['all'],help= \
                    'Provides user a choice to specify a set of organisms ' + \
                    '(example:Saccharomyces cerevisiae or 7227) separated ' + \
                    'by space. Default is all.')
    parser.add_argument('-N','--ontology',nargs='*', default=['all'],help= \
                    'Provides user a choice to specify a set of ' + \
                    'ontologies (F, P, C) separated by space. ' + \
                    'Default is all.')
    parser.add_argument('-V','--evidence',nargs='*', default=['all'],help= \
                    'Provides user a choice to specify a set of GO ' + \
                    'experimental evidence codes (example: IPI, IDA, ' + \
                    'EXP) separated by space. Default is all.')
    parser.add_argument('-S', '--source',action='store', nargs='*',default=\
                    ['all'],help='Provides user a choice to specify ' + \
                    'sources (example: UniProt, InterPro) separated ' + \
                    'by spaces. Default is all.')
    parser.add_argument('-C', '--confidence',default='F',help='Allows ' + \
                    'user to turn on the annotation confidence filter. ' + \
                    'If turned on, GO terms assignments to proteins that ' + \
                    'are documented in few papers (4 or less by default) ' + \
                    'will not be considered part of the benchmark set. By ' + \
                    'default, it is turned off.')
    parser.add_argument('-T', '--threshold',type=int, default=4,help= \
                    'Allows users to specify a threshold for the minimum ' + \
                    'number of papers to be used for having a confident ' + \
                    'annotation. If not specified, defaults to a value of 4.')
    parser.add_argument('-P', '--pubmed',default='F',help='Allows user to ' + \
                    'turn on the pubmed filter. If turned on, GO terms ' + \
                    'w/o any Pubmed references will not be considered ' + \
                    'part of the benchmark set. By default, it is ' + \
                    'turned off.')
    parser.add_argument('-B', '--blacklist', nargs='*',default=[], help= \
                    'This parameter can take in a list of pubmed ids. ' + \
                    'All GO terms and proteins annotated in them will ' + \
                    'be eliminated from the benchmark set. Default is ' + \
                    'an empty list.')
    return parser

def extract_args(args, prog):
    """
    This method builds a dictionary from the user supplied arguments
    and returns the constructed dictionary at the end.
    """
    args_dict = OrderedDict() 
    args_dict['t1'] = args.input1
    args_dict['t2'] = args.input2
    if prog == 'benchmark':
        args_dict['outfile'] = args.output # Default: ''
    elif prog == 'verify': 
        args_dict['t3'] = args.input3
    args_dict['Taxon_ID'] = args.organism # Default: 'all'
    args_dict['Aspect'] = args.ontology # Default: 'all'
    args_dict['Evidence'] = args.evidence # Default: 'all'   
    args_dict['Assigned_By'] = args.source # Default is 'all' 
    args_dict['Confidence'] = args.confidence # Default: 'F'
    args_dict['Threshold'] = args.threshold # Default: 4
    args_dict['Pubmed'] = args.pubmed # Default: 'F' 
    args_dict['Blacklist'] = args.blacklist # Default: [] 
    return args_dict
    
def check_args(args_dict, parser):
    """ 
    This method checks the consistency of the user arguments. It builds 
    a new ordered dictionary of the input arguments and returns the 
    created dictionary at the end.
    """
    user_dict = OrderedDict() 
    for arg in args_dict:
        if arg == 't1':
            if args_dict[arg] == None:
                print 'Missing input file at time t1\n'
                print parser.parse_args(['--help'])
            else:
                user_dict['t1'] = args_dict[arg]
        elif arg == 't2':
            if args_dict[arg] == None:
                print 'Missing input file at time t2\n'
                print parser.parse_args(['--help'])
            else:
                user_dict['t2'] = args_dict[arg]
        elif arg == 't3':
            if args_dict[arg] == None:
                print 'Missing the benchmark file name\n'
                print parser.parse_args(['--help'])
            else:
                user_dict['t3'] = args_dict[arg]
        elif arg == 'outfile':
            user_dict[arg] = args_dict[arg]
        elif arg == 'Threshold':
            user_dict[arg] = args_dict[arg]
        elif arg == 'Confidence':
            user_dict[arg] = args_dict[arg]
        elif arg == 'Pubmed':
            user_dict[arg] = args_dict[arg]
        elif arg == 'Taxon_ID':
            if 'all' in args_dict[arg] or len(args_dict[arg]) == 0:
                user_dict[arg] = set([]) 
            else:
                args_dict[arg] = [x.capitalize() for x in args_dict[arg]]
                user_dict[arg] = set(args_dict[arg])
        else: # Aspect, Evidence, Assigned_By, Blacklist
            if 'all' in args_dict[arg] or len(args_dict[arg]) == 0:
                user_dict[arg] = set([])
            else:
                args_dict[arg] = [x.upper() for x in args_dict[arg]]
                user_dict[arg] = set(args_dict[arg])
    return user_dict

def parse_args(prog='benchmark'):
    """ 
    This is the entry point for the other methods in this module. It
       1. invokes collect_args to collect user arguments
       2. puts those arguments into a dictionary by calling extract_args method
       3. checks the consistency of those arguments by invoking check_args which
          returns a dictionary of correct arguments
       4. returns the dictionary at the end.
    """
    # Collect user supplied argument values:
    parser = collect_args(prog) 
    args_dict = {}
    args, unknown = parser.parse_known_args()
    if len(unknown) > 0:
        print '\n*********************************'
        print "Invalid Arguments"
        print '*********************************\n'
        # Shows help messages and quits:
        print parser.parse_args(['--help']) 
    args_dict = extract_args(args, prog)
    user_dict = check_args(args_dict, parser)
    return user_dict

if __name__ == '__main__':
    print (sys.argv[0] + ':')
    print (__doc__)
    sys.exit(0) 
