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

    """This function transforms `edges_df` to be compatible with the networkx
    graph expected by a pyvis network.

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

    # Check color and color_map args
    if color is not None and color_map is not None:
        assert isinstance(color, str) and isinstance(color_map, dict), (
            '`color` must be a string representing the name of the column '
            'in `edges_df` that determines the color of each node and '
            '`color_map` must be a dictionary that maps each unique value in '
            'column `color` to a hexadecimal'
        )
    # Declare `color` column
    edges_df['color'] = edges_df[color].map(color_map)


# Function to prepare nodes for pyvis
def transforms_nodes():
    True
