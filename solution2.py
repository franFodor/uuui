import sys
import copy

clauses = []
final_clause = ''
no_of_premises = 0
no_of_new_clauses = 0
index_deduced = 0
index_total = 0
clause_index = 0
nil_pair = None
        
def parse_input(filename) -> None:
    global clause_index
    file = open(filename, mode="r", encoding="utf-8")
    lines = file.readlines()
    counter = 0
    counter_2 = 0
    for line in lines:
        line = line.strip()
        line = line.lower()
        # komentar
        if line == "#":
            continue
        line_tmp = line
        line = line.split(" v ")

        clauses_tmp = []
        # dosli smo do zadnje linije
        if counter == len(lines) - 1:
            global final_clause
            final_clause = line_tmp
            # ako je manji od 3 - sadrzi samo jedan literal
            if len(line) < 2:
                for clause in line:
                    if "~" in clause:
                        clauses_tmp.append(clause.replace("~", ""))
                    elif "~" not in clause:
                        clauses_tmp.append("~" + clause)
                clauses.append((clauses_tmp, clause_index, None))
                clause_index += 1
                break
            # neki kompleksiniji izraz, treba parsat
            else:
                for clause in line:
                    if "~" in clause:
                        clauses_tmp.append(clause.replace("~", ""))
                    elif "~" not in clause:
                        clauses_tmp.append("~" + clause)
                    if clauses_tmp not in clauses:
                        clauses.append((clauses_tmp, clause_index, None))
                        clause_index += 1
                        clauses_tmp = []
                    
                break

        for clause in line:
            # provjeri tautologiju nekak
            clauses_tmp.append(clause)

        flag = True
        for literal in clauses_tmp.copy():
            for literal_2 in clauses_tmp.copy():
                if literal == "~" + literal_2 or literal_2 == "~" + literal:
                    counter_2 -= 1
                    flag = False
        if flag == True:
            clauses.append((clauses_tmp, clause_index, None))
            clause_index += 1

        counter += 1
        counter_2 += 1

    global no_of_premises, no_of_new_clauses
    tmp = len(clauses) - counter_2
    no_of_premises = len(clauses) - tmp

    return 


# TODO izbacit duplikate iz liste

def select_clauses() -> tuple:
    # ako imaju komplementarne literale vrati ih
    # TODO prepravit da ide po SoS

    global index_total, index_deduced
    #print("totaln", index_total)
    #print("deduced ",index_deduced)

    for clause in clauses[index_deduced:]:
        for clause_2 in clauses[index_total:]:
            for literal_i in clause_2[0]:
                literal = literal_i
                #print("+++++++++++++++++++++")
                #print(clause)
                #print(clause_2)
                #print(literal)
                # makni negaciju
                if "~" in literal:
                    literal = literal.replace("~", "")
                    literal_r = literal
                    
                # dodaj negaciju 
                else:
                    literal_r = literal
                    literal = "~" + literal
                ##print(literal)
                if literal in clause[0]:
                    index_total += 1
                    return (clause[0], clause_2[0], literal_r, clause[1], clause_2[1])
            index_total += 1
            if index_total > no_of_premises and index_deduced < no_of_premises:
                index_total = 0
        #print("BRUH MOMENTO")
        index_total = 0
        index_deduced += 1

    return None


def pl_resolve(pair) -> list:
    # copy jer modificira orginalni clauses inace jer ima referencu idalje
    pair_tmp = copy.deepcopy(pair)
    #print("ULAY--------------------------")
    #print(pair)
    global clause_index
    
    # makni ga iz prve
    if pair[2] in pair[0]:
        pair_tmp[0].remove(pair[2])
    elif "~" + pair[2] in pair[0]:
        pair_tmp[0].remove("~" + pair[2])

    # makni ga iz druge
    if pair[2] in pair[1]:
        pair_tmp[1].remove(pair[2])
    elif "~" + pair[2] in pair[1]:
        pair_tmp[1].remove("~" + pair[2])

    # ponistili smo ih -> nasli smo NIL
    if len(pair_tmp[0]) == 0 and len(pair_tmp[1]) == 0:
        global nil_pair
        nil_pair = pair
        return None
    

    if pair_tmp[0] == pair_tmp[1]:
        return_val = (pair_tmp[0], clause_index, (pair_tmp[3], pair_tmp[4]))
        clause_index += 1
        return return_val
    else:
        return_val = (pair_tmp[0] + pair_tmp[1], clause_index, (pair_tmp[3], pair_tmp[4]))
        clause_index += 1
        return return_val


