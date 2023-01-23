from random import random, sample as random_sample
import networkx
import gravis
import logging


class RandomWaterDistributionNetwork:
    leak_flow_reduction_range = (0.03, 0.2)
    redirection_probability = 0.1

    @classmethod
    def random_graph_with_one_source(cls, number_of_nodes: int) -> networkx.DiGraph:
        return networkx.gnr_graph(number_of_nodes, cls.redirection_probability).reverse(copy=True)

    @staticmethod
    def random_float_in_range(minimum: float, maximum: float) -> float:
        return minimum + random() * (maximum - minimum)

    @classmethod
    def split_value_randomly(cls, value: int, quantity_to_split_into: int) -> list[int, ...]:
        if quantity_to_split_into <= 0:
            raise ValueError("Can't split a value into 0 or fewer divisions.")

        even_split = value / quantity_to_split_into
        min_allowed, max_allowed = even_split * 0.5, even_split * 1.5
        values = [int(cls.random_float_in_range(min_allowed, max_allowed)) for _ in range(quantity_to_split_into - 1)]
        values.append(value - sum(values))
        return values

    @classmethod
    def assign_flows_to_nodes(cls, network: networkx.DiGraph, start_from_node: int) -> None:
        to_consider = [start_from_node]

        while to_consider:
            currently_considering = to_consider.pop()
            neighbors = list(network.adj[currently_considering])
            if len(neighbors) == 0:
                continue
            neighbor_flows = cls.split_value_randomly(network.nodes[currently_considering]["flow_rate"], len(neighbors))
            for neighbor, flow in zip(neighbors, neighbor_flows):
                network.nodes[neighbor]["flow_rate"] = flow
            to_consider += neighbors

    def add_leak_to_network(self, network: networkx.DiGraph, edge: tuple[int, int]) -> None:
        logging.debug(f"Adding a leak to edge {edge}")
        flow_coefficient = 1 - self.random_float_in_range(*self.leak_flow_reduction_range)
        node_at_end_of_edge = edge[1]
        network.nodes[node_at_end_of_edge]["flow_rate"] = int(network.nodes[node_at_end_of_edge]["flow_rate"] * flow_coefficient)
        self.assign_flows_to_nodes(network, node_at_end_of_edge)

    def add_leaks_to_network(self, network: networkx.DiGraph, num_leaks: int) -> list[tuple[int, int], ...]:
        edges_to_add_leaks_to = random_sample(list(network.edges), num_leaks)
        [self.add_leak_to_network(network, edge) for edge in edges_to_add_leaks_to]
        return edges_to_add_leaks_to

    def random_network(self, number_of_nodes: int, initial_flow: int, number_of_leaks: int) -> networkx.DiGraph:
        graph = self.random_graph_with_one_source(number_of_nodes)
        graph.nodes[0]["flow_rate"] = initial_flow
        self.assign_flows_to_nodes(graph, 0)
        self.add_leaks_to_network(graph, number_of_leaks)

        return graph


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    random_network_maker = RandomWaterDistributionNetwork()
    graph = random_network_maker.random_network(30, 1000, 3)
    fig = gravis.d3(graph)
    fig.display()
