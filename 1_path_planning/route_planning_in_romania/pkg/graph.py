from prettytable import PrettyTable
from pkg.utils import * 

class Node:
   def __init__(self, name):
       self.parent = 0
       self.name = name
       self.edges = []
       self.value = 0
           
   def __lt__(self, other):
      return self.value < other.value
     

class Edge:
   def __init__(self, edge): #INPUT E.G. edge = ('Arad', 'Sibiu', 140)
      self.start = edge[0]
      self.end = edge[1]
      self.value = edge[2]
      
   def __lt__(self, other):
      return self.value < other.value


class Graph:
   def __init__(self, node_list, edges):
      self.nodes = []
      for name in node_list:
         self.nodes.append(Node(name)) #MAKES A LIST OF ALL NODES

      for e in edges:
        e = (getNode(e[0],self.nodes), getNode(e[1], self.nodes), e[2]) # PUTS REAL NODES INTO THE EDGES 

        self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[0].name), -1)].edges.append(Edge(e)) #ADDS EDGES TO THE NODES 
        self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[1].name), -1)].edges.append(Edge((e[1], e[0], e[2]))) #ADDS EDGES TO THE NODES 


   def print(self):
      node_list = self.nodes
      
      t = PrettyTable(['  '] +[i.name for i in node_list])
      for node in node_list:
         edge_values = ['X'] * len(node_list)
         for edge in node.edges:
            edge_values[ next((i for i,e in enumerate(node_list) if e.name == edge.end.name) , -1)] = edge.value           
         t.add_row([node.name] + edge_values)
      print(t)
      
      
   def contains(self, node):
      if isinstance(node, str):
         return any(n.name == node for n in self.nodes)
      if isinstance(node, Node):
         return any(n.name == node.name for n in self.nodes)

   
   def get(self, node_name):
      return next((node for node in self.nodes if node.name == node_name), None)
   
   def print_path(self, goal_node):
      path = []
      total_cost = 0
      current = goal_node

      while current:
         path.append(current.name)
         if current.parent:
            for edge in current.parent.edges:
               if edge.end.name == current.name:
                  total_cost += edge.value
                  break
         current = current.parent

      path.reverse()
      print("Path:", " -> ".join(path))
      print("Total cost:", total_cost)
