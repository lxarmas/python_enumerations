from pathlib import Path

rainfall_file = Path("rainfall_set") / "rainfall_earlylist.txt"

contents = rainfall_file.read_text(encoding="utf-8")
lines = contents.splitlines()

for line in lines:
    if line:  # Skip the empty first line
        location, rainfall = line.rsplit(maxsplit=1)

        print("Location:", location)
        print("Rainfall:", rainfall)