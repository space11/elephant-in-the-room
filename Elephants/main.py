import fileinput


def define_file() -> list:
    """Extracts lines from input file"""
    # extract lines from input file and contain strings in list without "\n" and "\r" signs.
    file = [line.replace('\n', '').replace('\r', '') for line in fileinput.input()]
    return file


class Permutation:

    def __init__(self, file: list):
        """ Initializes Permutation Object with path to .in file """
        self.file = file
        self.n = int(self.file[0])  # number of elephants
        self.mass_list = [int(mass) for mass in self.file[1].split(' ')]  # list of elephants masses
        self.actual = [int(pos) - 1 for pos in self.file[2].split(' ')]  # actual arrangement
        self.target = [int(pos) - 1 for pos in self.file[3].split(' ')]  # target arrangement
        self.perm = self.create_permutation()  # define permutation
        self.cycles = self.define_cycles()  # creates permutation cycles
        self.parameters, self.minimum = self.define_cycles_parameters()  # list of cycles parameters and min weight
        self.result = self.calculate_result()  # lowest cost of rearrangement

    def create_permutation(self) -> list:
        """Returns list of permutation values"""
        perm = [0 for _ in range(self.n)]
        for i in range(self.n):
            perm[self.target[i]] = self.actual[i]
        return perm

    def define_cycles(self) -> list:
        """Defines permutation cycles"""
        odw = [False for _ in range(self.n)]  # array of booleans to define end of cycle
        cycles = [[] for _ in range(self.n)]  # list of cycles
        c = 0  # number of permutation cycles
        for i in range(self.n):
            if not odw[i]:
                c += 1
                x = i
                while not odw[x]:
                    odw[x] = True
                    cycles[c - 1].append(x)
                    x = self.perm[x]
        cycles = [value for value in cycles if len(value) > 1]  # deletes cycles with zero or one elephant
        return cycles

    def define_cycles_parameters(self) -> tuple:
        """Returns List of dictionaries with parameters of permutation cycles"""
        minimum = min(self.mass_list)
        parameters = []
        for i in range(len(self.cycles)):
            sumCi = 0
            minCi = float('inf')
            for e in self.cycles[i]:
                sumCi += self.mass_list[e]
                minCi = min(minCi, self.mass_list[e])
            parametersCi = {'sum(Ci)': sumCi,
                            'min(Ci)': minCi,
                            '|Ci|': len(self.cycles[i])}
            parameters.append(parametersCi)
        return parameters, minimum

    def calculate_result(self) -> int:
        """Returns the lowest value of permutation cost"""
        result = 0
        for i in range(len(self.cycles)):
            method_1_Ci = self.parameters[i]['sum(Ci)'] + (self.parameters[i]['|Ci|'] - 2) * self.parameters[i]['min(Ci)']
            method_2_Ci = self.parameters[i]['sum(Ci)'] + self.parameters[i]['min(Ci)'] + (self.parameters[i]['|Ci|'] + 1) * self.minimum
            result += min(method_1_Ci, method_2_Ci)
        return result


if __name__ == "__main__":

    solver = Permutation(define_file())
    print(solver.result)

