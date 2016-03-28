#!/usr/bin/env python

"""
    This script verifies the Limited-Knowledge(LK) and No-Knowledge(NK)
    benchmark sets. The entry points for such verification are the
    following two methods:

        verify_LK_benchmark: 
            This method need to be invoked to verify LK-benchmark files.
            The arguments for calling this method are the following:
                t1_iea_handle: file handle to a t1_ea file
                t1_exp_handle: file handle to a t1_exp file
                t2_exp_handle: file handle to a t2_exp file
                output_filename_LK_bpo: file name to a LK-bpo benchmark set
                output_filename_LK_cco: file name to a LK-cco benchmark set
                output_filename_LK_mfo: file name to a LK-mfo benchmark set

        verify_NK_benchmark: 
            This method need to be invoked to verify NK-benchmark files. The 
            arguments for calling this method are the following:
                t1_iea_handle: file handle to a t1_ea file
                t1_exp_handle: file handle to a t1_exp file
                t2_exp_handle: file handle to a t2_exp file
                output_filename_LK_bpo: file name to a NK-bpo benchmark set
                output_filename_LK_cco: file name to a NK-cco benchmark set
                output_filename_LK_mfo: file name to a NK-mfo benchmark set

        The following methods are invoked by the above two methods to create
        required data structures and perform the verification:

       create_iea_ann_dict: 
                This method builds a dictionary for <protein, GO ID> tuples 
                from t1_iea file.

       create_ann_ann_dict: 
                This method builds three dictionaries in BPO, CCO, and MFO 
                categories for <protein, GO ID> tuples from a 
                t1_exp or t2_exp file.

       verify_LK_benchmark_xxo: 
               This method verifies any of the LK-benchmark sets.

       verify_NK_benchmark_xxo: 
               This method verifies any of the NK-benchmark sets.
"""

import os.path
import sys
from collections import defaultdict

import FormatChecker as fc

def create_iea_ann_dict(goa_iea_handle):
     # Initialize a dictionar which will later be populated with
    # <protein, GO ID> tuples from t1_iea file:
    dict_iea = defaultdict(lambda:set())
    # Populate the dictionary for t1_iea with <protein, GO terms> as
    # <key, values> pairs from the entries with NOn-Experimental Evidence
    # at time t1:
    for lines in goa_iea_handle:
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        dict_iea[cols[1]].add(cols[4])
        # Column 1: protein name, Column 4: GO ID
    return dict_iea

