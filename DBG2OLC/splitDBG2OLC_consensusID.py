#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="Split DBG2OLC_Consensus_info.txt into N files or N seq. per file")
    
    parser.add_argument('-i', '-query', '--input_file', metavar='INPUT',
                        required=True, type=str, help='DBG2OLC_Consensus_info.txt input file with query structure')
    parser.add_argument('-o', '-out', '--output', metavar='OUTPUT',
                        type=str, help='Output file basename (default: $input_file_basename.atomic_$program_vs_$database_name)')
    parser.add_argument('-n', '--nb_seq', metavar='NBSEQ', default='50',
                        type=int, help='Number of sequences per subfile (default: 50)')
    parser.add_argument('-f', '--nb_file', metavar='NBFILE',
                        type=int, help='Number of subfiles to be created. Incompatible with the -n/--nb_seq argument')
    parser.add_argument('-v', '--version', action='version', version='Split multifasta v0.1')
    args = parser.parse_args()
    
    return args

def read_fasta_file_handle(fasta_file_handle):
    """
    Parse a fasta file like and return a generator
    """
    # Variables initialization
    header = ''
    seqlines = list()
    sequence_nb = 0
    # Reading input file
    for line in fasta_file_handle:
        if line[0] == '>':
            # Yield the last read header and sequence
            if sequence_nb:
                yield (header, ''.join(seqlines))
                del seqlines[:]
            # Get header
            header = line[1:].rstrip()
            sequence_nb += 1
        else:
            # Concatenate sequence
            #seqlines.append(line.strip())
            seqlines.append(line)
    # Yield the input file last sequence
    yield (header, ''.join(seqlines))
    # Close input file
    fasta_file_handle.close()

def format_seq(seq, linereturn=80):
    """
    Format an input sequence
    """
    buff = list()
    for i in xrange(0, len(seq), linereturn):
        buff.append("{0}\n".format(seq[i:(i + linereturn)]))
    return ''.join(buff)

def split_multifasta_by_increment(input_file_handle, directory_path, output_files_basename, max_nb_seq):
    """
    Split a multifasta file in subfiles of nb_seq_increment sequences
    """
    # Variable initialization
    subfile_nb = 0
    sequence_nb = 0
    subfile_fh = None
    # Reading input multifasta file
    for header, sequence in read_fasta_file_handle(input_file_handle):
        # Open a new subfile at the beginning and when reaching the maximum sequence number
        if sequence_nb % max_nb_seq == 0:
            # Close the last opened subfile
            if subfile_nb:
                subfile_fh.close()
            # Open a new subfile
            subfile_nb += 1
            subfile_name = "{0}.{1}.fasta".format(subfile_nb, output_files_basename)
            subfile_path = "{0}/{1}".format(directory_path, subfile_name)
            try:
                subfile_fh = open(subfile_path, 'w')
            except:
                sys.stderr.write("\nERROR: [Subfile] {0} cannot be created\n\n".format(subfile_path))
                raise
        # Write sequences in the subfiles
        subfile_fh.write(">{0}\n".format(header))
        #subfile_fh.write("{0}\n".format(format_seq(sequence, linereturn=80)))
        subfile_fh.write("{0}\n".format(sequence))
        sequence_nb += 1

    # Return the total subfiles number
    return subfile_nb
    
def main(args):
    """
    Main program
    """
    
    # Open the input file
    try:
        sys.stdout.write("QUERY: {input}\n".format(input=args.input_file))
        input_fh = open(args.input_file, 'r')
    except IOError:
        sys.stderr.write("ERROR: [Input] {0} cannot be open\n".format(args.input_file))
        raise
    
    # Generate the subfiles basename
    # get the input basename and remove the fasta extension
    subfiles_basename = re.sub(r'(\.fasta|\.fa|\.fsa|\.faa|\.fna)$', '', args.input_file.strip().split('/')[-1])
    
    # Define default tmp output directory and add the pid
    output_directory = "{0}".format(args.output)
    if not args.output:
        args.output = subfiles_basename
        output_directory = "{0}_split".format(subfiles_basename)
    # Remove the last backslash if any
    if output_directory[-1] == '/':
        output_directory = output_directory[:-1]
    sys.stdout.write("OUTDIR: {outdir}\n".format(outdir=output_directory))
    
    # Create the output directory if it doesn't exists
    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
    except OSError:
        sys.stderr.write("ERROR: [Outdir] {0} cannot be created\n\n".format(output_directory))
        raise
    
    ##### Step n°1: Split multifasta file #####
    # Compute subfile sequence number if a subfile number is defined
    if args.nb_file:
        # Count sequences number
        input_file_nb_seq = int(subprocess.check_output("grep -c '>' {0}".format(args.input_file), shell=True).strip())
        sys.stdout.write("INFO: {0} sequences in the query\n".format(input_file_nb_seq))
        # Compute subfiles sequence number
        args.nb_seq = (input_file_nb_seq / float(args.nb_file))
        # 10 seq / 2 files --> 5 seq/subfile || 10 seq / 3 files --> 3.333 --> 4 seq/subfiles
        if args.nb_seq % 1 != 0:
            args.nb_seq += 1
        args.nb_seq = int(args.nb_seq)
    
    total_subfiles_nb = args.nb_file

    sys.stdout.write('INFO: Splitting input file...\n')
    total_subfiles_nb = split_multifasta_by_increment(input_fh, output_directory, subfiles_basename, args.nb_seq)
    sys.stdout.write("INFO: The input file was splitted into {0} subfiles\n".format(total_subfiles_nb))

if __name__ == '__main__':
    args = get_args()
    main(args)