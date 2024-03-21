import sys
import bisect

node_set = dict()
final_nodes = []
starting_node = None


class Node:
    def __init__(self, name, parent=None, children=[], cost=0) -> None:
        self.name = name
        self.parent = parent 
        self.children = children
        self.cost = cost

    def __str__(self) -> str:
        return f"======\nname {self.name}, \n children{self.children}, \n cost{self.cost}\n"

    # napravi string za ispis patha - rekurzino pozivanje self.parent
    def path(self, final_node_name):
        string = []
        string.append(final_node_name)
        current = self.parent

        while current != None:
            string.append(current.name)
            current = current.parent
        
        return string
    
    # preuzeto sa: https://www.geeksforgeeks.org/operator-overloading-in-python/
    # uspredi cijenu 2 nodea
    def __gt__(self, other):
        if(self.cost > other.cost):
            return True
        else:
            return False

        
def parse_input(filename) -> None:
    file = open(filename, mode="r", encoding="utf-8")
    lines = file.readlines()
    counter = 0
    for line in lines:
        line = line.strip()
        # komentar
        if line == "#":
            continue
        # prva linija - pocetno stanje
        if counter == 0:
            global starting_node
            starting_node = line
            node_set[line] = []
            # postavi pocetno stanje
            counter = counter + 1
            continue
        # druga linija - ciljna stanja
        if counter == 1:
            for node_input in line.split(" "):
                node_set[node_input] = []
                #node_set.append(node)
                final_nodes.append(node_input)
            counter = counter + 1
            continue

        # ostale linije, stanje: sljedece,cijena sljedece2,cijena 
        # uzmi trenutno stanje :-1 da se makne : iz imena
        line_parts = line.split(" ")
        first_iteration = True

        # iteriraj po "djeci"
        for children in line_parts:
            if first_iteration:
                # provjeri je li trenutno stanje postoji
                if line_parts[0][:-1] not in node_set:
                    # ako ne dodaj ga u dict
                    node_set[line_parts[0][:-1]] = []
                first_iteration = False
                continue

            children_part = children.split(",")
            node_set[line_parts[0][:-1]].append((line_parts[0][:-1], children_part[0], children_part[1]))

            # sortiraj abecedno
            node_set[line_parts[0][:-1]].sort()
        
    return 


def initial(starting_state) -> Node:
    return Node(starting_state, None, node_set[starting_state])


def bfs() -> None:    
    print("# BFS")
    # pocetno stanje
    open = [initial(starting_node)]
    visited = set()
    result = None
    #print(open[0])

    # dok ima nesto u open
    while len(open) > 0:
        # uzmi prvi element iz open
        state = open.pop(0)
        #print(state.name)
        # dodaj ga u visited 
        visited.add(state.name)
        # provjera jesmo li u ciljnom stanju
        if state.name in final_nodes:
            result = state
            break
        # za svaki sljedeci prijelaz
        for next_node in state.children:
            # ako nije vec posjecen
            if next_node[1] not in visited:
                #print("next", next_node)
                # dodaj ga u open
                open.append(Node(next_node[1], state, node_set[next_node[1]], int(next_node[2]) + state.cost))
    
    # uzmi path
    path = result.path(result.name)

    solution = ""
    if result:
        solution = "yes"
    else:
        solution = "no"
    
    print("[FOUND_SOLUTION]:", solution)
    # ako je pronadjeno rjesenja ispisi dodatne informacije
    if solution == "yes":
        print("[STATES_VISITED]:", len(visited))
        print("[PATH_LENGTH]:", len(path))
        print("[TOTAL_COST]:", float(result.cost))

        # ispis puta
        print("[PATH]:",end=" ")
        counter = 0
        for el in reversed(path):
            print(el, end="")
            if counter != len(path) - 1:
                print(" => ", end="")
            counter = counter + 1

        print()
    
    return 


