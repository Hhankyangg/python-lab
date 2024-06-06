import json
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from tqdm import tqdm

from fun_leetcode.Problem import Problem


class TagGraph:
    
    def __init__(self, problems):
        """Build a graph based on the problems info, which vertices are problem ids and 
        edges are 1 / (common tags num) between problems. Weight lower means more common tags.

        Args:
            problems (List[Problem]): A list of Problem objects, the first element should be None.

        Returns:
            nx.Graph: The graph built based on the problems info.
        """
        self.problems = problems
        self.n = len(self.problems) - 1 # problem id starts from 1
        self.G = self._build_graph()
        
        
    def _build_graph(self):
        
        G = nx.Graph()  
        
        for problem in self.problems:
            if problem: # in case of problems[0] == None
                G.add_node(problem.id, 
                        title=problem.title, 
                        ac_rate=problem.ac_rate, 
                        difficulty=problem.difficulty, 
                        tags=problem.tags)
        
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                temp = len(set(self.problems[i].tags) & set(self.problems[j].tags))
                if temp == 0:
                    continue
                weight = 1 / temp
                G.add_edge(self.problems[i].id, self.problems[j].id, weight=weight)
        
        return G
    

    def visualize_graph(self):
        """Beta version of the function to visualize the graph
        """
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(self.G)
        
        for node in tqdm(net.nodes):
            node["title"] = f"ID: {node['id']}, Tags: {self.G.nodes[node['id']]['tags']}"
            node["value"] = 10 

        for edge in tqdm(net.edges):
            edge["value"] = edge["weight"] * 0.1

        net.toggle_physics(True)
        
        net.show("mygraph.html")
    
    
    def find_adjacent_problems(self, problem_id: int, tag_threshold: int = 1):
        """Find adjacent problem id of a specific problem id in the graph 
        with weight <= 1 / tag_threshold

        Args:
            problem_id (int): The problem id to find its adjacent nodes
            tag_threshold (int, optional): Weight threshold to filter the adjacent nodes. Defaults to 1.

        Returns:
            adjacent_nodes (List): the order of adjacent problem id, sorted by difficulty and then ac_rate (ac in reverse order)
        """
        if problem_id not in self.G:
            print(f"Node {problem_id} does not exist in the graph.")
            return []
        
        adjacent_nodes = []
        for neighbor, edge_attrs in self.G[problem_id].items():
            if edge_attrs['weight'] <= 1 / tag_threshold:
                adjacent_nodes.append(neighbor)
        
        if adjacent_nodes == []:
            print(f"Node {problem_id} has no adjacent nodes which weight <= {tag_threshold}.")
        
        # sort the adjacent nodes first by difficulty, then by ac_rate (acc in reverse order)
        adjacent_nodes = self._sort_nodes_by_difficulty_and_ac_rate(adjacent_nodes)
        
        return adjacent_nodes

    def _sort_nodes_by_difficulty_and_ac_rate(self, node_ids):
        
        nodes_data = [(node_id, self.G.nodes[node_id]) for node_id in node_ids if node_id in self.G]

        difficulty_order = {'Easy': 1, 'Medium': 2, 'Hard': 3}
        
        sorted_nodes = sorted(nodes_data, key=lambda x: (
            difficulty_order.get(x[1]['difficulty'], 0),
            -x[1]['ac_rate']
        ))

        return [node[0] for node in sorted_nodes]


    def get_similarity_between(self, problem_id1: int, problem_id2: int):
        """Get the similarity between two problems based on the weight of the edge between them

        Args:
            problem_id1 (int): The problem id of the first problem
            problem_id2 (int): The problem id of the second problem

        Returns:
            similarity (float): The similarity between the two problems
        """
        if problem_id1 not in self.G or problem_id2 not in self.G:
            raise ValueError(f'Invalid id! Node {problem_id1} or {problem_id2} does not exist')
            return 0
        
        try:
            length = nx.shortest_path_length(self.G, source=problem_id1, target=problem_id2, weight='weight')
            print(f"Shortest path length from {problem_id1} to {problem_id2} is:", length)
        except nx.NetworkXNoPath:
            length = float('inf')
            print(f"No path between {problem_id1} and {problem_id2}.")
        
        return length


def build_graph_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        
    problem_list = [None]
    for p in data:
        problem_list.append(Problem(p))

    G = TagGraph(problem_list)
    
    return G
