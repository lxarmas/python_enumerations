

import pandas as pd
from matplotlib import pyplot as plt


def main():
   
    photography_services = ["Portraits", "Events", "Weddings", "Real Estate"]
    session_bookings = [23,43, 12, 79]

    # labelled collection of numbers.
    sessions = pd.Series(
        session_bookings,
        index=photography_services,
    )

    # draw the pandas bar chart.
    sessions.plot.bar(
        color="red",
        title="Monthly Photography Sessions",
        xlabel="Photography bookings",
        ylabel="Number of bookings",
        rot=0,
    )

    # Keep the labels inside the image boundaries.
    plt.tight_layout()


    plt.show()


if __name__ == "__main__":
    main()