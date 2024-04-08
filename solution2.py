import sys

# list of all clauses
all_clauses = []
# list of clasuses that are being used - ie when we remove redundant ones
relevant_clauses = []
# index to keep track of clauses
clause_index = 0
# final clause so we can print it in the end
final_clause = ""
# final parents tuple
final_parents = None
# final clause
final_clause_2 = None
# all clauses for cooking
cooking_all = []
# path to NIL
path = []


# index for SoS start
sos_index = 0
# index for the other SoS
total_index = 0


class Literal:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type
    
    def __str__(self) -> str:
        if self.type == False:
            return f"~{self.name}"
        else:
            return f"{self.name}"

    def __eq__(self, other) -> bool:
        if self.name == other.name and self.type == other.type:
            return True
        return False

    def __hash__(self):
        return hash((self.name, self.type))


class Clause:
    def __init__(self, literals, index, parent=None) -> None:
        self.literals = literals
        self.index = index
        self.parent = parent

    def __repr__(self) -> str:
        return f"{self.index}. {' v '.join(str(literal) for literal in self.literals)} from {self.parent}"

    def __str__(self) -> str:
        return f"{self.index}. {' v '.join(str(literal) for literal in self.literals)} from {self.parent}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Clause):
            return False
        if len(self.literals) != len(other.literals):
            return False
        for literal_self, literal_other in zip(self.literals, other.literals):
            if literal_self.name != literal_other.name or literal_self.type != literal_other.type:
                return False
        return True

    def __hash__(self):
        return hash(tuple(self.literals))

    def factiorization(self) -> None:
        for i, literal in enumerate(self.literals.copy()):
            for literal_2 in list(self.literals.copy())[i+1:]:
                # if there are two equal literals, remove one of them
                if literal.name == literal_2.name and literal.type == literal_2.type:
                    self.literals.remove(literal_2)

    def tautology(self) -> bool:
        for i, literal in enumerate(self.literals):
            for literal_2 in list(self.literals.copy())[i+1:]:
                # if there is a literal and its complement dont add it
                if literal.name == literal_2.name and literal.type != literal_2.type:
                    return False
                
        return True
    
    def subset(self, other_clause):
        # Convert literals to a set for faster lookup
        other_literals_set = {literal.name: literal.type for literal in other_clause.literals}

        # Check if each literal in self is present in other_clause
        for literal in self.literals:
            if literal.name not in other_literals_set or literal.type != other_literals_set[literal.name]:
                return False
        return True


def resolve(clause_1, clause_2, resolve_literal) -> "Clause":
    clause_tmp = set()
    # search until you find the literal and skip it, add the rest to the new clause
    for literal in clause_1.literals:
        for literal_2 in clause_2.literals:
            if literal_2.name != resolve_literal.name:
                clause_tmp.add(literal_2)
        if literal.name != resolve_literal.name:
            clause_tmp.add(literal)

    global clause_index
    return_clause = Clause(clause_tmp, clause_index, (clause_1.index, clause_2.index))
    clause_index += 1 
    return return_clause


def print_clauses() -> None:
    for clause in relevant_clauses:
        print(clause)
    return


def print_clauses_all() -> None:
    for clause in all_clauses:
        print(clause)
    return


