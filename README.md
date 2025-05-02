
<p align="center">
<a href="https://www.python.org/" title="Go to Python homepage"><img src="https://img.shields.io/badge/Made%20with-Python-FED564?logo=python&amp;logoColor=white" alt="Made with Python"></a>
<a href="https://www.ncbi.nlm.nih.gov/books/NBK25500/" title="Entrez API Documentation">
  <img src="https://img.shields.io/badge/Powered%20by-Entrez%20API-FED564?logo=databricks&logoColor=white" alt="Powered by Entrez API">
</a>
</p>

<p align="center">
  <h3 align="center">🔬 PhyloPipeline - Automated Phylogenetic Workflow</h3>
This project is a modular and automated pipeline for retrieving, processing, aligning, and inferring phylogenetic trees from genetic data. It integrates sequence retrieval from NCBI using the Entrez API, alignment with MAFFT, ID cleaning, and tree inference using RAxML-NG and MrBayes.
</p>

---

## Authors
A group of 4 students from ESTBarreiro with their school id number assigned.
- Bianca Silva, 202300273
- Erica Alaiz, 202300154
- Filipa Fernandes, 202300218
- Melissa Rocha, 202101023

---

## 📋 Index

- [📝 Introduction](#-introduction)
- [⚙️ Features](#-features)
- [💻 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📜 License](#-license)

---

## 📝 Introduction

This pipeline automates the process of retrieving sequences from GenBank, aligning them, cleaning headers, generating individual and concatenated alignments, and constructing phylogenetic trees using both maximum likelihood and Bayesian inference methods.

The pipeline was created to perform the phylogenetic study of the following article:
**"Phylogeny and biogeography of the African burrowing snake subfamily Aparallactinae (Squamata: Lamprophiidae)"**
Available at: [https://www.sciencedirect.com/science/article/pii/S1055790317301999](https://www.sciencedirect.com/science/article/pii/S1055790317301999)

---

## ⚙️ Features

- 📂 Organizes sequences by gene and species
- 🛠️ Aligns sequences with MAFFT
- ✨ Cleans FASTA headers and generates mapping CSVs
- 🔠 Generates individual and concatenated alignments
- 🌳 Builds trees with RAxML-NG and MrBayes
- 📝 Prompts user interaction for flexible control
- 📚 Structured and modular Python scripts for automation

---

## 💻 Installation

### Prerequisites
- Python 3.10+
- MAFFT
- RAxML-NG
- MrBayes
- Biopython

### Installation Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/Polytechnic-Projects/Phylogenetic_Pipeline.git
   cd Phylogenetic_Pipeline
   ```

2. Install dependencies:
   ```sh
   pip install biopython
   ```

---

## 🚀 Usage

### Run the pipeline:
```sh
python3 main_pipeline.py
```

The script will prompt you for the following:
- Whether to align sequences
- Whether to export individual/concatenated alignments
- Which phylogenetic trees to generate (RAxML-NG and/or MrBayes)
- Model and thread options for RAxML

### File Organization
- `fasta_sequences/` - Raw FASTA sequences.
- `aligned/` - Aligned and cleaned gene sequences. Also the csv files.
- `individual/` - Nexus and PHYLIP files per gene.
- `nexus/` - Concatenated NEXUS and PHYLIP files. Also MrBayes tree outputs.
- `trees/raxml/` - RAxML-NG tree outputs.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### 🔗 References
- [NCBI Entrez API](https://www.ncbi.nlm.nih.gov/books/NBK25500/)
- [MAFFT](https://mafft.cbrc.jp/alignment/software/)
- [RAxML-NG](https://github.com/amkozlov/raxml-ng)
- [MrBayes](https://nbisweden.github.io/MrBayes/)
- [Biopython](https://biopython.org/)
- Original Article: [https://www.sciencedirect.com/science/article/pii/S1055790317301999](https://www.sciencedirect.com/science/article/pii/S1055790317301999)
