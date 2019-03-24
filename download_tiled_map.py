#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
Tiled map downloader.

github.com/oktomus/py-map-fetcher
"""

import os
import requests
import shutil
import sys

from PIL import Image

# Fill in your parameters and edit the url as you wish.
url_template = (
    "...&TileCol={}&TileRow={}")
tiles_folder = "cached"
file_path = "{}/{}/{}.jpeg".format(tiles_folder, "{}", "{}")


def fetch_rows(column_begin, row_begin, width, height):
    """Download all tiles using `url_template` and given coordinates.
    """

    success = True

    print("Downloading tiles from [{}, {}] to [{}, {}]".format(
        column_begin, row_begin, column_begin + width, row_begin + height))

    print("Fetching from {}".format(
        url_template.format(column_begin, row_begin)))

    for row in range(row_begin, row_begin + height):
        for column in range(column_begin, column_begin + width):

            row = str(row)
            column = str(column)

            print("[{}, {}] ...".format(column, row))

            # Create a file path for the current tile.
            path = file_path.format(row, column)

            # Check if it has already been downloaded.
            if os.path.exists(path):
                continue

            # Fetch it from l'internet.
            req = requests.get(url_template.format(column, row), stream=True)

            if req.status_code == 200:
                directory = os.path.dirname(path)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # Write it to a file.
                with open(path, 'wb') as f:
                    req.raw.decode_content = True
                    shutil.copyfileobj(req.raw, f)
            else:
                print("FAILED")
                success = False

            sys.stdout.flush()

    return success


def merge_rows():
    """Check for downloaded tiles and merge them horrizontally.
    """

    print("Merging rows")

    # Find all directories containing tiles.
    # These are named by the row coordinate.
    rows = [
        int(d) for d in os.listdir(tiles_folder)
        if os.path.isdir(os.path.join(tiles_folder, d)) and
        d.isdigit()]

    for row in rows:
        print("Mergin row {}".format(row))

        folder_path = "{}/{}".format(tiles_folder, row)

        if not os.path.exists(folder_path):
            print("No such row")
            return false

        sys.stdout.flush()

        # Find all tiles in the current row directory.
        files = [
            f for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))]

        # Generate file path for each files.
        paths = [os.path.join(folder_path, f) for f in files]

        # Merge all images.
        images = [Image.open(p) for p in paths]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0

        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        new_im.save("{}/merged_row_{}.jpeg".format(tiles_folder, row))

    return True


def stack_rows():
    """Stack rows to create the final image.
    """
    print("Stacking rows")

    files = [
        os.path.join(tiles_folder, f) for f in os.listdir(tiles_folder)
        if os.path.isfile(os.path.join(tiles_folder, f)) and
        f.endswith(".jpeg") and
        f.split("/")[-1].startswith("merged_row_")]

    images = [Image.open(p) for p in files]
    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    total_height = sum(heights)

    new_im = Image.new('RGB', (max_width, total_height))

    y_offset = 0

    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]

    new_im.save("map.jpeg")
    print("Map written to map.jpeg")
    return True


if __name__ == "__main__":

    # Check arguments.
    if len(sys.argv) != 5:
        print("Usage: {} columng_begin row_begin width height".format(
            sys.argv[0]))
        sys.exit(2)

    # Get arguments.
    column_begin = int(sys.argv[1])
    row_begin = int(sys.argv[2])
    width = int(sys.argv[3])
    height = int(sys.argv[4])

    # Fetch tiles for each row.
    if not fetch_rows(column_begin, row_begin, width, height):
        print("Some tiles failed to download. Stopping here.")
        sys.exit(3)

    # Merge all tiles horizontally.
    if not merge_rows():
        print("Unable to merge all rows.")
        sys.exit(4)

    # Create the final image.
    if not stack_rows():
        print("Unable to create the final map image")
        sys.exit(5)
