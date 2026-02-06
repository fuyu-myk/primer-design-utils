def get_length(target_seq_a: str, target_seq_b: str, forward_primer: str, reverse_primer: str, mut_primer: str, nmer: int) -> int:
    """
    Calculate the length of the PCR product given the target sequence and primers.

    Args:
        target_seq (str): The DNA sequence of the target gene.
        forward_primer (str): The sequence of the forward primer.
        reverse_primer (str): The sequence of the reverse primer.
    """
    if target_seq_b == "":
        target_seq = target_seq_a[3 + nmer : -3 - nmer]
        pcr_product = forward_primer + target_seq + reverse_primer

        return len(pcr_product)
    
    target_seq_a = target_seq_a[3 + nmer : -nmer]
    target_seq_b = target_seq_b[nmer : -3 - nmer]

    pcr_product = forward_primer + target_seq_a + mut_primer + target_seq_b + reverse_primer

    return len(pcr_product)