import pandas as pd
from matplotlib import axes
from typing import Optional
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
import seaborn as sns


def plot_strike_zone(
    data: pd.DataFrame,
    title: str = "",
    colorby: str = "pitch_type",
    legend_title: str = "",
    annotation: Optional[str] = None,
    axis: Optional[axes.Axes] = None,
    alpha: Optional[float] = 0.5,
    # hue: Optional[str] = None,
    # player_headshot_img: Optional[np.ndarray] = None,
    cmap: str = "viridis",
    plate_loc_x: str = "plate_x",
    plate_loc_z: str = "plate_z",
) -> axes.Axes:
    """
    Produces a pitches overlaid on a strike zone using StatCast data

    Args:
        data: (pandas.DataFrame)
            StatCast pandas.DataFrame of StatCast pitcher data
        title: (str), default = ''
            Optional: Title of plot
        colorby: (str), default = 'pitch_type'
            Optional: Which category to color the mark with. Can be categorical or continuous.
        legend_title: (str), default = based on colorby
            Optional: Title for the legend or colorbar
        annotation: (str), default = 'pitch_type'
            Optional: What to annotate in the marker. 'pitch_type', 'release_speed', 'effective_speed',
              'launch_speed', or something else in the data
        axis: (matplotlib.axis.Axes), default = None
            Optional: Axes to plot the strike zone on. If None, a new Axes will be created
        hue: (str), default = None
            Optional: Deprecated, use colorby instead
        player_headshot_img: (np.ndarray), default = None
            Optional: Player headshot image
        cmap: (str), default = 'viridis'
            Optional: Colormap to use for continuous variables
    Returns:
        A matplotlib.axes.Axes object that was used to generate the pitches overlaid on the strike zone
    """

    # some things to auto adjust formatting
    alpha_markers = min(0.8, 0.5 + 1 / data.shape[0]) if alpha is None else alpha
    alpha_text = alpha_markers + 0.2

    # define Matplotlib figure and axis
    if axis is None:
        _, axis = plt.subplots(figsize=(10, 10))

    assert axis is not None

    # add home plate to plot
    home_plate_coords = [[-0.71, 0], [-0.85, -0.5], [0, -1], [0.85, -0.5], [0.71, 0]]
    axis.add_patch(
        patches.Polygon(
            home_plate_coords, edgecolor="darkgray", facecolor="lightgray", zorder=0.1
        )
    )

    # add strike zone to plot
    axis.add_patch(
        patches.Rectangle(
            (-0.71, 1.5),
            2 * 0.71,
            2,
            edgecolor="lightgray",
            fill=False,
            lw=3,
            zorder=0.1,
        )
    )

    # Check if colorby is continuous or categorical
    is_continuous = pd.api.types.is_numeric_dtype(data[colorby])

    if is_continuous:
        # Use a colormap for continuous variables
        scatter = axis.scatter(
            data["plate_x"],
            data["plate_z"],
            c=data[colorby],
            cmap=cmap,
            s=100,
            alpha=alpha_markers,
        )
        cbar = plt.colorbar(scatter)
        cbar.set_label(legend_title or colorby)
    else:
        # Use categorical colors for non-continuous variables
        sns.scatterplot(
            data=data,
            x="plate_x",
            y="plate_z",
            hue=colorby,
            palette="deep",
            s=100,
            alpha=alpha_markers,
            ax=axis,
        )
        axis.legend(
            title=legend_title or colorby, bbox_to_anchor=(1.05, 1), loc="upper left"
        )

    # Add annotations if specified
    if annotation is not None:
        for _, row in data.iterrows():
            label = str(row[annotation])
            if annotation in ["release_speed", "effective_speed", "launch_speed"]:
                label = f"{float(label):.0f}"
            axis.annotate(
                label,
                (row[plate_loc_x], row[plate_loc_z]),
                size=7,
                ha="center",
                va="center",
                alpha=alpha_text,
            )

    axis.set_xlim(-4, 4)
    axis.set_ylim(-1.5, 7)
    axis.set_xlabel("Horizontal Location (ft)")
    axis.set_ylabel("Vertical Location (ft)")

    plt.title(title)
    plt.tight_layout()
    return axis


def plot_strike_zone_heatmap(
    data: pd.DataFrame,
    title: str = "",
    stat_column: str = "pitch_type",
    agg_function: str = "count",
    cmap: str = "YlOrRd",
    plate_loc_x: str = "plate_x",
    plate_loc_z: str = "plate_z",
    axis: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Produces a strike zone heat map with aggregated statistics in 15 sections,
    including one block outside the traditional strike zone.

    Args:
        data: (pandas.DataFrame)
            StatCast pandas.DataFrame of StatCast pitcher data
        title: (str), default = ''
            Optional: Title of plot
        stat_column: (str), default = 'pitch_type'
            Column to aggregate in each zone
        agg_function: (str), default = 'count'
            Aggregation function to apply ('count', 'mean', 'sum', etc.)
        cmap: (str), default = 'YlOrRd'
            Colormap to use for the heatmap
        plate_loc_x: (str), default = 'plate_x'
            Column name for horizontal pitch location (in feet)
        plate_loc_z: (str), default = 'plate_z'
            Column name for vertical pitch location (in feet)
        axis: (matplotlib.axis.Axes), default = None
            Optional: Axes to plot the strike zone on. If None, a new Axes will be created

    Returns:
        A matplotlib.axes.Axes object with the strike zone heatmap
    """
    # Define extended strike zone boundaries
    x_edges = np.linspace(-2.5, 2.5, 6)
    z_edges = np.linspace(0.5, 4.5, 6)

    # Create bins for x and z coordinates
    data["x_bin"] = pd.cut(
        data[plate_loc_x],
        bins=x_edges,
        labels=["Far Left", "Left", "Middle", "Right", "Far Right"],
    )
    data["z_bin"] = pd.cut(
        data[plate_loc_z],
        bins=z_edges,
        labels=["Very Low", "Low", "Middle", "High", "Very High"],
    )

    # Aggregate data
    heatmap_data = (
        data.groupby(["z_bin", "x_bin"])[stat_column].agg(agg_function).unstack()
    )

    # Reorder the rows to flip the vertical axis
    heatmap_data = heatmap_data.iloc[::-1]

    # Create or get axis
    if axis is None:
        _, axis = plt.subplots()

    # Plot heatmap
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".2f",
        cmap=cmap,
        cbar_kws={"label": f"{agg_function.capitalize()} of {stat_column}"},
        ax=axis,
    )

    # Customize the plot
    axis.set_title(title)
    axis.set_xlabel("Horizontal Location")
    axis.set_ylabel("Vertical Location")

    # Add strike zone outline (now it's the middle 3x3 grid)
    axis.add_patch(plt.Rectangle((1, 1), 3, 3, fill=False, edgecolor="black", lw=2))

    return axis


# Example usage:
# plot_strike_zone_heatmap(data, stat_column='launch_speed', agg_function='mean', title='Average Launch Speed by Zone')
# plt.show()
