from altair import Chart, Tooltip  # Chart and Tooltip are imported from the Altair library.
from pandas import DataFrame  # The DataFrame class from the pandas library is imported.
import altair as alt


# The chart function is defined, taking four parameters. df, x, y, and target.
# df is the input DataFrame that has the data for the chart.
# x and y represent the x-axis and y-axis variables.
# target will be used for the color of the data points on the chart.
def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    properties = {
        'background': "#252525",
        'width': 700,
        'height': 500,
        'padding': 10,
    }

    slider = alt.binding_range(min=0, max=1, step=0.05, name='opacity:')
    op_var = alt.param(value=0.1, bind=slider)

    graph = Chart(df, title=f"{y} by {x} for {target}").mark_point(size=100, opacity=op_var).encode(
        x=x,
        y=y,
        color=target,
        tooltip=Tooltip(df.columns.to_list())
    ).properties(**properties).configure_axis(labelColor='white', titleColor='white').configure_title(
        color='white'
    ).configure_legend(
        strokeColor='gray',
        padding=10,
        cornerRadius=10,
        orient='right',
        labelColor='white',
        titleColor='white'
    ).add_params(
        op_var
    )

    return graph


if __name__ == '__main__':
    from app.data import Database

    db = Database("monster")
    db.reset()
    db.seed(3000)
    print(db.count())
