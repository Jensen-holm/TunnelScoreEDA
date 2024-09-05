import seaborn as sns
import matplotlib.pyplot as plt


def plot_strike_zone(
    data, x, y, color=None, title=None, ax=None, palette="viridis", alpha=0.7, s=20
):
    """
    Plot a strike zone using seaborn, capable of handling hundreds of pitches and incorporating tunnel score.

    Parameters:
    - data (DataFrame): The dataset containing pitch location information.
    - x (str): Column name for the horizontal location of pitches.
    - y (str): Column name for the vertical location of pitches.
    - color (str, optional): Column name for the color variable (e.g., 'tunnel_score').
    - title (str, optional): Title for the plot.
    - ax (matplotlib.axes.Axes, optional): The axes to draw the plot onto.
    - palette (str or list, optional): Color palette to use for the plot.
    - alpha (float, optional): Transparency of the scatter points.
    - s (float, optional): Size of the scatter points.

    Returns:
    - matplotlib.axes.Axes: The axes containing the plot.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 12))

    # Plot the pitches
    scatter = sns.scatterplot(
        data=data,
        x=x,
        y=y,
        hue=color,
        palette=palette,
        ax=ax,
        alpha=alpha,
        s=s,
        legend="auto",
    )

    # Set the strike zone (assuming a standard strike zone)
    strike_zone_width = 17 / 12  # 17 inches in feet
    strike_zone_height = 2.33  # Approximate height of strike zone

    # Draw the strike zone
    ax.add_patch(
        plt.Rectangle(
            (-strike_zone_width / 2, 1.5),
            strike_zone_width,
            strike_zone_height,
            fill=False,
            color="black",
            linewidth=2,
        )
    )

    # Set labels and title
    ax.set_xlabel("Horizontal Location (ft)", fontsize=12)
    ax.set_ylabel("Vertical Location (ft)", fontsize=12)
    if title:
        ax.set_title(title, fontsize=14)

    # Set equal aspect ratio and limits
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 5)
    ax.set_aspect("equal")

    # Customize the colorbar if a color variable is provided
    if color:
        colorbar = ax.collections[0].colorbar
        colorbar.set_label(color.capitalize(), fontsize=12)
        colorbar.ax.tick_params(labelsize=10)

    # Add grid lines
    ax.grid(True, linestyle="--", alpha=0.6)

    # Customize tick labels
    ax.tick_params(axis="both", which="major", labelsize=10)

    return ax


# Example usage:
# plot_strike_zone(df, x='pitch_x', y='pitch_y', color='tunnel_score', title='Pitch Locations and Tunnel Scores')
# plt.show()
