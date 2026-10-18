import matplotlib.pyplot as plt


def main():
    movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
    num_oscars = [5, 11, 3, 8, 10]
    # bars are by default width 0.8, so we'll add 0.1 to the left coordinates
    xs = [i + 0.1 for i, _ in enumerate(movies)]
    # plot bars with left x-coordinates [xs], heights [num_oscars]
    plt.bar(xs, num_oscars)
    plt.ylabel("# of Academy Awards")
    plt.title("My Favorite Movies")
    plt.xticks([i + 0.5 for i, _ in enumerate(movies)], movies)
    # label x-axis movie names
    plt.show()


if __name__ == "__main__":
    main()