import sys
import copy

class Node():
    def __init__(self, state, parent, action, heuristic):
        self.state = state
        self.parent = parent
        self.action = action
        self.heuristic = heuristic


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class gbfsFrontier(StackFrontier):   #new added
    
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = min(self.frontier, key= lambda x: x.heuristic)
            self.frontier.remove(node)
            return node

class Puzzle():

    def __init__(self, filename):

        # Read file and set height and width of puzzle
        with open(filename) as f:
            contents = f.read()


        # Determine height and width of puzzle
        
        puzzle = contents.split("\n")
        
        self.height = len(puzzle)
        self.width = max(len(line) for line in puzzle)

        self.array_puzzle = []

        for row in puzzle:
            row = list(row)
            self.array_puzzle.append(row)
        
        self.goal_puzzle = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", " "]]
        
        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()       
        print(self.array_puzzle)
        if solution is not None:
            for st in solution:
                print(st)
            print("No. of steps: ", len(solution))   

    def neighbors(self, state):

        for i, row in enumerate(state):
            for j, col in enumerate(row):
                if col == " ":
                    x = i
                    y = j
                    
        candidates = [
            ("up", (x - 1, y)),
            ("down", (x + 1, y)),
            ("left", (x, y - 1)),
            ("right", (x, y + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width:
                dummy = copy.deepcopy(state)
                temp = dummy[r][c]
                dummy[r][c] = " "
                dummy[x][y] = temp
                
                result.append((action, dummy))
                
        return result

    def calc_heu(self, state):
        i = 1
        n_misplaced = 0
        for row in state:
            for col in row:
                if col != str(i):
                    n_misplaced = n_misplaced+1
                i = i+1
                
        return n_misplaced
    
    
    def solve(self):
        """Finds a solution to puzzle, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        heu = self.calc_heu(self.array_puzzle)
        start = Node(state=self.array_puzzle, parent=None, action=None, heuristic = heu)

        frontier = gbfsFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = []

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            #print(node.state)
            #print(node.heuristic)
            if node.state == self.goal_puzzle:
                print("Solved")
                actions = []
                states = []
                while node.parent is not None:
                    actions.append(node.action)
                    states.append(node.state)
                    node = node.parent
                actions.reverse()
                states.reverse()
                self.solution = (actions, states)
                return

            # Mark node as explored
            self.explored.append(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    heu = self.calc_heu(state)
                    child = Node(state=state, parent=node, action=action, heuristic = heu)
                    frontier.add(child)


#m = Puzzle("two.txt")
#m.solve()



if len(sys.argv) != 2:
    sys.exit("Usage: python puzzle.py puzzle.txt")

m = Puzzle(sys.argv[1])

print("Puzzle:")
m.print()
print("Solving...")
m.solve()
print("Solution:")
m.print()
print("States Explored:", m.num_explored)

