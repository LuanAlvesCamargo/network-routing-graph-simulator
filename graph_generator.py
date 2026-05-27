import json
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def load_graph():
    with open("network.json", "r") as f:
        data = json.load(f)

    G = nx.Graph()
    for node in data["nodes"]:
        G.add_node(node["id"], type=node["type"])
    for edge in data["edges"]:
        G.add_edge(edge["source"], edge["target"], weight=edge["weight"])
    return G


NODE_STYLES = {
    "router":  {"color": "#38bdf8", "shape": "o", "size": 2800},
    "server":  {"color": "#22c55e", "shape": "s", "size": 3000},
    "user":    {"color": "#f59e0b", "shape": "o", "size": 2200},
    "switch":  {"color": "#a855f7", "shape": "D", "size": 2400},
    "default": {"color": "#94a3b8", "shape": "o", "size": 2000},
}


def draw_graph(G, shortest_path=None):
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    pos = nx.spring_layout(G, seed=42, k=2.5)

    # Draw edges (normal)
    path_edges = []
    if shortest_path and len(shortest_path) > 1:
        path_edges = list(zip(shortest_path, shortest_path[1:]))

    normal_edges = [e for e in G.edges() if e not in path_edges and (e[1], e[0]) not in path_edges]

    nx.draw_networkx_edges(
        G, pos,
        edgelist=normal_edges,
        edge_color="#334155",
        width=2,
        ax=ax,
        style="solid",
        alpha=0.8
    )

    # Draw path edges in red/orange
    if path_edges:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            edge_color="#ef4444",
            width=4,
            ax=ax,
            style="solid",
            alpha=1.0
        )

    # Draw nodes by type
    type_groups = {}
    for node, data in G.nodes(data=True):
        t = data.get("type", "default")
        if t not in type_groups:
            type_groups[t] = []
        type_groups[t].append(node)

    for ntype, nodes in type_groups.items():
        style = NODE_STYLES.get(ntype, NODE_STYLES["default"])
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=nodes,
            node_color=style["color"],
            node_size=style["size"],
            node_shape=style["shape"],
            ax=ax,
            alpha=0.95
        )

    # Labels
    nx.draw_networkx_labels(
        G, pos,
        font_color="#0f172a",
        font_size=9,
        font_weight="bold",
        ax=ax
    )

    # Edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_color="#94a3b8",
        font_size=8,
        ax=ax,
        bbox=dict(boxstyle="round,pad=0.2", facecolor="#1e293b", edgecolor="none", alpha=0.8)
    )

    # Legend
    legend_items = [
        mpatches.Patch(color="#38bdf8", label="Router"),
        mpatches.Patch(color="#22c55e", label="Server"),
        mpatches.Patch(color="#f59e0b", label="User"),
        mpatches.Patch(color="#a855f7", label="Switch"),
    ]
    if shortest_path:
        legend_items.append(mpatches.Patch(color="#ef4444", label="Menor Caminho"))

    legend = ax.legend(
        handles=legend_items,
        loc="upper left",
        facecolor="#1e293b",
        edgecolor="#334155",
        labelcolor="#cbd5e1",
        fontsize=9,
        framealpha=0.9
    )

    ax.set_title("Network Topology", color="#38bdf8", fontsize=14, fontweight="bold", pad=15)
    ax.axis("off")
    plt.tight_layout(pad=1.5)
    plt.savefig("static/images/graph.png", dpi=120, bbox_inches="tight", facecolor="#0f172a")
    plt.close()
