def select_halfcycles(data, number, select_range=None):
    """
    Returns input data with only the selected halfcycle numbers.
    number can be integer og list of integers.
    Range is a tuple of integers, or list of tuples of integers.
    """

    selected = {}
    halfcycles_to_catch = []
    if isinstance(number, int):
        halfcycles_to_catch.append(number)
    elif isinstance(number, list):
        for num in number:
            if num not in halfcycles_to_catch:
                halfcycles_to_catch.append(num)

    if isinstance(select_range, tuple):
        for num in range(
            select_range[0], select_range[1] + 1
        ):  # Including last element
            if num not in halfcycles_to_catch:
                halfcycles_to_catch.append(num)
    elif isinstance(select_range, list):
        for selected_range in select_range:
            for num in range(
                selected_range[0], selected_range[1] + 1
            ):  # Including last element
                if num not in halfcycles_to_catch:
                    halfcycles_to_catch.append(num)

    for i, (key, value) in enumerate(data.items()):
        if i + 1 in halfcycles_to_catch:
            selected[key] = value
    return selected
