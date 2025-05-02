#!/usr/bin/env python3

"""
export_concat.py: Concatenates or exports gene alignments into NEXUS/PHYLIP formats with MrBayes blocks.
"""

import os
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Data.IUPACData import ambiguous_dna_letters

VALID_DNA = set(ambiguous_dna_letters) # Defines the valid DNA letters including ambiguosities


def make_unique_ids(records):
    """
    Creates IDS guaranteeing their uniqueness
    """
    seen = {} # Defines an ID dictionary
    for rec in records:
        base_id = rec.id
        if base_id not in seen:
            seen[base_id] = 1 # If input ID not in dictionary, add it
        else:
            seen[base_id] += 1 # If input ID found in dictionary, add 1 to the last ID found
            rec.id = f"{base_id}_{seen[base_id]}" # Adds a suffix to duplicates
    return records 


def export_individual_alignments():
    """
    Exports each aligned gene sequence from the 'aligned' directory
    into separate PHYLIP and NEXUS files in the 'individual' directory..
    """
    aligned_dir = "aligned" # Input directory with aligned FASTA
    output_dir = "individual" # Output directory
    os.makedirs(output_dir, exist_ok=True) # Creates a new directory if non existent

    fasta_files = [f for f in os.listdir(aligned_dir) if f.endswith("_cleaned.fasta")] # Lists all FASTA files ending with "_cleaned.fasta"
    for fasta_file in fasta_files:
        gene = fasta_file.replace("_cleaned.fasta", "") # Extracts gene name
        path = os.path.join(aligned_dir, fasta_file) # Complete file path
        alignment = AlignIO.read(path, "fasta") # Reads alignment

        records = make_unique_ids(list(alignment)) # Runs other defined function to guarantee the uniqueness of ID
        alignment = MultipleSeqAlignment(records) # Creates new alignment

        # PHYLIP
        phylip_path = os.path.join(output_dir, f"{gene}.phy") # Creates PHYLIP file path to be saved on the output directory
        AlignIO.write(alignment, phylip_path, "phylip-relaxed") # Saves alignment in format relaxed PHYLIP

        # NEXUS with MrBayes block
        nexus_path = os.path.join(output_dir, f"{gene}.nex") # Defines path to NEXUS file
        with open(nexus_path, "w") as out: # Opens said file for writing function
            out.write("#NEXUS\n\nBegin data;\n") # Writes header in NEXUS pattern
            out.write(f"  Dimensions ntax={len(alignment)} nchar={alignment.get_alignment_length()};\n") # Defines the tax number and the sequences total length
            out.write("  Format datatype=dna missing=? gap=- interleave=no;\n") # Defines the alignment format
            out.write("  Matrix\n") # Begins the sequence block
            for record in alignment: # Iterates by alignment sequences
                seq = str(record.seq).upper() # Converts sequence to string and capital letter
                cleaned = ''.join(c if c in VALID_DNA else 'N' for c in seq) # Replaces any unknown character by 'N'
                out.write(f"{record.id:<25} {cleaned}\n") # Writes sequence ID followed by the sequence itself
            out.write("  ;\nEnd;\n\n") # Ends NEXUS block
            out.write("begin mrbayes;\n") # Starts block for MrBayes commands
            out.write("  set autoclose=yes nowarn=yes;\n") # Sets MrBayes to suppress warnings and to automatically close at the end of execution 
            out.write("  lset nst=6 rates=gamma;\n") # Defines model as GTR+G
            out.write("  prset ratepr=variable;\n") # Allows tax to vary between partitions
            out.write("  mcmcp ngen=2000000 samplefreq=1000 nchains=4 temp=0.2 printfreq=1000 diagnfreq=10000 burninfrac=0.25;\n") # Configures MCMC parameters (2M generations, 4 chains, 1K frequence, 25% burn-in)
            out.write("  mcmc;\n  sumt;\nend;\n") # Runs MCMC and summarizes the results

        print(f"[OK] Exported {gene} to .phy and .nex") # Prints a success message


