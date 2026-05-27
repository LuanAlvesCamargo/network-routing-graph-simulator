import json

NETWORK_FILE = "network.json"


class NetworkManager:

    def load_data(self):
        with open(NETWORK_FILE, "r") as f:
            return json.load(f)

    def save_data(self, data):
        with open(NETWORK_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def add_node(self, node_id, node_type):
        data = self.load_data()
        # Prevent duplicates
        existing_ids = [n["id"] for n in data["nodes"]]
        if node_id in existing_ids:
            return False, "Nó já existe na rede."
        data["nodes"].append({"id": node_id, "type": node_type})
        self.save_data(data)
        return True, "Nó adicionado com sucesso."

    def remove_node(self, node_id):
        data = self.load_data()
        existing_ids = [n["id"] for n in data["nodes"]]
        if node_id not in existing_ids:
            return False, "Nó não encontrado."
        data["nodes"] = [n for n in data["nodes"] if n["id"] != node_id]
        data["edges"] = [
            e for e in data["edges"]
            if e["source"] != node_id and e["target"] != node_id
        ]
        self.save_data(data)
        return True, "Nó removido com sucesso."

    def add_edge(self, source, target, weight):
        data = self.load_data()
        node_ids = [n["id"] for n in data["nodes"]]
        if source not in node_ids or target not in node_ids:
            return False, "Um ou ambos os nós não existem."
        # Check duplicate
        for e in data["edges"]:
            if (e["source"] == source and e["target"] == target) or \
               (e["source"] == target and e["target"] == source):
                return False, "Conexão já existe."
        data["edges"].append({"source": source, "target": target, "weight": weight})
        self.save_data(data)
        return True, "Conexão adicionada."

    def get_stats(self):
        data = self.load_data()
        stats = {"router": 0, "server": 0, "user": 0, "switch": 0, "other": 0}
        for node in data["nodes"]:
            t = node.get("type", "other")
            if t in stats:
                stats[t] += 1
            else:
                stats["other"] += 1
        stats["total_nodes"] = len(data["nodes"])
        stats["total_edges"] = len(data["edges"])
        return stats
