#!/usr/bin/env python3

import os  ##For directory and file handling
import subprocess  ##For running external commands

def run_mrbayes(nex_file): ##Function to run MrBayes on a given .nex file
    print(f"[RUNNING] MrBayes: mb {nex_file}")
    subprocess.run(["mb", nex_file])

def main(): ##Asks the user which type of tree(s) to generate
    print("Which MrBayes trees do you want to generate?")
    print("[1] Single-gene trees")
    print("[2] Concatenated tree")
    print("[3] Both")
    choice = input("Enter your choice [1/2/3]: ").strip()

    if choice in ("1", "3"): ##If the user selects gene-by-gene or both options
        input_dir = "individual"
        for file in os.listdir(input_dir):
            if file.endswith(".nex"):
                nex_path = os.path.join(input_dir, file)
                run_mrbayes(nex_path) ##Runs MrBayes

    if choice in ("2", "3"): ##If the user selects concatenated or both options
        nexus_path = os.path.join("nexus", "concatenated.nex")
        if os.path.exists(nexus_path):
            run_mrbayes(nexus_path) ##Run MrBayes on the concatenated alignment
        else:
            print(f"[ERROR] Concatenated nexus file not found at {nexus_path}")

    print("[DONE] MrBayes analysis complete.")

if __name__ == "__main__":  ##Execute the main function if the script is run directly
    main()

