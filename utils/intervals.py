def generate_one_dimension_fractions(limit, start=1):
    """
    Generates fractions like 1/2, 1/3, 1/LIMIT, 2/3, 2/LIMIT and so on.
    """
    interval = xrange(start,  limit + 1)
    for i in interval:
        for j in xrange(start, i):
            yield(j, i)
