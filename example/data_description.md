# Description of Sample Datasets

You can find two csv files within this repo's `./example/` directory. Together,
both files represent the nodes and edges of an undirected multigraph (i.e., the
nodes can be connected to one another through different types of edges).

This small graph is composed of 15 different nodes which share a total of 55
connections.

## Nodes

The file `data_nodes.csv` contains node-level information and has the following
columns:

- `id` - A unique identifier for each node.
- `target` - The category that each node belongs to (can be 0 or 1).
- `description` - A brief description of each node (e.g., _"I am node 11").

## Edges

The file `data_edges.csv` represents the undirected connections between pairs
of nodes. It has the following columns:

- `src` - The node ID of the source.
- `dst` - The node ID of the destination.
- `type` - The connection type shared by a pair of nodes (can be "_E1_" or
"_E2").
- `details` - A short description of each connection.
