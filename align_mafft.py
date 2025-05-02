#!/usr/bin/env python3

import os # Imports the module to interact with the file system
import subprocess # Imports the module to execute external commands

def run_mafft(input_file, output_file):
    """
    Executes the alignment with MAFFT redirecting the respective result
    to an output_file.
    """
    cmd = ["mafft", "--auto", input_file] # Defines the command to be executed, this being an alignment with MAFFT
    with open(output_file, "w") as out: # Opens the output file for writing
        subprocess.run(cmd, stdout=out, stderr=subprocess.DEVNULL) # Executes the MAFFT command to save the result in the output, ignoring error messages
    print(f"[OK] Aligned: {output_file}") # Shows a message to notify the success of the command

def main():
    """
    Questions the user if it's desired to perform sequence alignments,
    proceeding to verify the existence of FASTA files and finally calling the
    aligner for each file.
    """
    user_input = input("Do you want to perform sequence alignments with MAFFT? [y/n]: ").strip().lower() # Prints a message asking for an input to confirm the user's intention, removing the spaces and setting such to smallcase
    if user_input != "y":
        print("[INFO] Alignment skipped by user.") # Shows this message in case the user does not want to align the sequences
        return # Closes the main function

    input_dir = "fasta_sequences" # Directory where the input files are from
    output_dir = "aligned" # Directory where the results will be saved to
    os.makedirs(output_dir, exist_ok=True) # Creates output directory if non existent

    fasta_files = [f for f in os.listdir(input_dir) if f.endswith(".fasta")] # Only lists the files ending in '.fasta' in the input directory
    if not fasta_files:
        print("[ERROR] No FASTA files found in 'cleaned' directory.") # Error message incase of no FASTA files found
        return # Closes the main function

    for fasta_file in fasta_files: # For each FASTA file, executes the alignment
        input_path = os.path.join(input_dir, fasta_file) # Complete path to the input file
        output_path = os.path.join(output_dir, fasta_file) # Complete path to the output file
        run_mafft(input_path, output_path) # Runs the function responsible to execute MAFFT

if __name__ == "__main__": # Checks if the script is being executed directly
    main()
