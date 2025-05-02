#!/usr/bin/env python3

import sys                      # For accessing command-line arguments and exiting
from Bio import Entrez          # Biopython module for accessing NCBI's Entrez system
import os                       # For file and directory operations

# Output directory for FASTA sequences
fasta_dir = "fasta_sequences"
os.makedirs(fasta_dir, exist_ok=True)  # Create the output directory if it doesn't exist

def search_entrez(database, search_term):
    """
    Searches the Entrez database and returns WebEnv and QueryKey for batch downloading.
    These are used to identify the session and the search results on NCBI's servers.
    """
    Entrez.email = "email@example.com"  # Required by NCBI; should be replaced with a valid user email
    handle = Entrez.esearch(db=database, term=search_term, usehistory="y", retmax=10000)  # Perform search
    record = Entrez.read(handle)  # Parse the search results
    handle.close()
    return record["WebEnv"], record["QueryKey"]  # Return session identifiers

def fetch_fasta(database, webenv, query_key):
    """
    Uses WebEnv and QueryKey to fetch the actual sequences in FASTA format from Entrez.
    """
    handle = Entrez.efetch(db=database, query_key=query_key, WebEnv=webenv,
                           rettype="fasta", retmode="text")  # Fetch sequences
    fasta_data = handle.read()  # Read the FASTA data
    handle.close()
    return fasta_data  # Return the raw FASTA string

def main():
    # Check if there are at least 3 arguments: script name, database, base search term, and at least one gene
    if len(sys.argv) < 3:
        print("Usage: python search_entrez.py <database> <base_search_term> <gene1> <gene2> ...")
        sys.exit(1)  # Exit with error if usage is incorrect

    database = sys.argv[1]             # Entrez database name (e.g., "nucleotide")
    base_search_term = sys.argv[2]     # Base term to search (e.g., author/year)
    genes = sys.argv[3:]               # List of gene names passed as arguments

    # For each gene, construct a search query, retrieve the results, and save them as FASTA
    for gene in genes:
        search_term = f"{base_search_term} AND {gene}"  # Combine base term and gene for refined search
        print(f"[INFO] Searching sequences for gene '{gene}' with query: {search_term}")

        webenv, query_key = search_entrez(database, search_term)  # Perform search and get session info
        fasta_data = fetch_fasta(database, webenv, query_key)     # Download FASTA sequences

        # Save the FASTA data to a file named after the gene
        fasta_file = os.path.join(fasta_dir, f"{gene}.fasta")
        with open(fasta_file, "w") as f:
            f.write(fasta_data)
        print(f"[OK] Sequences for gene '{gene}' saved to {fasta_file}")

# Standard Python boilerplate to ensure main() is called when script is run directly
if __name__ == "__main__":
    main()

