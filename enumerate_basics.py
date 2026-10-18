"""Create a line chart using the GDP data from the lesson."""

from matplotlib import pyplot as plt


def main():
    """Plot the lesson's GDP values against their corresponding years."""
    # Horizontal positions of the points.
    years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]

    # Vertical positions, measured in billions of dollars.
    gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 2500.5]

    # Draw green points connected by a solid green line.
    plt.plot(years, gdp, color="red", marker="o", linestyle="solid")

    # Describe the chart and its axes.
    plt.title("Nominal GDP")
    plt.xlabel("Year")
    plt.ylabel("Billions of dollars")

    # Display the completed chart.
    plt.show()


if __name__ == "__main__":
    main()