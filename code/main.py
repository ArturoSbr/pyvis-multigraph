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
    """Transform `edges_df` to be compatible with a pyvis network.

    Parameters
    ----------
    edges_df : pd.DataFrame
        The dataframe representing the graph's edges and edge attributes.
    source : str:
        The name of the column that represents the source nodes.
    target : str
        The name of the column that represents the target nodes.
    color : str
        The name of the column that determines the color of each edge.
    color_map : str
        A dictionary that maps each unique value in column `color` to a color
        hex code (e.g., #FF0000) or a color name (e.g., blue).
    hover : str
        The name of the column that contains the text that will be displayed
        when the user hovers over an edge.
    """
    # Init column names to be returned
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
def transform_nodes(
    nodes_df,
    id: str,
    label: Optional[str] = None,
    color: Optional[str] = None,
    color_map: Optional[str] = None,
    hover: Optional[str] = None
):
    """Transform `nodes_df` to be compatible with pyvis.
    
    Parameters
    ----------
    nodes_df : pd.DataFrame
        The dataframe representing the graph's edges and edge attributes.
    id : str:
        The name of the column that represents the nodes' IDs.
    label : str
        The name of the column that represents the labels to be displayed inside
        or below each node.
    color : str
        The name of the column that determines the color of each node.
    color_map : str
        A dictionary that maps each unique value in column `color` to a color
        hex code (e.g., #FF0000) or a color name (e.g., blue).
    hover : str
        The name of the column that contains the text that will be displayed
        when the user hovers over a node.
    """
    # Init column names to be returned
    cols = [id]

    # Add label column
    if label is not None:
        assert isinstance(label, str), '`label` must be a string.'
        nodes_df['label'] = nodes_df[label].astype(str)
        cols.append('label')

    # Declare `color` column
    if color is not None and color_map is not None:
        assert isinstance(color, str) and isinstance(color_map, dict), (
            '`color` must be a string and `color_map` must be a dictionary.'
        )
        nodes_df['color'] = nodes_df[color].map(color_map)
        cols.append('color')
    elif color is not None and color_map is None:
        raise TypeError(
            '`color_map` must be a dictionary when `color` is passed.'
        )
    elif color is None and color_map is not None:
        raise TypeError(
            '`color` must be a string when `color_map` is passed.'
        )

    # Add hover column
    if hover is not None:
        assert isinstance(hover, str), '`hover` must be a string.'
        nodes_df = nodes_df.rename(columns={hover: 'title'})
        cols.append('title')

    # Return transformed nodes
    return nodes_df[cols]
