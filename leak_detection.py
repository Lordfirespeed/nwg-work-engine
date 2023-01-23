from dataclasses import dataclass
import logging
import networkx
from typing import Optional


@dataclass
class Leak:
    network: networkx.DiGraph
    from_node: int
    flow_loss: int

    def potential_leak_edges(self) -> list[tuple[int, int], ...]:
        return [(self.from_node, neighbor) for neighbor in self.network.adj[self.from_node]]

    @property
    def flow_loss_coefficient(self):
        return self.flow_loss / self.network.nodes[self.from_node]["flow_rate"]


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
            loss = self.get_flow_loss(network, currently_considering)

            if loss is None:
                continue

            leaks.append(Leak(network, currently_considering, loss))

        return leaks

    @staticmethod
    def get_flow_at(network: networkx.DiGraph, node: int) -> int:
        return network.nodes[node]["flow_rate"]

    def get_flow_out_total(self, network: networkx.DiGraph, node: int) -> int:
        return sum([self.get_flow_at(network, neighbor) for neighbor in list(network.adj[node])])

    def get_flow_loss(self, network: networkx.DiGraph, node: int) -> Optional[int]:
        """Return None if flow is retained, return a total flow loss otherwise."""
        expected_flow_out = self.get_flow_at(network, node)
        logging.debug(f"Expected flow out of {node} is {expected_flow_out}")
        actual_flow_out = self.get_flow_out_total(network, node)
        logging.debug(f"Actual flow total out of {node} is {actual_flow_out}")

        if actual_flow_out > expected_flow_out:
            raise ValueError("Flow out of a source is less than the flow into the source.")

        if actual_flow_out == expected_flow_out:
            return

        return expected_flow_out - actual_flow_out
