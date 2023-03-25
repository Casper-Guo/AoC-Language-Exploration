def is_int(input: str) -> bool:
    # extend isdigit to cover negative numbers
    return input.lstrip('-+').isdigit()
