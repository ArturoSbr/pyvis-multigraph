"""Functions that transform pandas dataframes to a graph compatible with pyvis.

This file contains a set of convenience functions that transform a graph
represented in pandas dataframes (nodes and edges tables) to a networkx graph
whose attributes are compatible with pyvis. The resulting networkx graph can be
visualized using pyvis and all of its edge and node attributes will be
displayed accordingly.

Project owned and maintained by [Arturo Soberon](
    https://github.com/ArturoSbr
).
"""

# TO-DO:
# Add `multigraph` parameter that calls `create_using=nx.MultiGraph`
# when `multigraph=True`. Raise warning: `Network(directed=True)`.


# Imports
from typing import Optional
from networkx import from_pandas_edgelist, set_node_attributes


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
    # Assert if columns required by user exist in edges_df
    cols_usr = [
        col for col in [source, target, color, hover] if col is not None
    ]
    msg = 'Column "{}" not found in `edges_df`.'
    for col in cols_usr:
        assert col in edges_df.columns, msg.format(col)

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
    return edges_df[cols]


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
        The name of the column that represents the labels to be displayed
        inside or below each node.
    color : str
        The name of the column that determines the color of each node.
    color_map : str
        A dictionary that maps each unique value in column `color` to a color
        hex code (e.g., #FF0000) or a color name (e.g., blue).
    hover : str
        The name of the column that contains the text that will be displayed
        when the user hovers over a node.
    """
    # Assert that columns passed by user exist in nodes
    cols_usr = [
        col for col in [id, label, color, hover] if col is not None
    ]
    msg = 'Column "{}" not found in `nodes_df`.'
    for col in cols_usr:
        assert col in nodes_df.columns, msg.format(col)

    # Copy `nodes_df` to avoid overwrite
    temp = nodes_df.copy(deep=True)

    # Init column names to be returned
    cols = [id]

    # Add label column
    if label is not None:
        assert isinstance(label, str), '`label` must be a string.'
        temp['label'] = temp[label].astype(str)
        cols.append('label')

    # Declare `color` column
    if color is not None and color_map is not None:
        assert isinstance(color, str) and isinstance(color_map, dict), (
            '`color` must be a string and `color_map` must be a dictionary.'
        )
        temp['color'] = temp[color].map(color_map)
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
        temp = temp.rename(columns={hover: 'title'})
        cols.append('title')

    # Return transformed nodes_df as dict
    return (
        temp[cols]
        .set_index(id)
        .to_dict(orient='index')
    )


# Function to create an nx graph from an edges and nodes table
def nx_from_pandas(
    edges_df,
    edges_source: str,
    edges_target: str,
    edges_color: Optional[str] = None,
    edges_color_map: Optional[dict] = None,
    edges_hover: Optional[str] = None,
    nodes_df=None,
    nodes_id: Optional[str] = None,
    nodes_label: Optional[str] = None,
    nodes_color: Optional[str] = None,
    nodes_color_map: Optional[str] = None,
    nodes_hover: Optional[str] = None
):
    """Convert pandas dataframes to a networkx graph compatible with pyvis.

    The attributes of the graph returned by this function are named according
    to pyvis' naming conventions. Therefore, the user can pass the resulting
    graph on to a `pyvis.network.Network` object through its `from_nx` method.
    The final visualization will display the graph's node and edge attributes
    set by the user.

    Parameters
    ----------
    edges_df : pd.DataFrame
        The dataframe representing the graph's edges and edge attributes.
    edges_source : str:
        The name of the column that represents the source nodes.
    edges_target : str
        The name of the column that represents the target nodes.
    edges_color : str
        The name of the column that determines the color of each edge.
    edges_color_map : str
        A dictionary that maps each unique value in column `color` to a color
        hex code (e.g., #FF0000) or a color name (e.g., blue).
    edges_hover : str
        The name of the column that contains the text that will be displayed
        when the user hovers over an edge.
    nodes_df : pd.DataFrame
        The dataframe representing the graph's edges and edge attributes.
    nodes_id : str:
        The name of the column that represents the nodes' IDs.
    nodes_label : str
        The name of the column that represents the labels to be displayed
        inside or below each node.
    nodes_color : str
        The name of the column that determines the color of each node.
    nodes_color_map : str
        A dictionary that maps each unique value in column `color` to a color
        hex code (e.g., #FF0000) or a color name (e.g., blue).
    nodes_hover : str
        The name of the column that contains the text that will be displayed
        when the user hovers over a node.

    Returns
    -------
    A networkx graph with edge and node attributes named according to pyvis.
    """
    # Transform edges
    edges_df = transform_edges(
        edges_df=edges_df,
        source=edges_source,
        target=edges_target,
        color=edges_color,
        color_map=edges_color_map,
        hover=edges_hover
    )

    # Transform nodes
    if nodes_df is not None:
        transform_nodes(
            nodes_df=nodes_df,
            id=nodes_id,
            label=nodes_label,
            color=nodes_color,
            color_map=nodes_color_map,
            hover=nodes_hover
        )

    # Get edge attributes
    edge_attr = [
        col for col in edges_df.columns if col not in ['src', 'dst']
    ]
    edge_attr = edge_attr if len(edge_attr) > 0 else None

    # Declare graph from edges
    G = from_pandas_edgelist(
        df=edges_df,
        source=edges_source,
        target=edges_target,
        edge_attr=edge_attr
    )

    # Set node attributes (if any)
    if nodes_df is not None:
        set_node_attributes(
            G=G,
            values=transform_nodes(
                nodes_df=nodes_df,
                id=nodes_id,
                label=nodes_label,
                color=nodes_color,
                color_map=nodes_color_map,
                hover=nodes_hover
            )
        )

    # Return nx Graph
    return G
