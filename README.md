:sunrise_over_mountains: :mag: Download the map you want.

## How to use it

1. Edit `download_tiled_map.py` to fill in required parameters.
2. Download

        ```
        # Download 5x5 tiles starting from tile at (34133, 22633)
        $ python download_tiled_map.py 34133 22633 5 5
        ```
3. The final map is available `map.jpeg`        
4. Delete the pretty big folder `cached` which containes all tiles once done.

## How to use the map with a map reader

The jpeg format is really small and easy to use, but you can't locate yourself on it with GPS. Although, you can convert the map to another format so that you can open it in a map reader. In my case, I used `Mobile Atlas Map Creator` to convert the map to `sqllite` and read it using the app `Locus`.

## How to know the coordinates of my map ?

For example on the website géoportail, open your web browser developper tools and take a look at the web requests.

![](screenshot.jpg)

## Contributing

Lot of improvements can be made. You can contribute to this project by writting code or user documentation. 

Here is a non exhausitve list of possible improvements:
- Writting a complete guide on how to get a map on a phone
- Don't write the parameters in the python script. Use a `yaml` file instead.
- Directly export the `sqllite` file.
- Adapt the script to other map providers and document it.
- Instead of giving coordinates, give a location and fetch a given radius

For any feature request, please [file an issue](https://github.com/oktomus/py-map-fetcher/issues/new).