def parse_input(filename, cooking_input="") -> None:
    global clause_index, relevant_clauses, all_clauses
    file = open(filename, mode="r", encoding="utf-8")
    lines = file.readlines()

    # counter to keep track of lines so we know when we reached the last one
    counter = 0

    # counter to keep track of where the starting SoS is 
    counter_sos = 0

    # number of comments
    no_of_comments = 0

    for line in lines:
        line = line.strip()
        line = line.lower()
        # comment line
        if "#" in line:
            no_of_comments += 1
            continue

        line_tmp = line
        line = line.split(" v ")

        # temp list to keep track of literals in the current line
        clause_tmp = set()

        # last line, we need to negate it
        if counter == len(lines) - 1 - no_of_comments and not cooking_input:
            global sos_index
            sos_index = counter_sos
            global final_clause
            final_clause = line_tmp
            # if its less than 2 it means there is only one literal
            if len(line) < 2:
                for clause in line:
                    if "~" in clause:
                        name = clause.replace("~", "")
                        clause_tmp.add(Literal(name, True))
                    elif "~" not in clause:
                        name = clause
                        clause_tmp.add(Literal(name, False))
                all_clauses.append(Clause(list(clause_tmp), clause_index, None))
                clause_index += 1
                break
            # more literals, have to use demorgan
            else:
                for clause in line:
                    if "~" in clause:
                        name = clause.replace("~", "")
                        clause_tmp.add(Literal(name, True))
                    elif "~" not in clause:
                        name = clause
                        clause_tmp.add(Literal(name, False))
                    if clause_tmp not in all_clauses:
                        all_clauses.append(Clause((clause_tmp), clause_index, None))
                        clause_index += 1
                        clause_tmp = set()
                    
                break

        # for each literal in line
        for literal in line:
            if "~" in literal:
                name = literal.replace("~", "")
                clause_tmp.add(Literal(name, False))
            else:
                name = literal
                clause_tmp.add(Literal(name, True))

        # create a clause and add it to list (if its not tautology)
        clause = Clause(list(clause_tmp), clause_index, None)
        if clause.tautology():
            clause.factiorization()
            all_clauses.append(clause)
            clause_index += 1
            counter_sos += 1
        
        counter += 1

    # add them to relevant_clauses
    relevant_clauses = all_clauses.copy()

    if cooking_input:
        file = open(cooking_input, mode="r", encoding="utf-8")
        lines = file.readlines()

        first_flag = True

        for line in lines:
            line = line.strip()
            line = line.lower()

            print("\nUser's command:", line)

            # if it is out first time thru, set sos to counter
            if first_flag:
                sos_index = counter_sos
                first_flag = False

            if line.endswith("?"):
                relevant_clauses = all_clauses.copy()
                clause_tmp = set()
                line = line.split(" ?")
                final_clause = line[0]
                # negate the input
                if "~" in line[0]:
                    name = line[0].replace("~", "")
                    clause_tmp.add(Literal(name, True))
                elif "~" not in line[0]:
                    name = line[0]
                    clause_tmp.add(Literal(name, False))
                if clause_tmp not in all_clauses:
                    all_clauses.append(Clause((clause_tmp), clause_index, None))
                    relevant_clauses.append(Clause((clause_tmp), clause_index, None))
                    clause_index += 1

                # save index and clauses before
                sos_before = sos_index
                clauses_before = all_clauses.copy()
                if pl_resolution():
                    find_path(path, final_clause_2)
                    path_s = sorted(path, key=lambda x: x.index)
                    for el in path_s:
                        print(el)
                    print(f"NIL {final_parents}")
                    print(f"[CONCLUSION]: {final_clause} is true")
                else:
                    print(f"[CONCLUSION]: {final_clause} is unknown")

                sos_index = sos_before
                all_clauses = clauses_before

                # remove the command
                all_clauses.pop()
                sos_index -= 1

                # clear list of clauses
                cooking_all.clear()
                
                
            elif line.endswith("-"):
                line = line.split(" -")
                clause_tmp = set()

                to_remove = line[0]

                line = line[0].split(" v ")
                for literal in line:
                    if "~" in literal:
                        name = literal.replace("~", "")
                        clause_tmp.add(Literal(name, False))
                    else:
                        name = literal
                        clause_tmp.add(Literal(name, True))

                clause = Clause((clause_tmp), clause_index, None)
                clause_index += 1
                if clause in all_clauses:
                    all_clauses.remove(clause)
                    sos_index -= 1
                
                print(f"Removed {to_remove}")

                    
            elif line.endswith("+"):
                line = line.split(" +")
                clause_tmp = set()

                to_add = line[0]

                line = line[0].split(" v ")
                for literal in line:
                    if "~" in literal:
                        name = literal.replace("~", "")
                        clause_tmp.add(Literal(name, False))
                    else:
                        name = literal
                        clause_tmp.add(Literal(name, True))

                clause = Clause((clause_tmp), clause_index, None)
                clause_index += 1
                    

                if clause not in all_clauses:
                    all_clauses.append(clause)
                    sos_index += 1

                print(f"Added {to_add}")

    return 


