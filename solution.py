import sys
import heapq


node_set = dict()
final_nodes = []
starting_node = None
heruistic_dict = dict()


class Node:
    def __init__(self, name, parent=None, children=[], cost=0, heruistic=0) -> None:
        self.name = name
        self.parent = parent 
        self.children = children
        self.cost = cost
        self.heruistic = heruistic

    def __str__(self) -> str:
        return f"======\nname {self.name}, \n children{self.children}, \n cost{self.cost}\n"

    # napravi string za ispis patha - rekurzino pozivanje self.parent
    def path(self, final_node_name):
        string = []
        string.append(final_node_name)
        current_node = self.parent

        while current_node != None:
            string.append(current_node.name)
            current_node = current_node.parent
        
        return string
    
    # uspredi cijenu 2 nodea
    # preuzeto sa: https://www.geeksforgeeks.org/operator-overloading-in-python/
    def __gt__(self, other):
        if (self.cost + self.heruistic > other.cost + other.heruistic):
            return True
        else:
            return False

        
def parse_input(filename, heruistic=None) -> None:
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
            node_set[line_parts[0][:-1]].append(((line_parts[0][:-1], children_part[0], children_part[1], 0)))

            # sortiraj abecedno
            node_set[line_parts[0][:-1]].sort()
        

    if heruistic:
        file = open(heruistic, mode="r", encoding="utf'8")
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            line = line.split(": ")
            heruistic_dict[line[0]] = line[1]
            for key, values in node_set.items():
                index = 0
                found = False
                tmp2 = None
                for value in values:
                    if value[1] == line[0]:
                        tmp = list(value)
                        tmp[3] = line[1]
                        tmp2 = tuple(tmp)
                        found = True
                        break
                    index += 1
                if found:
                    values[index] = tmp2

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


def ucs(starting_node, print_info=True):    
    if print_info == True:
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
        state = heapq.heappop(open)
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
                #bisect.insort_left(open, Node(next_node[1], state, node_set[next_node[1]], int(next_node[2]) + state.cost))
                heapq.heappush(open, Node(next_node[1], state, node_set[next_node[1]], int(next_node[2]) + state.cost))
                #open.append(Node(next_node[1], state, node_set[next_node[1]], int(next_node[2]) + state.cost))       
    
    # uzmi path
    path = result.path(result.name)

    solution = ""
    if result:
        solution = "yes"
    else:
        solution = "no"
    
    if print_info == True:
        print("[FOUND_SOLUTION]:", solution)
    # ako je pronadjeno rjesenja ispisi dodatne informacije
    if solution == "yes" and print_info == True:
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
    
    return float(result.cost)


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
        state = heapq.heappop(open)
        #print("current state:", state.name)
        # dodaj ga u visited 
        visited.add((state.name, state.cost))
        # provjera jesmo li u ciljnom stanju
        if state.name in final_nodes:
            result = state
            break

        # za svaki sljedeci prijelaz
        for next_node in state.children:
            #print(next_node)
            in_open = False
            in_open_index = 0
            in_open_cost = 0

            in_visited = False
            in_visited_index = 0
            in_visited_cost = 0

            # provjeri je li u open
            for node in open:
                if next_node[1] == node.name:
                    in_open = True
                    in_open_cost = node.cost
                    break
                in_open_index += 1
            # provjeri je li u visited
            for node in visited:
                if next_node[1] == node[1]:
                    in_visited = True
                    in_visited_cost = node[1]
                    break
                in_visited_index += 1

            if in_open:
                # vec postoji u nekom redu
                # provjeri cijenu sa trenutnom 
                if in_open_cost < int(next_node[2]) + int(state.cost):
                    # vec je stavljen sa manjom cijenom
                    continue
                else:
                    # inace ga izbaci
                    open.pop(in_open_index)

            if in_visited:
                if in_visited_cost < int(next_node[2]) + int(state.cost):
                    # vec je posjecen sa manjom cijenom
                    continue
                else:
                    # inace ga izbaci
                    visited.pop(in_visited_index)


            # dodaj ga u open
            # preuzeto sa: https://docs.python.org/3/library/heapq.html
            heapq.heappush(open, Node(next_node[1], state, node_set[next_node[1]], int(next_node[2]) + state.cost, int(next_node[3])))
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


def check_optimistic() -> None:
    fail = False
    for entry in node_set:
        # za svako stanje ucs
        cost = ucs(entry, False)
        heruistic_cost = float(heruistic_dict[entry])

        # provjeri je li stvarna udaljenost manja ili jednaka heruistici
        if float(heruistic_cost) <= float(cost):
            print(f"[CONDITION]: [OK] h({entry}) <= h*: {heruistic_cost} <= {cost}")
        else:
            fail = True
            print(f"[CONDITION]: [ERR] h({entry}) <= h*: {heruistic_cost} <= {cost}")

    if fail == True:
        print("[CONCLUSION]: Heuristic is not optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is optimistic.")

    return


def check_consistent() -> None:
    fail = False
    # za svaki prijaz
    for entry in node_set:
        for child in node_set[entry]:
            #print(entry, " ", child)

            # ukupna cijena i heruistika
            total_cost = float(child[2]) + float(child[3])
            heruistic_cost = heruistic_dict[entry]

            if float(heruistic_cost) <= float(total_cost):
                print(f"[CONDITION]: [OK] h({entry}) <= h({child[1]}) + c: {float(heruistic_cost)} <= {float(child[3])} + {float(child[2])}")
            else:
                fail = True
                print(f"[CONDITION]: [ERR] h({entry}) <= h({child[1]}) + c: {float(heruistic_cost)} <= {float(child[3])} + {float(child[2])}")


    if fail == True:
        print("[CONCLUSION]: Heuristic is not consistent.")
    else:
        print("[CONCLUSION]: Heuristic is consistent.")

    return


def main():
    args = []
    filename = ""
    algo = ""
    heruistic = ""
    check_optimistic_v = False
    check_consistent_v = False
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
        if arg == "--check-optimistic":
            check_optimistic_v = True
        if arg == "--check-consistent":
            check_consistent_v = True
        
    #filename = "files/istra.txt"
    parse_input(filename, heruistic)

    if algo == "bfs":
        bfs()
    elif algo == "ucs":
        ucs(starting_node)
    elif algo == "astar":
        astar()
    elif check_consistent_v == True:
        check_consistent()
    elif check_optimistic_v == True:
        check_optimistic()

    return


if __name__ == "__main__":
    main()