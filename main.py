import argparse

from primer import construct_primers
from temp import calculate_tm
from len import get_length


def fmt_tm_print(forward_tm: float, forward_ta: float, reverse_tm: float, reverse_ta: float) -> None:
    print("")
    print("="*60)
    print("Melting Temperature (Tm) of the forward primer: " + '\033[94m' + '\033[1m' + f"{forward_tm:.2f}" + " °C" + '\033[0m' + '\033[0m')
    print("Annealing Temperature (Ta) of the forward primer: " + '\033[94m' + '\033[1m' + f"{forward_ta:.2f}" + " °C" + '\033[0m' + '\033[0m')
    print("-"*60)
    print("Melting Temperature (Tm) of the reverse primer: " + '\033[94m' + '\033[1m' + f"{reverse_tm:.2f}" + " °C" + '\033[0m' + '\033[0m')
    print("Annealing Temperature (Ta) of the reverse primer: " + '\033[94m' + '\033[1m' + f"{reverse_ta:.2f}" + " °C" + '\033[0m' + '\033[0m')
    print("="*60)
    print("")
    print(
        '\033[91m' +\
        '\033[1m' +\
        "Note:\n" +\
        " - These temperature values are estimates and should be experimentally validated" +\
        '\033[0m' +\
        '\033[0m'
    )
    print("")

def fmt_len_print(pcr_product_length: int) -> None:
    print("")
    print("="*60)
    print("Length of PCR product: " + '\033[94m' + '\033[1m' + f"{pcr_product_length}" + " bp" + '\033[0m' + '\033[0m')
    print("="*60)
    print("")
    print(
        '\033[91m' +\
        '\033[1m' +\
        "Note:\n" +\
        " - If the `all` argument is used, the length produced will not include additional bases required for efficient restriction enzyme cutting\n" +\
        " - This script assumes the appropriate primers and sequences are inputted\n" +\
        " - Capitalization and spaces should not matter" +\
        '\033[0m' +\
        '\033[0m'
    )
    print("")

def fmt_primer_print(forward_primer: str, reverse_primer: str) -> None:
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
    print("")


