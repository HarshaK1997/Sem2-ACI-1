class Network:
    def __init__(self):
        self.adjacency_list = {}

    def add_connection(self, node1, node2, cost):
        if node1 not in self.adjacency_list:
            self.adjacency_list[node1] = []

        self.adjacency_list[node1].append((node2, cost))


    def get_neighbors(self, node):
        return self.adjacency_list.get(node, [])

    def heuristic(self, path_costs):
        return sum(path_costs) / len(path_costs) if path_costs else 0

    def show_transition_state(self,current, path,queue):
        print(f"Current node: {current}")
        print("Queue state:")
        for node, path, cost in queue:
            print(f"Node: {node}, Path: {path}, CumulativepathCost: {cost}")

    def bfs(self, start, goal):
        from collections import deque

        queue = deque([(start, [start], 0)])  # (current node, path, cost)
        visited = set()


        while queue:
            current, path, cost = queue[0]  # Peek at the current state

            current, path, cost = queue.popleft()
            if current in visited:
                continue

            visited.add(current)

            if current == goal:
                print(f"Goal test succeeded. Path found: {path}, Cumulative Cost: {cost}")
                return path, cost
            else:
                print("Goal test failed. Path explored:", path)

            for neighbor, edge_cost in self.get_neighbors(current):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor], cost + edge_cost))

            self.show_transition_state(current, path, queue)  # show transition state


        return path, float('inf')

    def rbfs(self, start, goal):
        import heapq

        def rbfs_helper(node, path, cost, f_limit):
            if node == goal:
                return path, cost

            neighbors = self.get_neighbors(node)
            if not neighbors:
                return None, float('inf')

            successors = []
            for neighbor, edge_cost in neighbors:
                if neighbor not in path:
                    total_cost = cost + edge_cost
                    f_cost = total_cost + self.heuristic([total_cost])
                    heapq.heappush(successors, (f_cost, neighbor, path + [neighbor], total_cost))

            while successors:
                f_cost, next_node, new_path, new_cost = heapq.heappop(successors)
                if f_cost > f_limit:
                    return None, f_cost

                result, best_f_cost = rbfs_helper(next_node, new_path, new_cost, min(f_limit, f_cost))
                if result:
                    return result, best_f_cost

            return None, float('inf')

        return rbfs_helper(start, [start], 0, float('inf'))

    def is_valid_node(self, node):
        return node in self.adjacency_list

    def handle_goal_test(self, start, goal):
        if not self.is_valid_node(start):
            raise ValueError(f"Start node {start} is not valid.")
        if not self.is_valid_node(goal):
            raise ValueError(f"Goal node {goal} is not valid.")

        return self.bfs(start, goal), self.rbfs(start, goal)

    def print_adjacency_table(self):
        print("Adjacency Table:")
        for node, neighbors in self.adjacency_list.items():
            for neighbor, cost in neighbors:
                print(f"{node} -> {neighbor} : {cost}")

    def get_successors(self, node):
        return self.adjacency_list.get(node, [])

# Create the network
network = Network()

# Add connections based on the provided graph
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

for node, connections in graph.items():
    for neighbor, cost in connections:
        network.add_connection(node, neighbor, cost)

# Print adjacency table
network.print_adjacency_table()

def get_dynamic_input():
    start_node = input("Enter the start node: ").strip()
    goal_node = input("Enter the goal node: ").strip()
    return start_node, goal_node

# Get dynamic input for start and goal nodes
start_node, goal_node = get_dynamic_input()

# Check if start and goal nodes are in the graph

if start_node not in graph or goal_node not in graph:
    print("Invalid start or goal node. Please make sure the nodes are in the graph.")
else:
    # Perform BFS and RBFS
    try:
        bfs_result, rbfs_result = network.handle_goal_test(start_node, goal_node)

        print("\nBFS Result:")
        if bfs_result[0]:
            print(f"Path: {bfs_result[0]}, Cumulative Cost: {bfs_result[1]}")
        else:
            print("No path found.")

        print("\nRBFS Result:")
        if rbfs_result[0]:
            print(f"Path: {rbfs_result[0]}, Cumulative Cost: {rbfs_result[1]}")
        else:
            print("No path found.")
    except ValueError as e:
        print(e)

# Perform BFS and RBFS
bfs_result, rbfs_result = network.handle_goal_test(start_node, goal_node)

print("\nBFS Result:")
if bfs_result:
    print(f"Path: {bfs_result[0]}, Cost: {bfs_result[1]}")
else:
    print("No path found.")

print("\nRBFS Result:")
if rbfs_result[0]:
    print(f"Path: {rbfs_result[0]}, Cost: {rbfs_result[1]}")
else:
    print("No path found.")

# Example usage of the transition model/successor function
print(f"\nSuccessors of node '{start_node}':")
successors = network.get_successors(start_node)
for successor in successors:
    print(successor)
