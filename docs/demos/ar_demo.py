import aframexr

DATA = aframexr.UrlData('https://cdn.jsdelivr.net/gh/davidlab20/TFG@main/docs/static/data/data.json')
BASE = aframexr.Chart(DATA, depth=1)

param = aframexr.selection_point('param', ['motor'])
charts = (
    # Base bar chart
    BASE.mark_bar().encode(x='motor', y='sum(sales)').properties(title='Sales by motor', position='0 2 0').add_params(param)

    +

    # Dynamic pie chart
    BASE.mark_arc().encode(color='model', theta='sales').properties(position='4 2 0').transform_filter(param).movable()
)

# Save scene
charts.save('ar-demo.html', ar_scale='0.075 0.075 0.075')
