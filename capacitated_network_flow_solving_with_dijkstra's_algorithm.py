import networkx as nx
import itertools
import matplotlib.pyplot as plt

# ===== 1. Define a larger network =====
G = nx.DiGraph()
edges = [
    (0, 1, 15, 2),
    (0, 2, 7, 4),
    (1, 3, 10, 1),
    (2, 3, 10, 2),
    (2, 4, 8, 3),
    (3, 5, 9, 2),
    (4, 5, 13, 1)
]

# Add edges to the graph with 'capacity' and 'cost' attributes
for u, v, cap, cost in edges:
    G.add_edge(u, v, capacity=cap, cost=cost)

# Define source, sink and total flow to send
source = 0
sink = 5
total_flow = 15

# Initialize node info dictionary
# For each node, we store:
# - shortest_distance: tentative shortest distance from source
# - previous_node: to reconstruct the shortest path
node_info = {
    node: {"shortest_distance": float('inf'), "previous_node": None}
    for node in G.nodes()
}

# Initialize edge info dictionary
# For each edge, we store the current flow
edge_info = {
    edge: {"flow": 0}
    for edge in G.edges()
}

# Distance from source to itself is zero
node_info[0]["shortest_distance"] = 0

# Initialize visited and unvisited node sets
visited_nodes = set()
unvisited_nodes = set(G.nodes())
total_cost = 0  # Total cost of all flows sent

# ===== Main loop: send flow until total_flow is satisfied =====
while total_flow > 0:
    # Reset node info for each Dijkstra iteration
    for node in G.nodes():
        node_info[node]["shortest_distance"] = float('inf')
        node_info[node]["previous_node"] = None
    node_info[source]["shortest_distance"] = 0

    visited_nodes = set()
    unvisited_nodes = set(G.nodes())

    # ===== Dijkstra algorithm on residual network =====
    while unvisited_nodes:
        # Pick the unvisited node with the smallest tentative distance
        min_node = min(unvisited_nodes, key=lambda x: node_info[x]["shortest_distance"])
        if node_info[min_node]["shortest_distance"] == float('inf'):
            break  # Remaining nodes are unreachable
        unvisited_nodes.remove(min_node)
        visited_nodes.add(min_node)

        # Relax all neighbors that have remaining capacity
        for neighbor in G.neighbors(min_node):
            # Check residual capacity
            if edge_info[(min_node, neighbor)]["flow"] < G[min_node][neighbor]["capacity"]:
                # Tentative distance to neighbor through min_node
                new_distance = node_info[min_node]["shortest_distance"] + G[min_node][neighbor]["cost"]
                # If this distance is smaller, update neighbor info
                if new_distance < node_info[neighbor]["shortest_distance"]:
                    node_info[neighbor]["shortest_distance"] = new_distance
                    node_info[neighbor]["previous_node"] = min_node

    # ===== Check if sink is reachable =====
    if node_info[sink]["previous_node"] is None:
          print("No more augmenting paths!")
          break   

    # ===== Reconstruct path from source to sink =====
    path = []
    node = sink
    while node != source:
        prev = node_info[node]["previous_node"]
        path.append((prev, node))
        node = prev
    path.reverse()  # Reverse to get path from source to sink

    # ===== Determine how much flow can be sent through this path =====
    send_flow = min(G[u][v]["capacity"] - edge_info[(u, v)]["flow"] for u, v in path)
    send_flow = min(send_flow, total_flow)  # Cannot send more than remaining total_flow

    # ===== Update flows along the path =====
    for u, v in path:
        edge_info[(u, v)]["flow"] += send_flow

    # ===== Calculate path cost =====
    # Total cost = sum of edge costs along path * flow sent
    path_cost = sum(G[u][v]["cost"] for u, v in path) * send_flow
    total_cost += path_cost  # Accumulate total cost

    # Reduce remaining flow to send
    total_flow -= send_flow

    # Print info about this flow augmentation
    print(f"Sent flow = {send_flow} via {path}, path cost = {path_cost}, remaining flow = {total_flow}, Total cost = {total_cost}")


# ===== Visualization =====
plt.figure(figsize=(12,8))  # Bigger figure

pos = nx.spring_layout(G, seed=42)  # positions for nodes

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=1200, node_color='lightblue')
# Draw edges with curved arrows
nx.draw_networkx_edges(
    G, pos, arrowstyle='-|>', arrowsize=25,
    connectionstyle='arc3,rad=0.2', width=2
)
# Draw node labels
nx.draw_networkx_labels(G, pos, font_size=14, font_color='black')

# Edge labels: flow / capacity, cost
edge_labels = {}
for u,v in G.edges():
    f = edge_info[(u,v)]["flow"]
    c = G[u][v]["capacity"]
    cost = G[u][v]["cost"]
    edge_labels[(u,v)] = f"{f}/{c}, cost={cost}"

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, label_pos=0.6)

plt.title("Capacitated Network Flow", fontsize=16)
plt.axis('off')
plt.show()