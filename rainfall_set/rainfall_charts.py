"""Read two rainfall datasets, compare them, and save five charts.

HELPER FUNCTIONS
1.Rainfall comparison (draw_comparison)

2.Earlier-period rainfall with minimum and maximum (draw_single_set)

3.Later-period rainfall with minimum and maximum(draw_single_set)

4.Minimum and maximum from both datasets(draw_extremes)

5.Rainfall change by location(draw_changes)


"""

from pathlib import Path

from matplotlib import pyplot as plt


def read_rainfall(file_path):
    """Return a dictionary of rainfall values from the given file."""
    rainfall = {}

    with file_path.open("r", encoding="utf-8-sig") as rainfall_file:
        for line_number, line in enumerate(rainfall_file, start=1):
            line = line.strip()

            # Ignore empty lines.
            if not line:
                continue

            # Separate the location name from the rainfall value.
            parts = line.rsplit(maxsplit=1)

            if len(parts) != 2:
                raise ValueError(
                    f"{file_path.name}, line {line_number}: "
                    "expected a location name and a rainfall value."
                )

            # Unpack the two parts into variables.
            location, rainfall_text = parts

            # Assume these two spellings refer to the same location.
            if location == "Adina":
                location = "Adine"

            try:
                amount = float(rainfall_text)
            except ValueError as error:
                raise ValueError(
                    f"{file_path.name}, line {line_number}: "
                    f"invalid rainfall value '{rainfall_text}'."
                ) from error

            if amount < 0:
                raise ValueError(
                    f"{file_path.name}, line {line_number}: "
                    "rainfall cannot be negative."
                )

            if location in rainfall:
                raise ValueError(
                    f"{file_path.name}, line {line_number}: "
                    f"duplicate location '{location}'."
                )

            rainfall[location] = amount

    if not rainfall:
        raise ValueError(f"{file_path.name} contains no rainfall data.")

    return rainfall


def validate_locations(setbefore, setafter):
    """Check that both datasets contain the same locations."""
    only_setbefore = set(setbefore) - set(setafter)
    only_setafter = set(setafter) - set(setbefore)

    if only_setbefore or only_setafter:
        raise ValueError(
            "The datasets contain different locations.\n"
            f"Only in Set_before_ten_years: {sorted(only_setbefore)}\n"
            f"Only in Set_after_ten_years: {sorted(only_setafter)}"
        )


def find_extremes(rainfall):
    """Return the locations with the minimum and maximum rainfall."""
    min_location = min(rainfall, key=rainfall.get)
    max_location = max(rainfall, key=rainfall.get)

    return min_location, max_location


def set_location_ticks(ax, positions, locations):
    """Place readable location labels along the horizontal axis."""
    ax.set_xticks(positions)
    ax.set_xticklabels(locations, rotation=60, ha="right")
    ax.set_xlabel("Location")


def draw_comparison(ax, locations, setbefore, setafter):
    """Draw side-by-side bars comparing the two periods."""
    positions = list(range(len(locations)))
    setbefore_values = [setbefore[location] for location in locations]
    setafter_values = [setafter[location] for location in locations]

    width = 0.4
    setbefore_positions = [
        position - width / 2 for position in positions
    ]
    setafter_positions = [
        position + width / 2 for position in positions
    ]

    ax.bar(
        setbefore_positions,
        setbefore_values,
        width=width,
        color="skyblue",
        label="Set_before_ten_years: earlier period",
    )

    ax.bar(
        setafter_positions,
        setafter_values,
        width=width,
        color="limegreen",
        label="Set_after_ten_years: later period",
    )

    set_location_ticks(ax, positions, locations)

    ax.set_title("Rainfall Comparison: Earlier and Later Periods")
    ax.set_ylabel("Rainfall (inches)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)


def draw_single_set(ax, locations, rainfall, set_name, color, upper_limit):
    """Draw one dataset and highlight its minimum and maximum."""
    positions = list(range(len(locations)))
    values = [rainfall[location] for location in locations]

    ax.bar(positions, values, color=color, alpha=0.7)

    min_location, max_location = find_extremes(rainfall)
    min_position = locations.index(min_location)
    max_position = locations.index(max_location)

    # Place markers at the tops of the minimum and maximum bars.
    ax.scatter(
        min_position,
        rainfall[min_location],
        color="hotpink",
        marker="v",
        s=110,
        zorder=3,
        label=f"Minimum: {min_location} ({rainfall[min_location]:.2f})",
    )

    ax.scatter(
        max_position,
        rainfall[max_location],
        color="lavender",
        marker="^",
        s=110,
        zorder=3,
        label=f"Maximum: {max_location} ({rainfall[max_location]:.2f})",
    )

    # Add text near each highlighted point.
    for location, position, description, text_color in [
        (min_location, min_position, "min", "hotpink"),
        (max_location, max_position, "max", "lavender"),
    ]:
        ax.annotate(
            f"{description}: {rainfall[location]:.2f}",
            xy=(position, rainfall[location]),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            color=text_color,
        )

    set_location_ticks(ax, positions, locations)

    ax.set_title(f"{set_name}: Rainfall with Minimum and Maximum")
    ax.set_ylabel("Rainfall (inches)")

    # Use the same vertical scale for both individual-set charts.
    ax.set_ylim(0, upper_limit)

    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)