def create_exp_ann_dict(goa_exp_handle):
    """
    This method builds three dictionaries in BPO, CCO, and MFO categories
    for <protein, GO ID> tuples from UniProt-GOA file without the header
    string.
    """
    # Initialize three dictionaries in BPO, CCO, and MFO ontology groups
    # which will later be populated with <protein, GO ID> tuples from
    # t1_exp file ontology groups:
    dict_bpo = defaultdict(lambda:set())
    dict_cco = defaultdict(lambda:set())
    dict_mfo = defaultdict(lambda:set())

    # Populate the three dictionaries for t1_exp with <protein, GO terms>
    # as <key, values> pairs from the entries with Non-Experimental Evidence
    # at time t1:
    for lines in goa_exp_handle:
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        if cols[8] == 'F': # Column 8: Ontology group
            dict_mfo[cols[1]].add(cols[4])
            # Column 1: protein name, Column 4: GO ID 
        elif cols[8] == 'P':
            dict_bpo[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            dict_cco[cols[1]].add(cols[4])
    return (dict_bpo, dict_cco, dict_mfo)

def verify_LK_benchmark_xxo(t1_iea_dict,
                            t1_xxo_dict,
                            t2_xxo_dict,
                            output_filename_LK_xxo, # benchmark file name
                            LKcount):
    """
    This method verifies the benchmark entries in the benchmark file
    output_filename_LK_xxo.

    Meaning of xxo: xxo is replaced runtime by bpo, cco, or mfo to make 
    this method specific to a certain type of benchmarks.
    """
#    if os.path.exists(output_filename_LK_xxo) and \
#       os.stat(output_filename_LK_xxo).st_size != 0:

    outfile_LK_xxo_handle = open(output_filename_LK_xxo, 'r')
    for lines in outfile_LK_xxo_handle:
        cols = lines.strip().split('\t')
        if cols[0] not in t1_iea_dict:
            print 'Error: an undesired protein ' + cols[0] + \
                ' got selected in ' + output_filename_LK_xxo
            break
        elif cols[0] in t1_xxo_dict:
            print 'Error: selected protein ' + cols[0] + ' in ' + \
                output_filename_LK_xxo + ' already had experimental \
                evidence at t1'
            break
        elif cols[0] not in t2_xxo_dict or cols[1] not in t2_xxo_dict[cols[0]]:
            print 'Error: selected protein ' + cols[0] + ' in ' + \
                output_filename_LK_xxo + ' has not gained experimental \
                evidence at t2'
            break
    outfile_LK_xxo_handle.close()
    LKcount += 1
    return LKcount

def verify_NK_benchmark_xxo(t1_iea_dict,
                            t1_bpo_dict,
                            t1_cco_dict,
                            t1_mfo_dict,
                            t2_xxo_dict,
                            output_filename_NK_xxo,
                            NKcount):
    """ 
    This method verify the benchmark entries in the benchmark file 
    output_filename_NK_xxo.

    Meaning of xxo: xxo is replaced runtime by bpo, cco, or mfo to make 
    this method specific to a certain type of benchmarks.

    """
    if os.path.exists(output_filename_NK_xxo) and \
       os.stat(output_filename_NK_xxo).st_size != 0:
        outfile_NK_xxo_handle = open(output_filename_NK_xxo, 'r')
        for lines in outfile_NK_xxo_handle:
            cols = lines.strip().split('\t')
            if cols[0] not in t1_iea_dict:
                print 'Error: an undesired protein ' + cols[0] + \
                      ' got selected in ' + output_filename_NK_xxo
                break
            elif cols[0] in t1_bpo_dict or \
                 cols[0] in t1_cco_dict or \
                 cols[0] in t1_mfo_dict:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                      output_filename_NK_xxo + ' already had experimental \
                      evidence at t1'
                break
            elif cols[0] not in t2_xxo_dict:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                      output_filename_NK_xxo + ' has not gained experimental \
                      evidence at t2'
                break
        outfile_NK_xxo_handle.close()
        NKcount += 1
    return NKcount

def verify_LK_benchmark(t1_iea_handle,
                        t1_exp_handle,
                        t2_exp_handle,
                        output_filename_LK_bpo,
                        output_filename_LK_cco,
                        output_filename_LK_mfo):
    """ 
    This method verifies Limited-Knowledge benchmark sets.
    """
    # Create a dictionary for the <protein, GO ID> tuples from t1_iea file:
    t1_iea_dict = create_iea_ann_dict(t1_iea_handle)

    # Create BPO, CCO and MFO dictionaries for the
    # <protein, GO ID> tuples from t1_exp file:
    t1_bpo_dict, t1_cco_dict, t1_mfo_dict = create_exp_ann_dict(t1_exp_handle)

    # Create BPO, CCO and MFO dictionaries for the
    # <protein, GO ID> tuples from t2_exp file:
    t2_bpo_dict, t2_cco_dict, t2_mfo_dict = create_exp_ann_dict(t2_exp_handle)
   
    # Check file format for LK_bpo benchmark file. 
    # LK_bpo is True when the filename is non-empty, file exists, file size 
    # is non-zero and file in correct format:
    LK_bpo = fc.check_benchmark_format(output_filename_LK_bpo)
    # Check file format for LK_cco benchmark file:
    LK_cco = fc.check_benchmark_format(output_filename_LK_cco)
    # Check file format for LK_mfo benchmark file:
    LK_mfo = fc.check_benchmark_format(output_filename_LK_mfo) 

    LKcount = 0
    if (not LK_bpo):
        LKcount = LKcount + verify_LK_benchmark_xxo(t1_iea_dict,
                                                    t1_bpo_dict,
                                                    t2_bpo_dict,
                                                    output_filename_LK_bpo,
                                                    LKcount)
    if (not LK_cco):
        LKcount = LKcount + verify_LK_benchmark_xxo(t1_iea_dict,
                                                    t1_cco_dict,
                                                    t2_cco_dict,
                                                    output_filename_LK_cco,
                                                    LKcount)
    if (not LK_mfo):
        LKcount = LKcount + verify_LK_benchmark_xxo(t1_iea_dict,
                                                    t1_mfo_dict,
                                                    t2_mfo_dict,
                                                    output_filename_LK_mfo,
                                                    LKcount)
    return (LK_bpo, LK_cco, LK_mfo, LKcount)

def verify_NK_benchmark(t1_iea_handle,
                        t1_exp_handle,
                        t2_exp_handle,
                        output_filename_NK_bpo,
                        output_filename_NK_cco,
                        output_filename_NK_mfo):
    """
    This method verifies No-Knowledge benchmark sets.
    """
    # Create a dictionary for the <protein, GO ID> tuples from t1_iea file:
    t1_iea_dict = create_iea_ann_dict(t1_iea_handle)

    # Create BPO, CCO and MFO dictionaries for the
    # <protein, GO ID> tuples from t1_exp file:
    t1_bpo_dict, t1_cco_dict, t1_mfo_dict = create_exp_ann_dict(t1_exp_handle)

    # Create BPO, CCO and MFO dictionaries for the
    # <protein, GO ID> tuples from t2_exp file:
    t2_bpo_dict, t2_cco_dict, t2_mfo_dict = create_exp_ann_dict(t2_exp_handle)

    # Check file format for LK_bpo benchmark file. 
    # LK_bpo is True when the filename is non-empty, file exists, file size 
    # is non-zero and file in correct format:
    NK_bpo = fc.check_benchmark_format(output_filename_NK_bpo)
    # Check file format for LK_cco benchmark file:
    NK_cco = fc.check_benchmark_format(output_filename_NK_cco)
    # Check file format for LK_mfo benchmark file:
    NK_mfo = fc.check_benchmark_format(output_filename_NK_mfo) 

    NKcount = 0
    # Verify NK-BPO benchmarks:
    if (not NK_bpo):
        NKcount = NKcount + verify_NK_benchmark_xxo(t1_iea_dict,
                                                    t1_bpo_dict,
                                                    t1_cco_dict,
                                                    t1_mfo_dict,
                                                    t2_bpo_dict,
                                                    output_filename_NK_bpo,
                                                    NKcount)
    # Verify NK-CCO benchmarks:
    if (not NK_cco):
        NKcount = NKcount + verify_NK_benchmark_xxo(t1_iea_dict,
                                                    t1_bpo_dict,
                                                    t1_cco_dict,
                                                    t1_mfo_dict,
                                                    t2_cco_dict,
                                                    output_filename_NK_cco,
                                                    NKcount)
    # Verify NK-MFO benchmarks:
    if (not NK_mfo):
        NKcount = NKcount + verify_NK_benchmark_xxo(t1_iea_dict,
                                                    t1_bpo_dict,
                                                    t1_cco_dict,
                                                    t1_mfo_dict,
                                                    t2_mfo_dict,
                                                    output_filename_NK_mfo,
                                                    NKcount)
    return (NK_bpo, NK_cco, NK_mfo, NKcount)

if __name__ == "__main__":
    print (sys.argv[0] + ' docstring:')
    print (__doc__)
    sys.exit(0)

