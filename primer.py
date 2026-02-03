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

def construct_primers(sequence: str, nmer: int, forward_re_site: str, reverse_re_site: str, forward_tag: str = "", reverse_tag: str = "") -> tuple[str, str]:
    """
    Construct both forward and reverse primer sequences.

    Args:
        sequence (str): Target DNA sequence.
        nmer (int): Number of nucleotides from each end to include.
        forward_re_site (str): Restriction enzyme site for the forward primer.
        reverse_re_site (str): Restriction enzyme site for the reverse primer.
        forward_tag (str, optional): Additional tag sequence for the forward primer. Defaults to "".
        reverse_tag (str, optional): Additional tag sequence for the reverse primer. Defaults to "".
    """

    forward_primer = construct_forward_primer(sequence, nmer, forward_re_site, forward_tag)
    reverse_primer = construct_reverse_primer(sequence, nmer, reverse_re_site, reverse_tag)

    return forward_primer, reverse_primer