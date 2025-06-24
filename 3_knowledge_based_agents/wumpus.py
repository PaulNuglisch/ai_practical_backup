import gym
import fh_ac_ai_gym

actions = {
        "w": 0,
        "l": 1,
        "r": 2,
        "s": 3,
        "g": 4,
        "c": 5,
        "a": "ask",
        "t": "tell"
    }

class KnowledgeBase:
    def __init__(self, method):
        self.method = method
        self.cnf_clauses = []
        self.facts = set() #{"B11"}
        self.horn_rules = [] #{"B11", "L11=>P11"}

    def tell(self, sentence):
        if self.method == "resolution":      
            clause = frozenset(sentence)
            if not clause in self.cnf_clauses:
                contradictions = [existing for existing in self.cnf_clauses if self._contradicts_existing(clause, existing)]
                if contradictions:
                    print(f"WARNING CONTRADICTION: {clause} contradicts with {contradictions}")
                    return
                self.cnf_clauses.append(clause)
                #print(f"[Info] Neue Klausel hinzugefügt: {clause}")
                
        elif self.method == "forward":
            if len(sentence) == 1: #set length is 1
                self.facts |= sentence
            elif any("=>" in s for s in sentence):
                premises, conclusion = self._parse_horn(sentence)
                self.horn_rules.append((premises, conclusion))
                
    def _parse_horn(self, sentence):
        premises = set()
        conclusion = None
        for s in sentence:
            if "=>" in s:
                left, right= s.split("=>")
                conclusion = right.strip()
            else:
                premises.add(s.strip())
        return premises, conclusion    

    def _contradicts_existing(self, clause1, clause2):
        for literal in clause1:
            #create negation
            negation = f"-{literal}" if literal[0] != "-" else literal[1:]
            if negation in clause2:
                #resolution
                if not frozenset(l for l in clause1 | clause2 if l != literal and l != negation):
                    return True
        return False

    def ask(self, literal):
        if self.method == "resolution":
            return self._resolution_ask(literal)
        if self.method == "forward":
            return self._forward_ask(literal)

    def _resolution_ask(self, literal):
        #create negation
        negation = f"-{literal}" if literal[0] != "-" else literal[1:]

        clauses = self.cnf_clauses.copy()
        query_clause = frozenset({negation})
        clauses.append(query_clause)
       
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                # print()
                # print(f"Resolvement {i}")
                for j in range(i + 1, len(clauses)):
                    resolvents = self._resolve(clauses[i], clauses[j])
                    for resolvent in resolvents:
                        
                        if resolvent == frozenset():
                            # print("RESOLVENTS THAT LEAD TO RESULT")
                            # print(resolvents)
                            print(f"KB |= {literal}")
                            return True
                    new_clauses = new_clauses + resolvents
                    
            if all(clause in clauses for clause in new_clauses):
                print(f"KB |= not {literal}")
                return False
            clauses.extend(new_clauses)
    
    def _forward_ask(self, literal):
        inferred = set(self.facts)
        changed = True

        while changed:
            changed = False
            for premises, conclusion in self.horn_rules:
                if premises <= inferred and conclusion not in inferred:
                    inferred.add(conclusion)
                    changed = True
                    
        if literal in inferred:
            print(f"KB |= {literal}")   
            return True
        if literal not in inferred:
            print(f"KB |= not {literal}")
                       
    def _resolve(self, clause1, clause2):
        resolvents = []
        for literal1 in clause1:
            negation1 = f"-{literal1}" if literal1[0] != "-" else literal1[1:]
            
            #if there is a conflict
            for literal2 in clause2:
                if negation1 == literal2:
                    #if negation in clause2:
                    new_clause = frozenset(
                        l for l in clause1 | clause2 if l != literal1 and l != negation1
                    )
                    resolvents.append(new_clause)
        print(clause1)
        print(clause2)    
        print(resolvents)
        return resolvents

    def print_kb(self):
        
        if self.method == "resolution":
            print("Current resolution Knowledge Base:")
            print("Facts:")
            for i, clause in enumerate(self.cnf_clauses, 1):
                print(f"Clause {i}: {clause}")
        elif self.method == "forward":
            print("Current horn Knowledge Base:")
            print("Facts:")
            for fact in sorted(self.facts):
                print(f"  {fact}")
            print("Horn Rules:")
            for i, (premises, conclusion) in enumerate(self.horn_rules, 1):
                premise_str = " ∧ ".join(sorted(premises))
                print(f"  Rule {i}: {premise_str} => {conclusion}")
    
