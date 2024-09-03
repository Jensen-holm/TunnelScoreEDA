def euclidean_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """returns the euclidean distance between two points (x1, y1), (x2, y2)"""
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
