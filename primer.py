import argparse


def reverse(str: str) -> str:
    """
    Return the reverse of the input DNA sequence.

    Args:
        str (str): Input DNA sequence.
    """
    
    return str[::-1]

def complement(str: str) -> str:
    """
    Return the complement of the input DNA sequence.

    Args:
        str (str): Input DNA sequence.
    """

    complement_map = str.maketrans("ATCGatcg", "TAGCtagc")

    return str.translate(complement_map)

def construct_forward_primer(sequence: str, nmer: int, forward_re_site: str, forward_tag: str) -> str:
    """
    Construct the forward primer sequence.

    Args:
        sequence (str): Target DNA sequence.
        nmer (int): Number of nucleotides from the 5' end to include.
        forward_re_site (str): Restriction enzyme site for the forward primer.
        forward_tag (str): Additional tag sequence for the forward primer.
    """

    if nmer > len(sequence):
        raise ValueError("nmer cannot be greater than the length of the target sequence.")

    nmer_sequence = sequence[:nmer]
    forward_primer = forward_re_site + forward_tag + nmer_sequence

    return forward_primer

def construct_reverse_primer(sequence: str, nmer: int, reverse_re_site: str, reverse_tag: str) -> str:
    """
    Construct the reverse primer sequence.

    Args:
        sequence (str): Target DNA sequence.
        nmer (int): Number of nucleotides from the 3' end to include.
        reverse_re_site (str): Restriction enzyme site for the reverse primer.
        reverse_tag (str): Additional tag sequence for the reverse primer.
    """

    if nmer > len(sequence):
        raise ValueError("nmer cannot be greater than the length of the target sequence.")

    nmer_sequence = sequence[-nmer:]
    nmer_complement = complement(nmer_sequence)
    nmer_reverse_complement = reverse(nmer_complement)
    reverse_primer = reverse_re_site + reverse(reverse_tag) + nmer_reverse_complement

    return reverse_primer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Edit a given DNA sequence.")
    parser.add_argument("--seq", dest="input_string", required=True,
                        help="Input full DNA sequence (5' to 3') of target gene.")
    parser.add_argument("--nmer", dest="nmer", type=int, required=True,
                        help="Length of the DNA to be added to the primers.")
    parser.add_argument("--forward-re", dest="forward_re_site", required=True,
                        help="Sequence of the RE site (5' to 3') of the forward primer.")
    parser.add_argument("--reverse-re", dest="reverse_re_site", required=True,
                        help="Sequence of the RE site (5' to 3') of the reverse primer.")
    parser.add_argument("--forward-tag", dest="forward_tag", required=False,
                        help="Additional tag sequence for the forward primer.")
    parser.add_argument("--reverse-tag", dest="reverse_tag", required=False,
                        help="Additional tag sequence for the reverse primer.")
    args = parser.parse_args()

    target_seq: str = "".join(args.input_string.upper().split())
    forward_re_site: str = args.forward_re_site.upper()
    reverse_re_site: str = args.reverse_re_site.upper()
    forward_tag: str = "".join(args.forward_tag.upper().split()) if args.forward_tag else ""
    reverse_tag: str = "".join(args.reverse_tag.upper().split()) if args.reverse_tag else ""
    
    forward_primer = construct_forward_primer(target_seq, args.nmer, forward_re_site, forward_tag)
    reverse_primer = construct_reverse_primer(target_seq, args.nmer, reverse_re_site, reverse_tag)

    print("")
    print("="*60)
    print("Generated Primer Sequences")
    print("="*60)
    print("")
    print(f"Forward Primer:\n{forward_primer}")
    print("")
    print(f"Reverse Primer:\n{reverse_primer}")
    print("")
    print(
        '\033[91m' +\
        '\033[1m' +\
        "Note:\n" +\
        " - Primers are shown in 5' to 3' direction\n" +\
        " - Primer sequences do not include the additional bases required for efficient restriction enzyme cutting" +\
        '\033[0m' +\
        '\033[0m'
    )