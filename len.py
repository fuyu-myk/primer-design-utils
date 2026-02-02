import argparse


def get_length(target_seq: str, forward_primer: str, reverse_primer: str) -> int:
    """
    Calculate the length of the PCR product given the target sequence and primers.

    Args:
        target_seq (str): The DNA sequence of the target gene.
        forward_primer (str): The sequence of the forward primer.
        reverse_primer (str): The sequence of the reverse primer.
    """
    
    pcr_product = forward_primer + target_seq + reverse_primer
    return len(pcr_product)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Output the length of a given DNA sequence.")
    parser.add_argument("--seq", dest="input_string", required=True,
                        help="Input full DNA sequence (5' to 3') of target gene.")
    parser.add_argument("--forward", dest="forward_primer", required=True,
                        help="Forward primer sequence (5' to 3').")
    parser.add_argument("--reverse", dest="reverse_primer", required=True,
                        help="Reverse primer sequence (5' to 3').")
    args = parser.parse_args()

    target_seq: str = "".join(args.input_string.upper().split())
    forward_primer: str = "".join(args.forward_primer.upper().split())
    reverse_primer: str = "".join(args.reverse_primer.upper().split())
    
    pcr_product_length = get_length(target_seq, forward_primer, reverse_primer)

    print("")
    print("="*60)
    print("Length of PCR product: " + '\033[94m' + '\033[1m' + f"{pcr_product_length}" + " bp" + '\033[0m' + '\033[0m')
    print("="*60)
    print("")
    print(
        '\033[91m' +\
        '\033[1m' +\
        "Note:\n" +\
        " - This script assumes the appropriate primers and sequences are inputted\n" +\
        " - Capitalization and spaces should not matter" +\
        '\033[0m' +\
        '\033[0m'
    )