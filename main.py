import argparse

from primer import construct_mutation_primers_single, construct_primers
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
        " - For mutation primers, please ensure that the position and mutation sequences are correct" +\
        '\033[0m' +\
        '\033[0m'
    )
    print("")

def fmt_primer_mutation_print(forward_primer: str, mut_reverse_primer: str, mut_forward_primer: str, reverse_primer: str) -> None:
    print("")
    print("="*60)
    print("Generated Primer Sequences")
    print("="*60)
    print("")
    print(f"Forward Primer:\n{forward_primer}")
    print("")
    print(f"Mutation Reverse Primer:\n{mut_reverse_primer}")
    print("")
    print(f"Mutation Forward Primer:\n{mut_forward_primer}")
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
    primer_parser.add_argument("--seq-b", dest="input_string_b", required=False,
                        help="Input full DNA sequence (5' to 3') of target gene B (for mutation primers).")
    primer_parser.add_argument("--nmer", dest="nmer", type=int, required=True,
                        help="Length of the DNA to be added to the primers.")
    primer_parser.add_argument("--mut", dest="mut", required=False,
                        help="The sequence of the mutation to be introduced in the primers.")
    primer_parser.add_argument("--forward-re", dest="forward_re_site", required=True,
                        help="Sequence of the RE site (5' to 3') of the forward primer.")
    primer_parser.add_argument("--reverse-re", dest="reverse_re_site", required=True,
                        help="Sequence of the RE site (5' to 3') of the reverse primer.")
    primer_parser.add_argument("--forward-tag", dest="forward_tag", required=False,
                        help="Additional tag sequence for the forward primer.")
    primer_parser.add_argument("--reverse-tag", dest="reverse_tag", required=False,
                        help="Additional tag sequence for the reverse primer.")
    
    # Subparser for mutation primer generation
    mut_primer_parser = subparsers.add_parser("mut-primer", help="Construct mutation primer pair, given a single sequence and mutation position.")
    mut_primer_parser.add_argument("--seq", dest="seq", required=True,
                        help="Input full DNA sequence (5' to 3') of target gene A.")
    mut_primer_parser.add_argument("--nmer", dest="nmer", type=int, required=True,
                        help="Length of the DNA to be added to the primers.")
    mut_primer_parser.add_argument("--pos", dest="pos", type=int, required=True,
                        help="Position of the mutation in the sequence, e.g. F64L; pos = 64.")
    mut_primer_parser.add_argument("--mut", dest="mut", required=True,
                        help="The sequence of the mutation to be introduced in the primers.")

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
    len_parser.add_argument("--seq-b", dest="input_string_b", required=False,
                            help="Input full DNA sequence (5' to 3') of target gene B (for mutation primers).")
    len_parser.add_argument("--mut-primer", dest="mut_primer", required=False,
                            help="Input full DNA sequence (5' to 3') of the mutation primer (for mutation primers).")
    len_parser.add_argument("--forward", dest="forward_primer", required=True,
                            help="Forward primer sequence (5' to 3').")
    len_parser.add_argument("--reverse", dest="reverse_primer", required=True,
                            help="Reverse primer sequence (5' to 3').")
    len_parser.add_argument("--nmer", dest="nmer", type=int, required=True,
                           help="Length of the DNA to be added to the primers.")
    
    # Subparser for all available functions
    all_parser = subparsers.add_parser("all", help="Run all available functions with the provided inputs.")
    all_parser.add_argument("--seq", dest="input_string", required=True,
                            help="Input full DNA sequence (5' to 3') of target gene.")
    all_parser.add_argument("--seq-b", dest="input_string_b", required=False,
                            help="Input full DNA sequence (5' to 3') of target gene B (for mutation primers).")
    all_parser.add_argument("--mut", dest="mut", required=False,
                            help="The sequence of the mutation to be introduced in the primers.")
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

        if args.nmer > len(forward_primer):
            raise ValueError("nmer cannot be greater than the length of the forward primer sequence.")

        forward_tm = calculate_tm(forward_primer, args.nmer)
        reverse_tm = calculate_tm(reverse_primer, args.nmer)
        forward_ta = forward_tm - 5
        reverse_ta = reverse_tm - 5

        fmt_tm_print(forward_tm, forward_ta, reverse_tm, reverse_ta)
    
    elif args.command == "len":
        target_seq: str = "".join(args.input_string.upper().split())
        target_seq_b: str = "".join(args.input_string_b.upper().split()) if args.input_string_b else ""
        forward_primer: str = "".join(args.forward_primer.upper().split())
        reverse_primer: str = "".join(args.reverse_primer.upper().split())
        forward_mutation_primer: str = "".join(args.mut_primer.upper().split()) if args.mut_primer else ""

        if target_seq_b == "" and forward_mutation_primer != "":
            raise ValueError("Mutation primer should not be provided when only one sequence is given.")
        
        if target_seq_b != "" and forward_mutation_primer == "":
            raise ValueError("Mutation primer must be provided when two sequences are given.")
        
        pcr_product_length = get_length(
            target_seq,
            target_seq_b,
            forward_primer,
            reverse_primer,
            forward_mutation_primer,
            args.nmer
        )

        fmt_len_print(pcr_product_length)
    elif args.command == "primer":
        target_seq: str = "".join(args.input_string.upper().split())
        target_seq_b: str = "".join(args.input_string_b.upper().split()) if args.input_string_b else ""
        forward_re_site: str = "".join(args.forward_re_site.upper().split())
        reverse_re_site: str = "".join(args.reverse_re_site.upper().split())
        forward_tag: str = "".join(args.forward_tag.upper().split()) if args.forward_tag else ""
        reverse_tag: str = "".join(args.reverse_tag.upper().split()) if args.reverse_tag else ""
        mut: str = "".join(args.mut.upper().split()) if args.mut else ""

        if mut != "" and target_seq_b == "":
            raise ValueError("For mutation primers, sequence B must be provided.")
        
        if target_seq_b != "" and mut == "":
            raise ValueError("Mutation sequence must be provided when sequence B is given.")
        
        primer_a, primer_b, primer_c, primer_d = construct_primers(
            target_seq,
            target_seq_b,
            mut,
            args.nmer,
            forward_re_site,
            reverse_re_site,
            forward_tag,
            reverse_tag
        )

        if primer_b == "" and primer_c == "":
            fmt_primer_print(primer_a, primer_d)
        else:
            fmt_primer_mutation_print(primer_a, primer_b, primer_c, primer_d)
    elif args.command == "mut-primer":
        mut: str = "".join(args.mut.upper().split())

        if args.pos is None:
            raise ValueError("Position of mutation must be provided when only one sequence is given.")
        
        aa_idx = (args.pos - 1) * 3
        target_a: str = "".join(args.seq[:aa_idx].upper().split())
        target_b: str = "".join(args.seq[aa_idx + 3:].upper().split())

        forward_primer, reverse_primer = construct_mutation_primers_single(target_a, target_b, args.nmer, mut)

        fmt_primer_print(forward_primer, reverse_primer)
            
    elif args.command == "all":
        target_seq: str = "".join(args.input_string.upper().split())
        target_seq_b: str = "".join(args.input_string_b.upper().split()) if args.input_string_b else ""
        mut: str = "".join(args.mut.upper().split()) if args.mut else ""
        forward_re_site: str = "".join(args.forward_re_site.upper().split())
        reverse_re_site: str = "".join(args.reverse_re_site.upper().split())
        forward_tag: str = "".join(args.forward_tag.upper().split()) if args.forward_tag else ""
        reverse_tag: str = "".join(args.reverse_tag.upper().split()) if args.reverse_tag else ""

        if mut != "" and target_seq_b == "":
            raise ValueError("For mutation primers, sequence B must be provided.")
        
        if target_seq_b != "" and mut == "":
            raise ValueError("Mutation sequence must be provided when sequence B is given.")
        
        primer_a, primer_b, primer_c, primer_d = construct_primers(
            target_seq,
            target_seq_b,
            mut,
            args.nmer,
            forward_re_site,
            reverse_re_site,
            forward_tag,
            reverse_tag
        )

        if primer_b == "" and primer_c == "":
            fmt_primer_print(primer_a, primer_d)
        else:
            fmt_primer_mutation_print(primer_a, primer_b, primer_c, primer_d)

        forward_tm = calculate_tm(primer_a, args.nmer)
        reverse_tm = calculate_tm(primer_d, args.nmer)
        forward_ta = forward_tm - 5
        reverse_ta = reverse_tm - 5

        fmt_tm_print(forward_tm, forward_ta, reverse_tm, reverse_ta)

        pcr_product_length = get_length(
            target_seq,
            target_seq_b,
            primer_a,
            primer_d,
            primer_b, 
            args.nmer
        )

        fmt_len_print(pcr_product_length)
            

if __name__ == "__main__":
    main()