import glob
import os
import shutil


# Set location of HTML files
html = "final/shipments/*.html"
destination = "final/shipments/archive/"
csv = ("CSV/*/*.CSV")
# Iterate through HTML files
for f in glob.glob(html):
    print("Moving " + f)
    shutil.copy(f, destination)
    if f:
        os.remove(f)

for f in glob.glob(csv):
    print(f)

    # remove old csv files
    os.remove(f)