def select_clauses():
    global sos_index, total_index
    #print("selecting...", sos_index)
    #print(relevant_clauses[sos_index])
    for clause in relevant_clauses[sos_index:]:
        for i, clause_2 in enumerate(relevant_clauses[total_index:], total_index):
            for literal in clause_2.literals:
                for literal_2 in clause.literals:
                    if literal.name == literal_2.name and literal.type != literal_2.type:
                        #print_clauses()
                        total_index = i + 1
                        #print("Found:", literal, literal_2, clause, clause_2)
                        return resolve(clause, clause_2, literal)     
        total_index = 0
        sos_index += 1


def pl_resolution() -> bool:
    global total_index, sos_index

    # remove subesets from input
    while True:
        clauses_before = relevant_clauses.copy()
        for i, clause in enumerate(relevant_clauses.copy()):
            for clause_2 in relevant_clauses.copy()[i+1:]:
                if clause_2.subset(clause):
                    #print("buraz", clause, clause_2)
                    if i < sos_index:
                        sos_index -= 1
                    total_index = 0
                    relevant_clauses.remove(clause)
                    break
        if len(clauses_before) == len(relevant_clauses):
            break

    while True:
        new = set()
        total_index = 0
        resolvents = select_clauses()
        #print("REsolce outer", resolvents)

        # if resolvents is None -> we could not find any matches
        if not resolvents:
            break

        resolvents.factiorization()

        # remove subsets
        for i, clause in enumerate(relevant_clauses.copy()):
            if resolvents.subset(clause):
                if i < sos_index:
                    sos_index -= 1
                total_index = 0
                relevant_clauses.remove(clause)
        
        while resolvents:
            #if not resolvents:
                #return False
            # if the clause that returned is empty -> we got NIL
            if not resolvents.literals:
                global final_parents, final_clause_2
                final_parents = resolvents.parent
                final_clause_2 = resolvents
                return True
            
            # remove subsets 
            for i, clause in enumerate(relevant_clauses.copy()):
                if resolvents.subset(clause):
                    if i < sos_index:
                        sos_index -= 1
                    total_index = 0
                    relevant_clauses.remove(clause)
            
            # otherwise, add the new clause
            if resolvents.tautology():
                flag = False
                for clause in new:
                    if clause.literals == resolvents.literals:
                        flag = True
                if not flag:
                    new.add(resolvents)

            resolvents = select_clauses()
            if resolvents:
                resolvents.factiorization()
                

            #print("Resolve innder", resolvents)

        # if we didnt make anything new
        # TODO do this better
        flag = False
        for el in new:
            if el not in relevant_clauses:
                flag = True
                break

        if flag == False:
            return False

        for el in new:
            relevant_clauses.append(el)
            all_clauses.append(el)

        #print_clauses()

    return False


def find_path(path, clause_i) -> None:
    if clause_i.parent is None:
        return
    # go recursiverly to parents
    for clause in all_clauses.copy():
        if clause.index in clause_i.parent:
            #print(clause)
            if clause not in path:
                path.append(clause)
            find_path(path, clause)


    return


def main():
    args = []
    filename = ""
    mode = ""

    for arg in sys.argv:
        args.append(arg)

    args_iter = iter(args)
    # skip the first argument (program name)
    _ = next(args_iter)
    mode = next(args_iter)
    filename = next(args_iter)

    if mode == "resolution":
        parse_input(filename)
        pl_resolution()
        if final_parents:
            find_path(path, final_clause_2)
            path_s = sorted(path, key=lambda x: x.index)
            for el in path_s:
                print(el)
            print(f"NIL {final_parents}")
            print(f"[CONCLUSION]: {final_clause} is true")
        else:
            print(f"[CONCLUSION]: {final_clause} is unknown")
    elif mode == "cooking":
        cooking_input = next(args_iter)
        parse_input(filename, cooking_input)

    return


if __name__ == "__main__":
    main()