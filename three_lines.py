"""Practice zip(), enumerate(), and plotting multiple lines."""

from matplotlib import pyplot as plt


def main():
    """Create the bias-variance chart using the lesson's sample data."""
    variance = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    bias_squared = [256, 128, 64, 32, 16, 8, 4, 2, 1]

    # Add values at matching positions.
    total_error = [
        x + y for x, y in zip(variance, bias_squared)
    ]

    # Create horizontal positions from 0 through 8.
    xs = [i for i, _ in enumerate(variance)]

    # Display the calculated lists in the terminal.
    print("X positions:", xs)
    print("Total error:", total_error)

    # Draw three data series on the same chart.
    plt.plot(xs, variance, "y-", label="variance")
    plt.plot(xs, bias_squared, "r-.", label="bias^2")
    plt.plot(xs, total_error, "b:", label="total error")

    # Show the labels in a legend at the top center.
    plt.legend(loc=9)

    plt.xlabel("model complexity")
    plt.title("The Bias-Variance Tradeoff")

    plt.show()


if __name__ == "__main__":
    main()