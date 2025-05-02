#!/usr/bin/env python3

"""
main_pipeline.py: runs the full phylogenetic pipeline.
1. search_entrez.py     – searches and downloads sequences from NCBI
2. align_mafft.py       – aligns the sequences using MAFFT
3. clean_name.py        – standardizes sequence names
4. export_concat.py     – concatenates alignments and exports them
5. raxml_tree.py        – builds a tree using RAxML
6. mrbayes_tree.py      – builds a tree using MrBayes
"""

import subprocess # Allows running external commands and scripts
import sys        # Used to access Python executable and exit with specific status codes

def run_script(script, args=None):
    """Runs a Python script and stops if it returns an error."""
    print(f"\n[RUNNING] {script}") # Notify which script is currently running
    command = [sys.executable, script] + (args or []) # Construct the command: python script arg1 arg2 ...
    result = subprocess.run(command) # Run the command
    if result.returncode != 0:
        # If the script exited with a non-zero code, show error and exit pipeline
        print(f"[ERROR] Script {script} exited with code {result.returncode}")
        sys.exit(result.returncode)

if __name__ == "__main__":
    # Entry point of the script
    print("Starting full phylogenetic pipeline...")
    
    # Ask the user for input to pass to search_entrez.py
    db = input("Enter Entrez database (e.g., nucleotide): ").strip()
    term = input("Enter base search term (e.g., Portillo F [author], 2018 [year]): ").strip()
    genes = input("Enter gene names separated by space (e.g., 16S ND4 cytb c-mos RAG1): ").split()

    # Step 1: Search and download sequences from NCBI
    run_script("search_entrez.py", [db, term] + genes)
    
    # Step 2: Align sequences with MAFFT
    run_script("align_mafft.py")
    
   # Step 3: Clean and standardize sequence names
    run_script("clean_name.py")

   # Step 4: Concatenate and export alignments for tree building
    run_script("export_concat.py")

   # Step 5: Build phylogenetic tree using RAxML
    run_script("raxml_tree.py")

    # Step 6: Build phylogenetic tree using MrBayes
    run_script("mrbayes_tree.py")

    print("\n[OK] Pipeline completed successfully!") # Final success message
