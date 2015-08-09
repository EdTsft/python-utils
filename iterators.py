"""Iterator utilities"""

class LengthError(ValueError):
    pass

def get_and_ensure_single(iterator):
    """Return the single element contained in iterator.

    Raises LengthError if the iterator does not contain exactly 1 element.
    Consumes up to 2 elements from iterator.
    """
    is_length_one, elements = get_and_check_size(iterator, 1)
    if not is_length_one:
        raise LengthError("Iterator does not contain exactly one element.")
    return elements[0]


def get_and_check_size(iterator, n):
    """Check if the iterator is length n and return consumed elements.

    Consumes the next n+1 elements if possible (up to the end of the iterator).
    Returns (is_length_n, elems)
    """
    elements = []
    try:
        for _ in range(n):
            elements.append(next(iterator))
    except StopIteration:
        return False, elements

    try:
        elements.append(next(iterator))
        return False, elements
    except StopIteration:
        pass

    assert(len(elements) == n)
    return True, elements