def ucs() -> None:    
    print("# UCS")
    # pocetno stanje
    open = [initial(starting_node)]
    visited = set()
    result = None

    # sortiraj pocetni node
    open.sort(key=lambda state: state.cost)
    
    # dok ima nesto u open
    while len(open) > 0:
        # uzmi prvi element iz open
        state = open.pop(0)
        #print("current state:", state.name)
        # dodaj ga u visited 
        visited.add(state.name)
        # provjera jesmo li u ciljnom stanju
        if state.name in final_nodes:
            result = state
            break

        # za svaki sljedeci prijelaz
        for next_node in state.children:
            #print(next_node)
            # ako nije vec posjecen
            if next_node[1] not in visited:
                #print("next", next_node)
                # dodaj ga u open
                # preuzeto sa: https://docs.python.org/3/library/bisect.html
                bisect.insort_left(open, Node(next_node[1], state, node_set[next_node[1]], int(next_node[2]) + state.cost))
                #open.append(Node(next_node[1], state, node_set[next_node[1]], int(next_node[2]) + state.cost))       
    
    # uzmi path
    path = result.path(result.name)

    solution = ""
    if result:
        solution = "yes"
    else:
        solution = "no"
    
    print("[FOUND_SOLUTION]:", solution)
    # ako je pronadjeno rjesenja ispisi dodatne informacije
    if solution == "yes":
        print("[STATES_VISITED]:", len(visited))
        print("[PATH_LENGTH]:", len(path))
        print("[TOTAL_COST]:", float(result.cost))

        # ispis puta
        print("[PATH]:",end=" ")
        counter = 0
        for el in reversed(path):
            print(el, end="")
            if counter != len(path) - 1:
                print(" => ", end="")
            counter = counter + 1

        print()
    
    return 

def astar() -> None:
    print("# ASTAR")
    # pocetno stanje
    open = [initial(starting_node)]
    visited = set()
    result = None

    # sortiraj pocetni node
    open.sort(key=lambda state: state.cost)
    
    # dok ima nesto u open
    while len(open) > 0:
        # uzmi prvi element iz open
        state = open.pop(0)
        #print("current state:", state.name)
        # dodaj ga u visited 
        visited.add(state.name)
        # provjera jesmo li u ciljnom stanju
        if state.name in final_nodes:
            result = state
            break

        # za svaki sljedeci prijelaz
        for next_node in state.children:
            #print(next_node)
            # ako nije vec posjecen
            if next_node[1] not in visited:
                #print("next", next_node)
                # dodaj ga u open
                # preuzeto sa: https://docs.python.org/3/library/bisect.html
                bisect.insort_left(open, Node(next_node[1], state, node_set[next_node[1]], int(next_node[2]) + state.cost))
                #open.append(Node(next_node[1], state, node_set[next_node[1]], int(next_node[2]) + state.cost))       
    
    # uzmi path
    path = result.path(result.name)

    solution = ""
    if result:
        solution = "yes"
    else:
        solution = "no"
    
    print("[FOUND_SOLUTION]:", solution)
    # ako je pronadjeno rjesenja ispisi dodatne informacije
    if solution == "yes":
        print("[STATES_VISITED]:", len(visited))
        print("[PATH_LENGTH]:", len(path))
        print("[TOTAL_COST]:", float(result.cost))

        # ispis puta
        print("[PATH]:",end=" ")
        counter = 0
        for el in reversed(path):
            print(el, end="")
            if counter != len(path) - 1:
                print(" => ", end="")
            counter = counter + 1

        print()
    
    return 


    return


def main():
    args = []
    filename = ""
    algo = ""
    heruistic = ""
    check_optimistic = ""
    check_consistent = ""
    for arg in sys.argv:
        args.append(arg)


    args_iter = iter(args)
    for arg in args_iter:
        if arg == "--ss":
            filename = next(args_iter)
        if arg == "--alg":
            algo = next(args_iter)
        if arg == "--h":
            heruistic = next(args_iter)
        if arg == "--check-consistant":
            check_optimistic = next(args_iter)
        if arg == "--check-consistant":
            check_consistent = next(args_iter)
        

    
    #filename = "files/istra.txt"
    parse_input(filename)

    if algo == "bfs":
        bfs()
    elif algo == "ucs":
        ucs()
    elif algo == "astar":
        astar()

    return


if __name__ == "__main__":
    main()