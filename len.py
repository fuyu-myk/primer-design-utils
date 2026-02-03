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