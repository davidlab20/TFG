"""Python test to evaluate the results."""


import babiaAltair
import webbrowser


data = """
    {"model": "leon", "motor": "electric", "color": "red",
    "doors": 5, "sales": 10},
    {"model": "ibiza", "motor": "electric", "color": "white",
    "doors": 3, "sales": 15},
    {"model": "cordoba", "motor": "diesel", "color": "black",
    "doors": 5, "sales": 3},
    {"model": "toledo", "motor": "diesel", "color": "white",
    "doors": 5, "sales": 18},
    {"model": "altea", "motor": "diesel", "color": "red",
    "doors": 5, "sales": 4},
    {"model": "arosa", "motor": "electric", "color": "red",
    "doors": 3, "sales": 12},
    {"model": "alhambra", "motor": "diesel", "color": "white",
    "doors": 5, "sales": 5},
    {"model": "600", "motor": "gasoline", "color": "yellow",
    "doors": 3, "sales": 20},
    {"model": "127", "motor": "gasoline", "color": "white",
    "doors": 5, "sales": 2},
    {"model": "panda", "motor": "gasoline", "color": "black",
    "doors": 3, "sales": 13}
"""

chart = babiaAltair.Chart(data).mark_bar().encode(x='model', y='sales')  # Create the chart
chart.save('chart.html')  # Save the chart in an HTML file to see the results in the browser
webbrowser.open('chart.html')  # Open the HTML file in the browser to see the results
