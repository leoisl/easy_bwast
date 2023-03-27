#!/usr/bin/env python
import argparse
import sys
from Bio import Entrez
import subprocess
import os
import logging
logging.basicConfig(stream=sys.stderr,
                    level=logging.INFO,
                    format='[%(asctime)s] (%(levelname)s) %(message)s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wrapper script to run blast and ACT on accessions without needing to download them.')

    # takes in the input files
    parser.add_argument('input', nargs="+", action="store", help="Specify at least 2 accessions with versions "
                                                                 "(e.g. CP052317.1, CP052432.1, etc)")
    parser.add_argument("-e", "--email", required=True, help="NCBI requires you to specify your email address with each request.")
    args = parser.parse_args()

    Entrez.email = args.email

    fasta_files = []
    for accession in args.input:
        fasta_file = accession+".fa"
        logging.info("Downloading fasta file for " + accession + " ...")
        with Entrez.efetch(db="nucleotide", id=accession, rettype="fasta", retmode="text") as net_handle, \
             open(fasta_file, "w") as accession_fh:
            accession_fh.write(net_handle.read())
            fasta_files.append(fasta_file)
        logging.info("Downloading fasta file for " + accession + " - done!")

    script_dir = os.path.dirname(os.path.realpath(__file__))
    bwast_script = script_dir + "/bwast.py"
    bwast_command = [sys.executable, bwast_script, "--act", *fasta_files]
    logging.info("Running " + " ".join(bwast_command) + " ...")
    subprocess.check_call(bwast_command)
