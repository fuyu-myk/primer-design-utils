# Primer design utils

This project provides basic scripts that aim to reduce the complexity of primer design. Template commands are provided for ease of use. The scripts provided by no means cover all aspects of primer design, and users are advised to perform due diligence when designing primers for their experiments.

A useful site to check for primer validity is [NCBI's Primer-BLAST](https://www.ncbi.nlm.nih.gov/tools/primer-blast/).

## Usage instructions

1. Clone/download this repository to your local machine
2. Ensure you have [Python 3](https://www.python.org/downloads/) installed on your machine
3. Open a terminal and navigate to the directory where the scripts are located
4. Run the scripts using the template commands provided below, filling in the required parameters

## What each script does

**[main.py](main.py)**: Main script that combines the functionalities of all other scripts. Use this script to access all functionalities in one place.

This script calls the other scripts based on the subcommand provided. The subcommands are as follows:

- `primer`: Calls the [primer.py](primer.py) script for non-mutation primers
- `mut-primer`: Calls the [primer.py](primer.py) script for mutation primers
- `len`: Calls the [len.py](len.py) script
- `temp`: Calls the [temp.py](temp.py) script
- `all`: Calls all three scripts in sequence

> [!NOTE]
> When using the `all` subcommand, ensure that the parameters provided are valid for all scripts to prevent undefined behavior.
> I.e., the disclaimers for each individual script still apply.

Template command to call all functionalities (tags are optional):

```bash
python main.py all \
--seq "" \
--seq-b "" \
--mut "" \
--nmer  \
--forward-re "" \
--reverse-re "" \
--forward-tag "" \
--reverse-tag ""
```

**[primer.py](primer.py)**: Outputs the forward and reverse primers with the given parameters

This module requires the following parameters:

- `--seq`: Full target coding sequence (5' - 3')
- `--seq-b`: Full target coding sequence of the other target gene (5' - 3') (if any)
- `--nmer`: Number corresponding to number of complementary nucleotides to the target sequence in the primer
- `--mut`: The mutation sequence (5' - 3'), i.e. extra bases to be introduced between target sequences (if any)
- `--forward-re`: The restriction site sequence (5' - 3') of the restriction enzyme of choice for the forward primer
- `--reverse-re`: The restriction site sequence (5' - 3') of the restriction enzyme of choice for the reverse primer
- `--forward-tag`: The sequence of the tag of the forward primer (if any)
- `--reverse-tag`: The sequence of the tag of the reverse primer (if any)

> [!NOTE]
> This script does not check for the validity of the RE site sequences provided. Due diligence is required to ensure that the RE sites are valid.

Template command for single/double sequences (seq-b, mut and tags are optional):

```bash
python main.py primer \
--seq "" \
--seq-b "" \
--nmer  \
--mut "" \
--forward-re "" \
--reverse-re "" \
--forward-tag "" \
--reverse-tag ""
```

Template command for mutation primers (mut is required):

```bash
python main.py mut-primer \
--seq "" \
--nmer  \
--pos  \
--mut "" \
```

**[len.py](len.py)**: Outputs the length of the PCR product given the target sequence and primers

This module requires the following parameters:

- `--seq`: Full target coding sequence
- `--seq-b`: Full target coding sequence of the other target gene (5' - 3') (if any)
- `--mut-primer`: Full sequence of the forward mutation primer (if any)
- `--forward-primer`: Full sequence of the forward primer
- `--reverse-primer`: Full sequence of the reverse primer
- `--nmer`: Number corresponding to number of complementary nucleotides to the target sequence in the primer

Template command:

```bash
python main.py len \
--seq "" \
--seq-b "" \
--mut-primer "" \
--forward "" \
--reverse "" \
--nmer 
```

**[temp.py](temp.py)**: Outputs the melting and annealing temperature of a given primer sequence

This module requires the following parameters:

- `--primer`: Full sequence of the primer (5' - 3')
- `--nmer`: Number corresponding to number of complementary nucleotides to the target sequence in the primer

Template command:

```bash
python main.py temp \
--forward "" \
--reverse "" \
--nmer 
```

## Useful sites

- [NCBI's Nucleotide Database](https://www.ncbi.nlm.nih.gov/nuccore/)
- [NCBI's Gene Database](https://www.ncbi.nlm.nih.gov/gene/)
- [NCBI's Primer-BLAST](https://www.ncbi.nlm.nih.gov/tools/primer-blast/)
- [RE finder](https://enzymefinder.neb.com/)
- [NEBcutter](https://nc3.neb.com/NEBcutter/)