def concatenate_alignments():
    """
    Concatenates selected aligned gene sequences from the 'aligned' directory into a single PHYLIP and 
    NEXUS file in the 'nexus' directory with MrBayes commands and partition information. A separate
    parition file is also generated for use with RAxML-NG.
    """
    aligned_dir = "aligned" # Input directory
    output_dir = "nexus" # Output directory
    os.makedirs(output_dir, exist_ok=True) # Makes directory if non existent

    available = [f for f in os.listdir(aligned_dir) if f.endswith("_cleaned.fasta")] # Lists all ".fasta" clean files in input directory
    genes = [f.replace("_cleaned.fasta", "") for f in available] # Removes "_cleaned.fasta" suffix

    print("Available aligned genes:")
    for i, g in enumerate(genes, 1):
        print(f"{i}. {g}") # Prints message with the available genes and their respective numeration

    selected_input = input("Enter gene names to concatenate (space-separated, e.g., '16S ND4 RAG1'): ") # Requests the user for the genes desired to concatenate
    selected_genes = selected_input.strip().split()
    print(f"\nSelected genes for concatenation: {', '.join(selected_genes)}") # Shows selected genes

    alignments = {} # Dictionary for gene alignments
    gene_lengths = {} # Dictionary for gene length
    all_taxa = set() # Set with all found taxa

    for gene in selected_genes: # Verifies if file exists
        filename = f"{gene}_cleaned.fasta"
        path = os.path.join(aligned_dir, filename)
        if not os.path.exists(path):
            print(f"[ERROR] File not found: {path}") # Error message if file not found
            exit(1) # Exits program

        aln = AlignIO.read(path, "fasta") # Reads alignment
        alignments[gene] = aln # Stores gene
        gene_lengths[gene] = aln.get_alignment_length() # Stores the gene length
        all_taxa.update(rec.id for rec in aln) # Stores taxa ID

    records = [] # List for concatenated records
    for taxon in sorted(all_taxa): # Sorts taxa
        seq_concat = ""
        for gene in selected_genes:
            rec = next((r for r in alignments[gene] if r.id == taxon), None)
            if rec:
                seq_concat += str(rec.seq) # Adds sequence to list if taxa exists
            else:
                print(f"[!] {taxon} missing in {gene}, filling with gaps.") # Adds gaps to list if taxa is absent
                seq_concat += "-" * gene_lengths[gene]
        records.append(SeqRecord(Seq(seq_concat), id=taxon, description="")) # Creates a SeqRecord for concatenated taxa and adds it to the list

    records = make_unique_ids(records) # Runs function earlier defined to guarantee unique IDs
    alignment = MultipleSeqAlignment(records) # Converts list to MultipleSeqAlignment object

    phylip_out = os.path.join(output_dir, "concatenated.phy")
    AlignIO.write(alignment, phylip_out, "phylip-relaxed")
    print(f"[OK] PHYLIP file saved at {phylip_out}") # Prints message of success with the PHYLIP output file the concatenation has been saved to

    nexus_out = os.path.join(output_dir, "concatenated.nex")
    with open(nexus_out, "w") as out: # Opens NEXUS file for writing functions
        out.write("#NEXUS\n\nBegin data;\n")
        out.write(f"  Dimensions ntax={len(alignment)} nchar={alignment.get_alignment_length()};\n")
        out.write("  Format datatype=dna missing=? gap=- interleave=no;\n")
        out.write("  Matrix\n") # Writes pattern NEXUS header
        for record in alignment:
            seq = str(record.seq).upper()
            cleaned = ''.join(c if c in VALID_DNA else 'N' for c in seq)
            out.write(f"{record.id:<25} {cleaned}\n") # Writes the formatted sequences, replacing invalid characters
        out.write("  ;\nEnd;\n\n") # Finishes the data block

        out.write("begin mrbayes;\n  set autoclose=yes nowarn=yes;\n") # Starts MrBayes block
        positions = {} # Dictionary with gene positions
        start = 1 # Sets the starting point at 1
        for gene in selected_genes:
            end = start + gene_lengths[gene] - 1
            positions[gene] = (start, end)
            out.write(f"  charset {gene} = {start}-{end};\n")
            start = end + 1 # Calculates each gene's interval and defines "charsets" for partition
        out.write(f"  partition genes = {len(selected_genes)}: " + ", ".join(selected_genes) + ";\n") # Creates gene partition
        out.write("  set partition=genes;\n") # Applies the gene partition
        out.write("  lset applyto=(all) nst=6 rates=gamma;\n")
        out.write("  prset applyto=(all) ratepr=variable;\n")
        out.write("  mcmcp ngen=2000000 samplefreq=1000 nchains=4 temp=0.2 printfreq=1000 diagnfreq=10000 burninfrac=0.25;\n")
        out.write("  mcmc;\n  sumt;\nend;\n") # Defines MCMC and MrBayes parameters earlier mentioned

    print(f"[OK] NEXUS file with MrBayes block saved at {nexus_out}") # Confirms the NEXUS file successful save

    partition_txt = os.path.join(output_dir, "concatenated.partition.txt") # Creates file with partitions
    with open(partition_txt, "w") as pfile: # Opens file for writing functions
        for gene in selected_genes:
            start, end = positions[gene]
            pfile.write(f"DNA, {gene} = {start}-{end}\n") # Writes gene for RAxML-NG later use
    print(f"[OK] Partition file for RAxML-NG saved at {partition_txt}") # Confirms export of resulting file


if __name__ == "__main__":

    user_input = input("What operation do you want? Export individual (i), concatenate (c), or both (b)? [i/c/b]: ").strip().lower() # Asks user what operation they desire to run
    if user_input == 'c':
        concatenate_alignments() # If "c", runs concatenate_alignments function
    elif user_input == 'i':
        export_individual_alignments() # If "i", runs export_individual_alignments function
    elif user_input == 'b':
        export_individual_alignments()
        concatenate_alignments() # If "b", runs export_individual_alignments and concatenate_alignments functions
    else:
        print("[INFO] Operation aborted by user.") # If the user writes something else, a message is shown and no functions are executed
   
