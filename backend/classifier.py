
def classify_species(parsed):
    """
    parsed: dict of element counts OR raw string
    Heuristic: if parsed dict has length 1, treat as element; otherwise compound.
    """
    if isinstance(parsed, dict) and len(parsed)==1:
        return "element"
    return "compound"
