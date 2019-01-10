""" Graphing helpers and shortcuts for Python Pandas dataframes
Using the Plotly graphing library.  Help at https://plot.ly/python/
"""

import pendulum #Datetime library
from plotly.offline import iplot
import plotly.graph_objs as go


def chart_time(strtime, local_tz):
    """ A plotly bug forces all timestamps to UTC.
    This function converts the supplied time-string to local time,
    then recasts it as UTC so that the hours align on the graph.
    Isoformatting makes the Pendulum object compatible with Pandas.
    local_tz can be 'America/New_York', 'America/Los_Angeles', etc."""
    return pendulum.parse(strtime).in_tz(local_tz).set(tz='UTC').isoformat()

def itergroups(df, groupcol):
    """Return slices of a dataframe based on the
    supplied grouping column (str)
    """
    for item in df[groupcol].unique():
        yield df[df[groupcol] == item], item


def histo_series(series, title=None):
    """Histogram a single Pandas Series"""
    if title is None:
        title = series
    
    histo = go.Histogram(
        x=series,
        opacity=0.75,
    )

    data = [histo]

    layout = go.Layout(dict(
        width=900,
        height=300,
        title=title,
        xaxis=dict(
            title='',
        ),
        yaxis=dict(
            title='Frequency',
        ),
        hovermode='closest'
    ))

    fig = go.Figure(data=data, layout=layout)

    iplot(fig)

def histo_all(df):
    """Histogram all columns of a pandas DataFrame"""
    for column in df.columns:
        try: 
            histo_series(df[column], column)
        except Exception as ex:
            print("Error plotting {}: {}".format(column, ex))
            next
            
def scatter_xy(df, x, y, mode='markers', title=''):
    """Provide a dataframe(df), and strings representing
    the column names for the x and y variables.
    Uses Plotly's WebGL interface for speedier scatters.
    """
    data = []

    data.append(
        go.Scattergl(
            name='',
            x=df[x],
            y=df[y],
            # text=None,
            mode=mode,
            marker=dict(
                opacity=0.5,
                # color=color,
                # colorscale='Portland',
            )
        )
    )

    layout = go.Layout(dict(
        title=title,
        xaxis=dict(
            title=x,
            ),
        yaxis=dict(
            title=y),
        hovermode='closest'
    ))

    iplot(go.Figure(data=data, layout=layout))

def sort_by_x(df, x):
    """Sort a dataframe by a column """
    return df.sort_values(by=x)

def line_xy(df, x, y):
    """Provide a dataframe(df), and strings representing
    the column names for the x and y variables.  Identify
    a column for the text or color variables if you wish.
    Uses Plotly's WebGL interface for speedier scatters.
    """
    scatter_xy(sort_by_x(df, x), x, y, mode='lines')

def line_by_group(df, x, y, group):
    """Line chart looping over groups
    in the provided DataFrame
    """

    #Order the values so lines don't look crazy
    data = []

    #Iterate over group names and append a scatter
    for tdf, item in itergroups(sort_by_x(df, x), group):
        data.append(
            go.Scatter(
                name=item,
                x=tdf[x],
                y=tdf[y],
                mode='lines',
            ))

    layout = go.Layout(dict(
        title='',
        xaxis=dict(
            title=x,
            ),
        yaxis=dict(
            title=y),
        hovermode='closest'
    ))

    iplot(go.Figure(data=data, layout=layout))

def box_by_group(df, group, y, title=''):
    """Box plot for categorical groups
    """
    data = []

    #Iterate over group names and append a scatter
    for tdf, item in itergroups(df, group):
        data.append(go.Box(
            name=item,
            y=tdf[y],
            jitter=0.3,
            showlegend=False,
            marker=dict(
                opacity=0.5,
                color='blue'
            )
        ))

    layout = go.Layout(dict(
        title=title,
        xaxis=dict(
            title=group,
            ),
        yaxis=dict(
            title=y,
        ),
        hovermode='closest'
    ))

    iplot(go.Figure(data=data, layout=layout))
