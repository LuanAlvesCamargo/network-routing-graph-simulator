from flask import Flask, render_template, request, redirect, url_for, jsonify
import networkx as nx
import os

from network_manager import NetworkManager
from graph_generator import load_graph, draw_graph

app = Flask(__name__)
manager = NetworkManager()


def get_algorithms(G):
    """Run BFS, DFS, Dijkstra on the graph and return results."""
    results = {
        "bfs": [],
        "dfs": [],
        "shortest_path": [],
        "cost": 0,
        "source": "Core",
        "target": "Server",
        "error": None
    }

    nodes = list(G.nodes())
    if not nodes:
        results["error"] = "Grafo vazio."
        return results

    source = "Core" if "Core" in G.nodes() else nodes[0]
    target = "Server" if "Server" in G.nodes() else nodes[-1]
    results["source"] = source
    results["target"] = target

    try:
        results["bfs"] = list(nx.bfs_tree(G, source).nodes())
    except Exception as e:
        results["bfs"] = [str(e)]

    try:
        results["dfs"] = list(nx.dfs_tree(G, source).nodes())
    except Exception as e:
        results["dfs"] = [str(e)]

    try:
        if nx.has_path(G, source, target):
            path = nx.dijkstra_path(G, source, target, weight="weight")
            cost = nx.dijkstra_path_length(G, source, target, weight="weight")
            results["shortest_path"] = path
            results["cost"] = cost
        else:
            results["error"] = f"Sem caminho entre {source} e {target}"
    except Exception as e:
        results["error"] = str(e)

    return results


@app.route("/")
def index():
    G = load_graph()
    algo = get_algorithms(G)
    draw_graph(G, algo.get("shortest_path"))
    stats = manager.get_stats()
    data = manager.load_data()
    return render_template(
        "index.html",
        algo=algo,
        stats=stats,
        nodes=data["nodes"],
        edges=data["edges"],
        graph_ts=int(os.path.getmtime("static/images/graph.png"))
    )


@app.route("/topology")
def topology():
    G = load_graph()
    algo = get_algorithms(G)
    draw_graph(G, algo.get("shortest_path"))
    stats = manager.get_stats()
    data = manager.load_data()
    return render_template(
        "topology.html",
        algo=algo,
        stats=stats,
        nodes=data["nodes"],
        edges=data["edges"],
        graph_ts=int(os.path.getmtime("static/images/graph.png"))
    )


@app.route("/manage")
def manage():
    data = manager.load_data()
    stats = manager.get_stats()
    return render_template("manage.html", data=data, stats=stats)


@app.route("/add-node", methods=["POST"])
def add_node():
    node_id = request.form.get("node_id", "").strip()
    node_type = request.form.get("node_type", "router")
    if node_id:
        manager.add_node(node_id, node_type)
        G = load_graph()
        algo = get_algorithms(G)
        draw_graph(G, algo.get("shortest_path"))
    return redirect(url_for("manage"))


@app.route("/remove-node", methods=["POST"])
def remove_node():
    node_id = request.form.get("node_id", "").strip()
    if node_id:
        manager.remove_node(node_id)
        G = load_graph()
        algo = get_algorithms(G)
        draw_graph(G, algo.get("shortest_path"))
    return redirect(url_for("manage"))


@app.route("/add-edge", methods=["POST"])
def add_edge():
    source = request.form.get("source", "").strip()
    target = request.form.get("target", "").strip()
    weight = request.form.get("weight", "1")
    try:
        weight = int(weight)
    except ValueError:
        weight = 1
    if source and target:
        manager.add_edge(source, target, weight)
        G = load_graph()
        algo = get_algorithms(G)
        draw_graph(G, algo.get("shortest_path"))
    return redirect(url_for("manage"))


@app.route("/api/graph-data")
def api_graph_data():
    """Return graph stats as JSON for live updates."""
    G = load_graph()
    algo = get_algorithms(G)
    stats = manager.get_stats()
    draw_graph(G, algo.get("shortest_path"))
    ts = int(os.path.getmtime("static/images/graph.png"))
    return jsonify({
        "stats": stats,
        "bfs": algo["bfs"],
        "dfs": algo["dfs"],
        "shortest_path": algo["shortest_path"],
        "cost": algo["cost"],
        "source": algo["source"],
        "target": algo["target"],
        "graph_ts": ts
    })


@app.route("/api/nodes")
def api_nodes():
    data = manager.load_data()
    return jsonify(data)


if __name__ == "__main__":
    os.makedirs("static/images", exist_ok=True)
    G = load_graph()
    algo = get_algorithms(G)
    draw_graph(G, algo.get("shortest_path"))
    app.run(debug=True, port=5000)
