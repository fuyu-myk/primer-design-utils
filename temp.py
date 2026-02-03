def calculate_tm(primer: str, nmer: int) -> float:
    """
    Calculate the melting temperature of the primer using the Wallace rule.
    
    Args:
        primer (str): Input primer sequence.
        nmer (int): Length of the DNA segment from the 3' end to consider for Tm calculation.
    """
    
    if nmer > len(primer):
        raise ValueError("nmer cannot be greater than the length of the primer sequence.")

    primer_segment = primer[-nmer:]
    a_count = primer_segment.count('A')
    t_count = primer_segment.count('T')
    c_count = primer_segment.count('C')
    g_count = primer_segment.count('G')

    tm = 2 * (a_count + t_count) + 4 * (c_count + g_count)

    return tm