def update_resolution_kb(kb: KnowledgeBase, perceptions: list = [],x: int = 1, y: int = 1):
    
    #Start field is safe (no pit, no wumpus)
    
    #print(perceptions)
    
    kb.tell({f"S{x}{y}"} if perceptions["stench"]  else {f"-S{x}{y}"})
    kb.tell({f"B{x}{y}"} if perceptions["breeze"] else {f"-B{x}{y}"})
    kb.tell({f"G{x}{y}"} if perceptions["glitter"] else {f"-G{x}{y}"})
    
    kb.tell({f"-W{x}{y}"}) 
    kb.tell({f"-P{x}{y}"})

    adjacent = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 1 <= nx <= 4 and 1 <= ny <= 4:
            adjacent.append((nx, ny))

    if perceptions["stench"]:
        for i, (nx, ny) in enumerate(adjacent):
            premises = {f"-S{x}{y}"}
            for j, (ox, oy) in enumerate(adjacent):
                if (ox, oy) != (nx, ny):
                    premises.add(f"W{ox}{oy}")
            premises.add(f"W{nx}{ny}")
            kb.tell(premises)
         
    if perceptions["breeze"]:
        for i, (nx, ny) in enumerate(adjacent):
            premises = {f"-B{x}{y}"}
            for j, (ox, oy) in enumerate(adjacent):
                if (ox, oy) != (nx, ny):
                    premises.add(f"P{ox}{oy}")
            premises.add(f"P{nx}{ny}")
            kb.tell(premises)  
        
def update_forward_kb(kb: KnowledgeBase, perceptions: list = [],x: int = 1, y: int = 1):
    
    #Start field is safe (no pit, no wumpus)
    
    #print(perceptions)
    
    kb.tell({f"S{x}{y}"} if perceptions["stench"]  else {f"-S{x}{y}"})
    kb.tell({f"B{x}{y}"} if perceptions["breeze"] else {f"-B{x}{y}"})
    kb.tell({f"G{x}{y}"} if perceptions["glitter"] else {f"-G{x}{y}"})
    
    kb.tell({f"-W{x}{y}"}) 
    kb.tell({f"-P{x}{y}"})

    adjacent = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 1 <= nx <= 4 and 1 <= ny <= 4:
            adjacent.append((nx, ny))

    # Breeze rules (adjacent to pits)
    if perceptions["breeze"]:
        for i, (nx, ny) in enumerate(adjacent):
            premises = {f"B{x}{y}"}
            for j, (ox, oy) in enumerate(adjacent):
                if (ox, oy) != (nx, ny):
                    premises.add(f"-P{ox}{oy}")
            premises.add(f"=>P{nx}{ny}")
            kb.tell(premises)

    # Stench rules (adjacent to wumpus)
    if perceptions["stench"]:
        for i, (nx, ny) in enumerate(adjacent):
            premises = {f"S{x}{y}"}
            for j, (ox, oy) in enumerate(adjacent):
                if (ox, oy) != (nx, ny):
                    premises.add(f"-W{ox}{oy}")
            premises.add(f"=>W{nx}{ny}")
            kb.tell(premises)

def move(wumpus_env: gym, kb: KnowledgeBase, pos: map, direction: int, action: str):
    
    if action == "l":
        direction = (direction - 1) % 4
    if action == "r":
        direction = (direction + 1) % 4
    
    if action == "w":
        match direction:
            case 0: pos["x"] += 1
            case 1: pos["y"] -= 1
            case 2: pos["x"] -= 1
            case 3: pos["y"] += 1  
                
    perceptions, reward, done, info = wumpus_env.step(actions[user_input])
    
    if kb.method == "resolution":
        update_resolution_kb(kb, perceptions, pos["x"], pos["y"])
    if kb.method == "forward":
        update_forward_kb(kb, perceptions, pos["x"], pos["y"])
    
    print("POSITION:")
    print(f"X: {pos['x']}")
    print(f"y: {pos['y']}")
    
    return direction

    
print("START THE WUMPUS GAME!")
print()
print("Select your solving algorithm:")
print("1 -> Resolution")
print("2 -> Forward chaining")
selected_algorithm = input()

wumpus_env = gym.make('Wumpus-v0', disable_env_checker=True)
perceptions = wumpus_env.reset()

if selected_algorithm == "1":
    kb = KnowledgeBase(method="resolution")
    update_resolution_kb(kb, perceptions)
elif selected_algorithm == "2":
    kb = KnowledgeBase(method="forward")
    update_forward_kb(kb, perceptions)
else:
    print("Invalid selection. Defaulting to resolution.")
    kb = KnowledgeBase(method="resolution")
    update_resolution_kb(kb, perceptions)
    
user_input: str = "start"
pos = {"x": 1, "y": 1}
directions = {0:"r", 1: "d", 2: "l", 3: "u"}
direction: int = 0

while user_input != "q":
    
    print("THE WUMPUS GAME:")
    print()
    print("GIVEN OPERATIONS")
    print("walk: w")
    print("turn left: l")
    print("turn right: r")
    print("shoot: s")
    print("grab: g")
    print("climb: c")
    print()
    print("ask: a")
    print("tell: t")
    print()
    print("quit: q")
    print()
    wumpus_env.render()
    user_input = input("Your input: ")
    
    if user_input == "q":
        break  # quit the game

    match user_input:
        case "w" | "l" | "r" | "s" | "g" | "c":
            direction = move(wumpus_env, kb, pos, direction, user_input)
        case "a":
            query = input("What do you want to ask (e.g. P12)? ")
            kb.ask(query)
            print()
            kb.print_kb()
        case "t":
            sentence = input("Enter clause (e.g. -P12,B11): ")
            clause = set(s.strip() for s in sentence.split(","))
            kb.tell(clause)
        case _:
            print("Invalid input.")
       



