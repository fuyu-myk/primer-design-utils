import argparse


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the melting temperature (Tm) and annealing temperature (Ta) of a given primer sequence.")
    parser.add_argument("--primer", dest="primer_sequence", required=True,
                        help="Input full DNA sequence (5' to 3') of the primer.")
    parser.add_argument("--nmer", dest="nmer", type=int, required=True,
                        help="Length of the DNA segment from the 3' end to consider for Tm calculation.")
    args = parser.parse_args()

    primer_sequence: str = "".join(args.primer_sequence.upper().split())
    
    tm_value = calculate_tm(primer_sequence, args.nmer)
    ta_value = tm_value - 5

    print("")
    print("="*60)
    print("Melting Temperature (Tm) of the primer: " + '\033[94m' + '\033[1m' + f"{tm_value:.2f}" + " °C" + '\033[0m' + '\033[0m')
    print("Annealing Temperature (Ta) of the primer: " + '\033[94m' + '\033[1m' + f"{ta_value:.2f}" + " °C" + '\033[0m' + '\033[0m')
    print("="*60)
    print("")