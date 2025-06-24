from pkg.myqueue import Queue
from pkg.graph import Node, Edge, Graph


def BFS(graph:Graph, start:str, goal:str):
    
    print("BFS")

    if start == goal or not graph.contains(start) or not graph.contains(goal):
        print("INVALID INPUT")
        return -1
    
    startNode = graph.get(start)
    goalNode = graph.get(goal)
        
    frontier = Queue('FIFO')
    frontier.push(startNode)
    explored = Queue()
    path: Queue = Queue()
    
    while not frontier.is_empty():
        node = frontier.pop()
        explored.push(node)
        
        parent = node
        
        for edge in node.edges:
  
            child = edge.end
            if not explored.contains(child) and not frontier.contains(child):
                if child == goalNode:
                    child.parent = parent
                    graph.print_path(child)
                    return graph
                
                child.parent = parent
                frontier.push(child)
    
    
    print("NODE NOT FOUND")            
    return -1

def DFS(graph:Graph, start:str, goal:str):
    
    print("DFS")
    
    if start == goal or not graph.contains(start) or not graph.contains(goal):
        print("INVALID INPUT")
        return -1
    
    startNode = graph.get(start)
    goalNode = graph.get(goal)
        
    frontier = Queue('LIFO')
    frontier.push(startNode)
    explored = Queue()
    path: Queue = Queue()
    
    while not frontier.is_empty():
        node = frontier.pop()
        explored.push(node)
        
        parent = node
        
        for edge in node.edges:
  
            child = edge.end
            if not explored.contains(child) and not frontier.contains(child):
                if child == goalNode:
                    child.parent = parent
                    graph.print_path(child)
                    return graph
                
                child.parent = parent
                frontier.push(child)
    
    
    print("NODE NOT FOUND")            
    return -1

def UCS(graph:Graph, start:str, goal:str):
    
    print("UCS")
    
    if start == goal or not graph.contains(start) or not graph.contains(goal):
        print("INVALID INPUT")
        return -1
    
    pathCost = 0
    startNode = graph.get(start)
    startNode.value = pathCost
    goalNode = graph.get(goal)
        
    frontier = Queue('PRIO')
    frontier.push(startNode)
    explored = Queue()
    path: Queue = Queue()
    
    
    while not frontier.is_empty():
        node = frontier.pop()
        explored.push(node)
        
        parent = node
        
        for edge in node.edges:
  
            child = edge.end
            child.value = node.value + edge.value
            if not explored.contains(child) and not frontier.contains(child):
                if child == goalNode:
                    child.parent = parent
                    graph.print_path(child)
                    return graph
                
                child.parent = parent
                frontier.push(child)
    
    
    print("NODE NOT FOUND")            
    return -1