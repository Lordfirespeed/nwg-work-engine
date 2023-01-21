from network import RandomWaterDistributionNetwork
from dataclasses import dataclass
import logging
import networkx
from typing import Optional


@dataclass
class Leak:
    network: networkx.DiGraph
    from_node: int
    flow_loss_coefficient: float

    def potential_leak_edges(self) -> list[tuple[int, int], ...]:
        return [(self.from_node, neighbor) for neighbor in self.network.adj[self.from_node]]


class LeakFinder:
    def find_leaks(self, network: networkx.DiGraph, start_at_node: int = 0) -> list[Leak, ...]:
        to_consider = [start_at_node]

        leaks = []

        while to_consider:
            currently_considering = to_consider.pop()
            neighbors = list(network.adj[currently_considering])
            if len(neighbors) == 0:
                continue

            to_consider += neighbors
            loss = self.get_loss_coefficient(network, currently_considering)

            if loss is None:
                continue

            leaks.append(Leak(network, currently_considering, loss))

        return leaks

    def get_loss_coefficient(self, network: networkx.DiGraph, node: int) -> Optional[float]:
        """Return None if flow is retained, return a loss coefficient otherwise."""
        expected_flow_out = network.nodes[node]["flow_rate"]
        logging.debug(f"Expected flow out of {node} is {expected_flow_out}")
        neighbor_flows = [network.nodes[neighbor]["flow_rate"] for neighbor in list(network.adj[node])]
        actual_flow_out = sum(neighbor_flows)
        logging.debug(f"Actual flow total out of {node} is {actual_flow_out}")

        if actual_flow_out > expected_flow_out:
            raise ValueError("Flow out of a source is less than the flow into the source.")

        if actual_flow_out == expected_flow_out:
            return

        return (expected_flow_out - actual_flow_out) / expected_flow_out


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    random_network_maker = RandomWaterDistributionNetwork()
    graph = random_network_maker.random_network(30, 1000, 3)
    leak_finder = LeakFinder()
    leaks = leak_finder.find_leaks(graph)
    print(leaks)
    print(len(leaks))