def main():
    parser = argparse.ArgumentParser(description="Primer Design Utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for primer generation
    primer_parser = subparsers.add_parser("primer", help="Construct forward and reverse primer sequences.")
    primer_parser.add_argument("--seq", dest="input_string", required=True,
                        help="Input full DNA sequence (5' to 3') of target gene.")
    primer_parser.add_argument("--nmer", dest="nmer", type=int, required=True,
                        help="Length of the DNA to be added to the primers.")
    primer_parser.add_argument("--forward-re", dest="forward_re_site", required=True,
                        help="Sequence of the RE site (5' to 3') of the forward primer.")
    primer_parser.add_argument("--reverse-re", dest="reverse_re_site", required=True,
                        help="Sequence of the RE site (5' to 3') of the reverse primer.")
    primer_parser.add_argument("--forward-tag", dest="forward_tag", required=False,
                        help="Additional tag sequence for the forward primer.")
    primer_parser.add_argument("--reverse-tag", dest="reverse_tag", required=False,
                        help="Additional tag sequence for the reverse primer.")

    # Subparser for Tm calculation
    tm_parser = subparsers.add_parser("temp", help="Calculate the melting temperature (Tm) and annealing temperature (Ta) of a given primer sequence.")
    tm_parser.add_argument("--forward", dest="forward_primer", required=True,
                           help="Input full DNA sequence (5' to 3') of the forward primer.")
    tm_parser.add_argument("--reverse", dest="reverse_primer", required=True,
                           help="Input full DNA sequence (5' to 3') of the reverse primer.")
    tm_parser.add_argument("--nmer", dest="nmer", type=int, required=True,
                           help="Length of the DNA segment from the 3' end to consider for Tm calculation.")

    # Subparser for length calculation
    len_parser = subparsers.add_parser("len", help="Output the length of a given DNA sequence.")
    len_parser.add_argument("--seq", dest="input_string", required=True,
                            help="Input full DNA sequence (5' to 3') of target gene.")
    len_parser.add_argument("--forward", dest="forward_primer", required=True,
                            help="Forward primer sequence (5' to 3').")
    len_parser.add_argument("--reverse", dest="reverse_primer", required=True,
                            help="Reverse primer sequence (5' to 3').")
    
    # Subparser for all available functions
    all_parser = subparsers.add_parser("all", help="Run all available functions with the provided inputs.")
    all_parser.add_argument("--seq", dest="input_string", required=True,
                            help="Input full DNA sequence (5' to 3') of target gene.")
    all_parser.add_argument("--nmer", dest="nmer", type=int, required=True,
                            help="Length of the DNA to be added to the primers or considered for Tm calculation.")
    all_parser.add_argument("--forward-re", dest="forward_re_site", required=True,
                            help="Sequence of the RE site (5' to 3') of the forward primer.")
    all_parser.add_argument("--reverse-re", dest="reverse_re_site", required=True,
                            help="Sequence of the RE site (5' to 3') of the reverse primer.")
    all_parser.add_argument("--forward-tag", dest="forward_tag", required=False,
                            help="Additional tag sequence for the forward primer.")
    all_parser.add_argument("--reverse-tag", dest="reverse_tag", required=False,
                            help="Additional tag sequence for the reverse primer.")

    args = parser.parse_args()

    if args.command == "temp":
        forward_primer: str = "".join(args.forward_primer.upper().split())
        reverse_primer: str = "".join(args.reverse_primer.upper().split())

        forward_tm = calculate_tm(forward_primer, args.nmer)
        reverse_tm = calculate_tm(reverse_primer, args.nmer)
        forward_ta = forward_tm - 5
        reverse_ta = reverse_tm - 5

        fmt_tm_print(forward_tm, forward_ta, reverse_tm, reverse_ta)
    
    elif args.command == "len":
        target_seq: str = "".join(args.input_string.upper().split())
        forward_primer: str = "".join(args.forward_primer.upper().split())
        reverse_primer: str = "".join(args.reverse_primer.upper().split())
        
        pcr_product_length = get_length(target_seq, forward_primer, reverse_primer)

        fmt_len_print(pcr_product_length)
    elif args.command == "primer":
        target_seq: str = "".join(args.input_string.upper().split())
        forward_re_site: str = args.forward_re_site.upper()
        reverse_re_site: str = args.reverse_re_site.upper()
        forward_tag: str = "".join(args.forward_tag.upper().split()) if args.forward_tag else ""
        reverse_tag: str = "".join(args.reverse_tag.upper().split()) if args.reverse_tag else ""
        
        forward_primer, reverse_primer = construct_primers(target_seq, args.nmer, forward_re_site, reverse_re_site, forward_tag, reverse_tag)

        fmt_primer_print(forward_primer, reverse_primer)
    elif args.command == "all":
        target_seq: str = "".join(args.input_string.upper().split())
        forward_re_site: str = args.forward_re_site.upper()
        reverse_re_site: str = args.reverse_re_site.upper()
        forward_tag: str = "".join(args.forward_tag.upper().split()) if args.forward_tag else ""
        reverse_tag: str = "".join(args.reverse_tag.upper().split()) if args.reverse_tag else ""
        
        forward_primer, reverse_primer = construct_primers(target_seq, args.nmer, forward_re_site, reverse_re_site, forward_tag, reverse_tag)

        fmt_primer_print(forward_primer, reverse_primer)

        forward_tm = calculate_tm(forward_primer, args.nmer)
        reverse_tm = calculate_tm(reverse_primer, args.nmer)
        forward_ta = forward_tm - 5
        reverse_ta = reverse_tm - 5

        fmt_tm_print(forward_tm, forward_ta, reverse_tm, reverse_ta)

        pcr_product_length = get_length(target_seq, forward_primer, reverse_primer)

        fmt_len_print(pcr_product_length)

if __name__ == "__main__":
    main()