import polars as pl

__all__ = ["pl_euclidean_distance"]


def pl_euclidean_distance(
    x1: pl.Expr,
    y1: pl.Expr,
    x2: pl.Expr,
    y2: pl.Expr,
) -> pl.Expr:
    """returns the euclidean distance between two points (x1, y1), (x2, y2)"""
    return ((x1 - x2) ** 2) + ((y1 - y2) ** 2) ** 0.5