def update_list_of_lists(list_of_lists, target_list):
    target_set = set(target_list)
    for i, sublist in enumerate(list_of_lists):
        if target_set.issubset(sublist):
            list_of_lists.pop(i)
            list_of_lists.append(target_list)
            return

def remove_redundant(clauses, pair) -> list:


    return

def remove_unimportant(pair) -> list:
    #print("BRUAZ KOJI KURAC", pair)
    # tautologija
    for literal in pair[0]:
        for literal_2 in pair[0]:
            if literal == "~" + literal_2 or literal_2 == "~" + literal:
                #print("ALOOOOO", literal, literal_2)
                #exit()
                return None
    # faktorizacija
    pair = list(set(pair[0]))
            
    return pair

def pl_resolution() -> bool:
    new = []
    global index_deduced, no_of_premises, clauses, index_total
    index_deduced = no_of_premises - 1
    while True:
        #print("----------------------------\nnova iteracija") 
        # nova iteracija, dodane nove klauzule
        #print("premisa", no_of_premises, index_deduced)
        if index_deduced <= no_of_premises:
            index_deduced = no_of_premises
        else:
            index_deduced += 1 
        index_total = 0
        pair = select_clauses()   
        if pair == None: 
            return False
        #print("par2", pair)

        while pair != None:
            resolvents = pl_resolve(pair)
            #print("RESOLVENT", resolvents)

            # ako je NIL
            if resolvents == None:
                #print("NIL")
                #print(clauses)
                return True
            
            # TODO ove dve funkcije prepravit, i mozda rewrite sa klasom za klauzulu

            ##print(remove_redundant(clauses, resolvents))
            #resolvents = remove_unimportant(resolvents)
            if resolvents != None:
                # dodaj u new
                if resolvents not in new:
                    new.append(resolvents)

            

            #print("NOVI BURAQ", new)
            #print(clauses)

            pair = select_clauses()    
            #print("par", pair)

        
        #print("clause prie", clauses)
        #print("new prie", new)
        flag = False
        for clause in new:
            if clause not in clauses:
                flag = True
                break
        if flag == False:
            return False
        

        tmp = len(clauses) - no_of_premises
        no_of_premises = no_of_premises + tmp

        #print("broj premisa, zelimo da bude index sa kojeg se nanovo krece", no_of_premises)

        for clause in new:
            #print("BRATE STA JE OVO")
            #print(clause)
            if clause not in clauses:
                clauses.append(clause)
        #print(clauses)

    
    return    


def find_path(path, parents) -> None:
    for clause in clauses:
        if clause[1] in parents:
            if clause[2] is not None:
                find_path(path, clause[2])    
            if clause[2] is not None:
                tmp = ""
                last_flag = False
                i = 0
                for literal in clause[0]:
                    tmp += literal
                    if i == len(clause[0]) - 1:
                        last_flag = True
                    if last_flag == False:
                        tmp += " v "
                    i += 1
                    
                path[clause[1]] = f". {tmp} {clause[2]}"
            else:
                tmp = ""
                last_flag = False
                i = 0
                for literal in clause[0]:
                    tmp += literal
                    if i == len(clause[0]) - 1:
                        last_flag = True
                    if last_flag == False:
                        tmp += " v "
                    i += 1

                path[clause[1]] = f". {tmp}"

    return

def main():
    args = []
    filename = ""
    mode = ""
    for arg in sys.argv:
        args.append(arg)


    args_iter = iter(args)
    # preskoci prvi argument (ime programa)
    
    _ = next(args_iter)
    mode = next(args_iter)
    filename = next(args_iter)
    parse_input(filename)
    #print("pocetno", clauses)


    if mode == "resolution":
        if pl_resolution() == True:
            path = {}
            find_path(path, set((nil_pair[3], nil_pair[4])))
            path = dict(sorted(path.items()))
            for key, value in path.items():
                print(key, value)
            print(f"NIL iz ({nil_pair[3]}, {nil_pair[4]})")   
            print(f"[CONCLUSION]: {final_clause} is true")
        else:
            print(f"[CONCLUSION]: {final_clause} is unknown")

    elif mode == "cooking":
        pass
        #cooking()

    return


if __name__ == "__main__":
    main()