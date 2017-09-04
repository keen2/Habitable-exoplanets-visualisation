# Habitable-exoplanets-visualisation
Visualization of the open data from NASA Exoplanets Archive of planets outside the solar system that are similar to the Earth and habitable.

Using the open data from NASA Exoplanets Archive (https://exoplanetarchive.ipac.caltech.edu/index.html). By means of NASA API the planets outside the solar system that are similar to the Earth and habitable were parsed and stored to SQLite database:
"content.sqlite"

There are two visualizations of the parsed data:
1. "khistogram.py"  - via Python 3 it samples data into "khistogram.js";
2. "khistogram.htm" - uses D3.js library to visualize and "khistogram.js" with data needed;

3. "kbchart.py"  - via Python 3 it samples data into "kbchart.js" in special order;
4. "kbchart.htm" - uses Google BubbleChart to visualize and "kbchart.js" with data needed;

The Temperature in K. For clarity, the Earth was placed nearby the origin, but so that it could be seen. Axises are logarithmic.
