from pkg.graph import Node, Edge, Graph 

class Queue:
    def __init__(self, mode='FIFO'):
        assert mode in ['FIFO', 'LIFO', 'PRIO'], "Mode must be 'FIFO', 'LIFO', or 'PRIO'"
        self.mode = mode
        self.items = []

    def push(self, item):
        if self.mode in ['FIFO', 'LIFO']:
            self.items.append(item)
        elif self.mode in ['PRIO']:
            self.items.append(item)
            self.items.sort(key=lambda x: x.value)
        
    def pop(self):
        if self.mode in ['FIFO', 'PRIO']:
            return self.items.pop(0)
        if self.mode in ['LIFO']:
            return self.items.pop()
                
    def is_empty(self):
        return len(self.items) == 0
    
    def contains(self, node):
      if isinstance(node, str):
         return any(n.name == node for n in self.items)
      if isinstance(node, Node):
         return any(n.name == node.name for n in self.items)
     
            