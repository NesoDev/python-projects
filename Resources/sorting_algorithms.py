def quickSort(values: list, attribute: str = ""):
    if len(values) <= 1:
        return values
    pivot = getattr(values[0], attribute) if attribute != "" else values[0]
    left = (
        [x for x in values[1:] if getattr(x, attribute) < pivot]
        if attribute != ""
        else [x for x in values[1:] if x < pivot]
    )
    right = (
        [x for x in values[1:] if getattr(x, attribute) >= pivot]
        if attribute != ""
        else [x for x in values[1:] if x >= pivot]
    )
    return quickSort(left, attribute) + [values[0]] + quickSort(right, attribute)