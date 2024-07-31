import heapq


class GraphHeuristics:
    def __init__(self, graph, goal):
        self.graph = graph
        self.goal = goal
        self.heuristics = self.compute_heuristics()

    def all_paths(self, start):
        """ Generate all paths from start to goal in the graph """
        paths = []
        stack = [(start, [start])]

        while stack:
            (node, path) = stack.pop()
            for (next_node, weight) in self.graph.get(node, []):
                if next_node in path:
                    continue
                if next_node == self.goal:
                    paths.append(path + [next_node])
                else:
                    stack.append((next_node, path + [next_node]))

        print(paths)
        return paths

    def path_cost(self, path):
        """ Calculate the cost of a given path """
        cost = 0
        for i in range(len(path) - 1):

            for (next_node, weight) in self.graph[path[i]]:


                if next_node == path[i + 1]:

                    cost += weight

                    break

        return cost

    def average_path_cost(self, start):
        """ Calculate the average path cost from start to goal """
        paths = self.all_paths(start)
        if not paths:
            return float('inf')

        total_cost = sum(self.path_cost(path) for path in paths)

        return total_cost / len(paths)

    def compute_heuristics(self):
        """ Compute heuristic values for all nodes based on the average path cost to the goal """
        h_cost = {}
        for node in self.graph:
            if node != self.goal:
                h_cost[node] = self.average_path_cost(node)
                print(self.average_path_cost(node))
            else:
                h_cost[node] = 0

        return h_cost

    def rbfs(self, node, goal,f_limit=float('inf'),g_cost=0, path=[], visited=set()):
        """ Recursive Best-First Search (RBFS) """
        if node == goal:
            return (g_cost, path + [node])

        visited.add(node)
        successors = []
        for neighbor, weight in self.graph.get(node, []):
            if neighbor not in visited:
                new_g_cost = g_cost + weight
                new_f_cost = new_g_cost + self.heuristics.get(neighbor, 0)
                successors.append((new_f_cost, neighbor, new_g_cost))

        if not successors:
            visited.remove(node)
            return (float('inf'), path)

        while successors:
            successors.sort()  # Sort successors by f_cost
            best_f_cost, best_node, best_g_cost = successors[0]
            alternative = successors[1][0] if len(successors) > 1 else float('inf')
            result_cost, result_path = self.rbfs(best_node, goal, min(f_limit, alternative), best_g_cost, path + [node],
                                                 visited)
            if result_cost < float('inf'):
                return (result_cost, result_path)
            successors[0] = (result_cost, best_node, best_g_cost)

        visited.remove(node)
        return (float('inf'), [])

    def rbfs_search(self, start, goal):
        """ Initialize RBFS Search """
        return self.rbfs(start, goal)



# Example usage
graph = {
    'A': [('B', 15), ('C', 10), ('G', 5), ('D', 17)],
    'B': [('A', 15), ('D', 12)],
    'C': [('A', 10), ('G', 7)],
    'D': [('A', 17), ('B', 12), ('E', 2), ('F', 10), ('H', 4)],
    'E': [('D', 2)],
    'F': [('D', 10), ('H', 11)],
    'G': [('C', 7), ('A', 5), ('H', 25)],
    'H': [('D', 4), ('F', 11), ('G', 25)]
}

goal_node = 'F'
graph_heuristics = GraphHeuristics(graph, goal_node)

# Run RBFS Search
start_node = 'A'
cost, path = graph_heuristics.rbfs_search(start_node, goal_node)

print(f"Minimum cost: {cost}")
print(f"Path: {' -> '.join(path)}")
