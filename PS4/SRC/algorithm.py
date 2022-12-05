
EMPTY_CLAUSE = '{}'
NOT_OPERATOR = '-'
OR_OPERATOR = ' OR '

class algorithms:
    def __init__(self):
        self.is_solved = False
        self.alpha = []
        self.KB = []
        self.new_clauses = [] # chua menh de da hop giai

    # Ham doc file input
    def read_file(self, file_name: str):
        with open(file_name, 'r') as f:
            # Dong dau la alpha
            self.alpha = f.readline()[:-1].split(OR_OPERATOR)
            # Dong thu hai la so luong menh de theo gia thuyet
            num_clause = int(f.readline())
            # Cac dong tiep theo la cac menh de theo gia thuyet
            for i in range(num_clause):
                self.KB.append(f.readline()[0:].strip())
        
        self.KB = self.standard_clauses(self.KB)

    # Ham chuyen menh de thanh list cac literals va sap xep theo thu tu alphabet 
    def standard_clauses(self, clauses: list):
        std_clauses = []
        for c in clauses:
            literals = c.split(OR_OPERATOR)
            # sort theo alphabet (bo qua dau -)
            literals.sort(key=lambda x: x[1:] if x[0] == NOT_OPERATOR else x)
            # loai bo cac literal trung nhau
            literals = list(dict.fromkeys(literals))
            if literals not in std_clauses:
                std_clauses.append(literals)
        return std_clauses
    
    # Ham kiem tra doi ngau
    def is_inverse(self, literal1: str, literal2: str):
        return literal1 == self.negate_literal(literal2)

    # Ham kiem tra menh de co luon la chan tri True hay khong
    def is_always_true(self, clause: list):
        for literal in clause:
            if self.negate_literal(literal) in clause:
                return True
        return False

    # Ham dinh dang output theo CNF
    def format_cnf(self, clauses: list):
        if len(clauses) == 0:
            return EMPTY_CLAUSE
        else:
            return OR_OPERATOR.join(clauses)

    # Ham hop giai 2 menh de
    def resolve(self, clause1: list, clause2: list):
        resolvents = []
        for literal1 in clause1:
            for literal2 in clause2:
                if self.is_inverse(literal1, literal2):
                    resolvent = clause1 + clause2
                    resolvent.remove(literal1)
                    resolvent.remove(literal2)
                    resolvent.sort(key=lambda x: x[1:] if x[0] == NOT_OPERATOR else x)
                    resolvent = list(dict.fromkeys(resolvent))
                    if resolvent not in resolvents:
                        resolvents.append(resolvent)
        return resolvents

    # Ham chinh xu ly hop giai KB V -(alpha)
    def pl_resolution(self):
        clauses_list = self.KB
        for literal in self.alpha:
            if self.negate_literal(literal) not in self.KB:
                clauses_list.append([self.negate_literal(literal)])
        
        idx = 0 # Dung de toi uu vong lap
        while True:
            self.new_clauses.append([])

            for i in range(len(clauses_list)):
                for j in range(i + 1 if i >= idx else idx , len(clauses_list)):
                    resolvents = self.resolve(clauses_list[i], clauses_list[j])
                    
                    # Tồn tại 2 mệnh đề đối ngẫu nhau trong clauses_list
                    if [] in resolvents:
                        self.is_solved = True

                    for resolvent in resolvents:
                        if self.is_always_true(resolvent): # menh de co chan tri True can loai bo
                            continue
                        if resolvent not in clauses_list and resolvent not in self.new_clauses[-1]:
                            self.new_clauses[-1].append(resolvent)
                            

            if len(self.new_clauses[-1]) == 0:
                return self.is_solved
            
            # Duyet qua tat ca menh de moi xet KB entails alpha hay khong
            if self.is_solved:
                return self.is_solved

            clauses_list += self.new_clauses[-1]
            # Loop ke tiep chi can kiem tra voi cac menh de moi them vao
            idx = len(clauses_list) - len(self.new_clauses[-1])


    # Ham lay doi ngau cua literal    
    def negate_literal(self, literal: str):
        if literal[0] == NOT_OPERATOR:
            return literal[1:]
        else:
            return NOT_OPERATOR + literal

    # Ham ghi ket qua ra file output
    def write_file(self, file_name: str):
        f = open(file_name, 'w')
        for new_clauses in self.new_clauses:
            f.write(str(len(new_clauses)) + '\n')
            for clause in new_clauses:
                f.write(self.format_cnf(clause) + '\n')
        if self.is_solved:
            f.write('YES')
        else:
            f.write('NO')
        f.close()

    # Cac menh de duoc hop giai
    # def print_resolved(self, file_name:str):
    #     f = open(file_name, 'w')
    #     for i in range(len(self.is_resolved)):
    #         f.write('Loop ' + str(i + 1) + '\n')
    #         for j in range(0, len(self.is_resolved[i]), 2):
    #             f.write(self.format_cnf(self.is_resolved[i][j]) + ' with ' + self.format_cnf(self.is_resolved[i][j + 1]) + '\n')
    #         f.write('\n')
    #     f.close()
            