def draw_extremes(ax, setbefore, setafter):
    """Draw only the minimum and maximum values of both datasets."""
    min_location1, max_location1 = find_extremes(setbefore)
    min_location2, max_location2 = find_extremes(setafter)

    labels = [
        f"min-{min_location1}-Set_before_ten_years",
        f"max-{max_location1}-Set_before_ten_years",
        f"min-{min_location2}-Set_after_ten_years",
        f"max-{max_location2}-Set_after_ten_years",
    ]

    values = [
        setbefore[min_location1],
        setbefore[max_location1],
        setafter[min_location2],
        setafter[max_location2],
    ]

    colors = ["hotpink", "lavender", "hotpink", "lavender"]
    positions = list(range(len(labels)))

    ax.scatter(
        positions,
        values,
        color=colors,
        s=130,
        zorder=3,
    )

    # Label the four values without connecting unrelated locations.
    for position, value in zip(positions, values):
        ax.annotate(
            f"{value:.2f}",
            xy=(position, value),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
        )

    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=20, ha="right")

    ax.set_title("Minimum and Maximum Rainfall in Each Dataset")
    ax.set_xlabel("Extreme, location, and dataset")
    ax.set_ylabel("Rainfall (inches)")
    ax.set_ylim(0, max(values) * 1.2)
    ax.margins(x=0.15)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)


def draw_changes(ax, locations, setbefore, setafter):
    """Draw the rainfall change: later period minus earlier period."""
    # Sort from the largest decrease to the largest increase.
    ordered_locations = sorted(
        locations,
        key=lambda location: setafter[location] - setbefore[location],
    )

    changes = [
        setafter[location] - setbefore[location]
        for location in ordered_locations
    ]

    colors = [
        "hotpink" if change < 0 else "limegreen"
        for change in changes
    ]

    ax.barh(ordered_locations, changes, color=colors)
    ax.invert_yaxis()

    # Zero separates decreases from increases.
    ax.axvline(0, color="blue", linewidth=1)

    ax.set_title(
        "Rainfall Change by Location: "
        "Set_after_ten_years Minus Set_before_ten_years"
    )
    ax.set_xlabel("Change in rainfall (inches): negative = decrease")
    ax.set_ylabel("Location")
    ax.grid(axis="x", alpha=0.3)
    ax.set_axisbelow(True)


def save_chart(fig, output_folder, filename):
    """Adjust layout and save fig as a PNG image."""
    fig.tight_layout()

    output_path = output_folder / filename
    fig.savefig(output_path, dpi=150, bbox_inches="tight")

    print(f"Saved chart: {output_path.name}")


def main():
    """Read the files, create five plot objects, and save the charts."""
    # Find input files beside this Python script.
    project_folder = Path(__file__).resolve().parent

    setbefore_path = project_folder / "rainfall_earlylist.txt"
    setafter_path = project_folder / "rainfall_latelist.txt"

    setbefore = read_rainfall(setbefore_path)
    setafter = read_rainfall(setafter_path)

    validate_locations(setbefore, setafter)

    # Preserve the order from the earlier dataset.
    locations = list(setbefore)

    output_folder = project_folder / "rainfall_charts"
    output_folder.mkdir(exist_ok=True)

    upper_limit = max(
        max(setbefore.values()),
        max(setafter.values()),
    ) * 1.3

    # Chart 1: compare both datasets.
    comparison_fig, comparison_ax = plt.subplots(figsize=(16, 8))
    draw_comparison(
        comparison_ax,
        locations,
        setbefore,
        setafter,
    )
    save_chart(
        comparison_fig,
        output_folder,
        "01_rainfall_comparison.png",
    )

    # Chart 2: earlier period with its minimum and maximum.
    setbefore_fig, setbefore_ax = plt.subplots(figsize=(16, 8))
    draw_single_set(
        setbefore_ax,
        locations,
        setbefore,
        "Set_before_ten_years: Earlier Period",
        "skyblue",
        upper_limit,
    )
    save_chart(
        setbefore_fig,
        output_folder,
        "02_setbefore_extremes.png",
    )

    # Chart 3: later period with its minimum and maximum.
    setafter_fig, setafter_ax = plt.subplots(figsize=(16, 8))
    draw_single_set(
        setafter_ax,
        locations,
        setafter,
        "Set_after_ten_years: Later Period",
        "limegreen",
        upper_limit,
    )
    save_chart(
        setafter_fig,
        output_folder,
        "03_setafter_extremes.png",
    )

    # Chart 4: only the four extreme values.
    extremes_fig, extremes_ax = plt.subplots(figsize=(12, 7))
    draw_extremes(extremes_ax, setbefore, setafter)
    save_chart(
        extremes_fig,
        output_folder,
        "04_both_sets_extremes.png",
    )

    # Chart 5: change at each location.
    changes_fig, changes_ax = plt.subplots(figsize=(12, 11))
    draw_changes(changes_ax, locations, setbefore, setafter)
    save_chart(
        changes_fig,
        output_folder,
        "05_rainfall_changes.png",
    )

    # Display the figures after saving them.
    plt.show()


if __name__ == "__main__":
    main()


# Conclusion:
# Based on the reported results, rainfall increased at all 26
# matched locations.
#
# The earlier dataset has its minimum at Cascade (5.48 inches)
# and its maximum at Bloomfield (38.02 inches).
#
# The later dataset has its minimum at Adine (30.32 inches)
# and its maximum at Bloomfield (96.57 inches).
#
# This comparison assumes that "Adina" and "Adine" refer to the
# same location and that both datasets use inches and represent
# comparable rainfall measurements.
#
# These datasets do not show individual yearly changes or
# establish the cause of the differences.