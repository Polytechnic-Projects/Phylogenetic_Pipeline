#!/usr/bin/env python3

import os # Imports module for manipulating directories and paths
import csv # Imports module for reading and writing CSV files
import re # Imports module for operations with regular expressions (regex)

def parse_header(header_line):
    """
    Build headers in species_voucher or species_genbankID format
    """
    header = header_line.lstrip(">").strip() # Removes '>' and bonus spaces
    parts = header.split() # Splits the header by spaces

    if len(parts) < 3: # In case of a header with less than 3 parts,
        return None, None, None # Returns None, symbolizing a badly formatted header

    genbank_id = parts[0].split(".")[0] # Gets the GenBank ID without its version
    genes = parts[1] # Related gene
    species = parts[2] # Species name
    species_name = f"{genes}_{species}" # Combines gene and species

    voucher_match = re.search(r'voucher[_\s:]?([\w\-]+)', header, re.IGNORECASE) # Extracts voucher from header
    if voucher_match:
        voucher = voucher_match.group(1)
        full_id = f"{species_name}_{voucher}" # Final ID with voucher
    else:
        full_id = f"{species_name}_{genbank_id}" # Final ID with GenBank ID

    full_id = re.sub(r'[^\w\-]', '_', full_id) # Cleans the ID by replacing any non alphabetical character with an underline

    return full_id, species_name, header # Returns the extracted data

def sanitize_fasta(input_path, output_fasta, output_csv):
    """
    Creates a new FASTA with a cleaned header version
    and a CSV with a mapping with the cleaned IDS and the original headers
    """
    with open(input_path, "r") as infile, \ 
         open(output_fasta, "w") as fasta_out, \
         open(output_csv, "w", newline="") as map_out: # Opens the input path for reading and both output FASTA and CSV for writing

        writer = csv.writer(map_out)
        writer.writerow(["clean_id", "species", "original_header"]) # CSV header

        current_clean_id = None # Controls which ID is being used for the sequence

        for line in infile:
            line = line.strip()
            if line.startswith(">"):
                clean_id, species, full_header = parse_header(line) # Processes the header
                if not clean_id:
                    print(f"[WARNING] Bad formatted header: {line}") # Warns for poorly formatted header
                    continue
                writer.writerow([clean_id, species, full_header]) # Writes in CSV
                fasta_out.write(f">{clean_id}\n") # Writes new header in FASTA
                current_clean_id = clean_id
            elif current_clean_id:
                fasta_out.write(f"{line}\n")

    print(f"[OK] Cleaned FASTA saved as: {output_fasta}") # Informs the success and its respective output FASTA
    print(f"[OK] Mapping saved as: {output_csv}") # Informs the success and its respective output CSV

def main():
    """
    Executes the cleaning and mapping for each found file if
    such asked by user
    """
    answer = input("[?] Do you want to clean and rename all FASTA files in 'aligned/'? (y/n): ").strip().lower() # Prints a message asking for an input to confirm the user's intention, removing the spaces and setting such to smallcase
    if answer != 'y':
        print("[INFO] Operation aborted by user.") # Shows this message in case the user does not confirm
        return # Closes the function

    input_dir = "aligned" # Input directory
    os.makedirs(input_dir, exist_ok=True) # Ensures the existence of the directory

    fasta_files = [f for f in os.listdir(input_dir) if f.endswith(".fasta") or f.endswith(".fa")] # Filters only files with the .fa or .fasta extension
    if not fasta_files:
        print(f"[ERROR] No FASTA files found in '{input_dir}/'") # Shows an error message warning for the non existence of FASTA files
        return # Closes the function

    for file in fasta_files: # Processes each found file
        input_path = os.path.join(input_dir, file)
        base_name = os.path.splitext(file)[0] # Removes the extension of the file's name
        fasta_out = os.path.join(input_dir, f"{base_name}_cleaned.fasta") # Joins the new name for the clean FASTA
        csv_out = os.path.join(input_dir, f"{base_name}_map.csv") # Joins its respective mapping
        print(f"[INFO] Processing: {file}")
        sanitize_fasta(input_path, fasta_out, csv_out) # Calls the cleaning function

if __name__ == "__main__": # Checks if the script is being executed directly
    main()
