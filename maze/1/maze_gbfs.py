# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 09:56:27 2022

@author: Dell
"""

import sys

class Node():
    def __init__(self, state, parent, action,hueristic,cost_inc):
        self.state = state
        self.parent = parent
        self.action = action
        self.hueristic = hueristic
        self.cost_inc = cost_inc
        self.total_heuristic = hueristic + cost_inc
        

class StackFrontier():
    def __init__(self):
        self.frontier = []
        
    def add(self,node):
        self.frontier.append(node)
        
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
            
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
   

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
            
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class A_star(StackFrontier):
    def remove(self):
        if self.empty():
            return Exception("Empty Frontier")
        else:
            node = min(self.frontier, key= lambda x:x.total_heuristic)
            self.frontier.remove(node)
            return node


class gbfsFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
            
        else:
            node = min(self.frontier, key= lambda x:x.hueristic)
            self.frontier.remove(node)
            return node
        

class Maze():
    
    def __init__(self, filename):
        
        # Read file and set height and width of maze
        
        with open(filename) as f:
            contents = f.read()
            
        #validate start and Goal
            
        if contents.count("A") != 1:
            raise Exception("maze must have excatly one start point")
            
        if contents.count("B") != 1:
            raise Exception("maze must have excatly one goal")
            
        #determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        
        #keep track of walls
        self.walls = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i,j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
            
        self.solution = None
    
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    print("#", end="")
                elif (i,j) == self.start:
                    print("A",end="")
                elif (i,j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i,j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
                
            print()
        print()
        
    def neighbors(self, state):
        row,col = state
        candidates=[
            ("up",(row-1,col)),
            ("down",(row+1,col)),
            ("left",(row,col-1)),
            ("right",(row,col+1))]
        
        result = []
        for action, (r,c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action,(r,c)))
        return result
    
    
    def solve(self):
        """Finds a solution to maze, if one exists"""
        
        #keep track of states explored
        self.num_explored = 0
        
        #Initialise frontier to just the starting position
        cost = abs(self.goal[0]-self.start[0]) + abs(self.goal[1]-self.start[1])
        start = Node(state=self.start, parent=None, action=None, hueristic=cost ,cost_inc = 0) 
        frontier = A_star()
        frontier.add(start)
        
        #Initialise an empty explored set
        self.explored = set()
        
        
        #keep looping until solution found
        while True:
            #if nothing left in frontier then no path
            if frontier.empty():
                raise Exception("no solution")
                
            #Choose a node from the frontier
            node = frontier.remove()
            self.num_explored +=1
            
            #if node is the goal,then we have a solution
            if node.state == self.goal:
                actions=[]
                cells=[]
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution=(actions, cells)
                return
                
            #mark node as explored
            self.explored.add(node.state)
            
            #Add neighbour to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    cost = abs(state[0]-self.goal[0]) + abs(state[1]-self.goal[1])
                    child = Node(state=state, parent=node, action=action, hueristic=cost , cost_inc = node.cost_inc+1)
                    frontier.add(child)
                    
                    
if len(sys.argv)!=2:
    sys.exit("Usage: python maze.py maze.txt")
    
m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving....")
m.solve()
print("States Explored:",m.num_explored)
print("Solution:")
m.print()
