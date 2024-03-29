"""This is the main docstring."""

# Imports
from typing import Optional
from pyvis.network import Network as net


# Function to prepare edges for pyvis
def transform_edges(
    edges_df,
    source: str,
    target: str,
    color: Optional[str] = None,
    color_map: Optional[dict] = None,
    hover: Optional[str] = None
):

    """Transform `edges_df` to be compatible with the networkx graph expected by
    a pyvis network.

    Parameters
    ----------
    edges_df : pd.DataFrame
        The dataframe representing the graph's edges and edge attributes.
    source : str:
    target : str
    color : str
    color_map : str
    hover : str
    """

    # Start cols to select
    cols = [source, target]

    # Declare `color` column
    if color is not None and color_map is not None:
        assert isinstance(color, str) and isinstance(color_map, dict), (
            '`color` must be a string and `color_map` must be a dictionary.'
        )
        edges_df['color'] = edges_df[color].map(color_map)
        cols.append('color')
    elif color is not None and color_map is None:
        raise TypeError(
            '`color_map` must be a dictionary when `color` is passed.'
        )
    elif color is None and color_map is not None:
        raise TypeError(
            '`color` must be a string when `color_map` is passed.'
        )

    # Declare `title` column
    if hover is not None:
        assert isinstance(hover, str), '`hover` must be a string.'
        edges_df = edges_df.rename(columns={hover: 'title'})
        cols.append('title')
    
    # Return transformed edges
    edges_df[cols]


# Function to prepare nodes for pyvis
def transforms_nodes():
    True
