from numpy import exp


class Membership:

    class trimf:
        def __init__(self, a, b, c, l_min, l_max):
            self.a = a
            self.b = b
            self.c = c
            self.l_min = l_min
            self.l_max = l_max

        def get_interval(self):
            return [self.l_min, self.l_max]

        def __call__(self, x):
            if x <= self.l_min or x >= self.l_max:
                raise f'{x} fuera del dominio [{self.l_min}, {self.l_max}]'
            if x <= self.a or x >= self.c:
                return 0
            if self.a <= x <= self.b:
                return (x - self.a)/(self.b - self.a)
            if self.b <= x <= self.c:
                return (self.c - x)/(self.c - self.b)

    class trapmf:
        def __init__(self, a, b, c, d, l_min, l_max):
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.l_min = l_min
            self.l_max = l_max

        def get_interval(self):
            return [self.l_min, self.l_max]

        def __call__(self, x):
            if x <= self.l_min or x >= self.l_max:
                raise f'{x} fuera del dominio [{self.l_min}, {self.l_max}]'
            if x <= self.a or x >= self.d:
                return 0
            if self.a <= x <= self.b:
                return (x - self.a)/(self.b - self.a)
            if self.b <= x <= self.c:
                return 1
            if self.c <= x <= self.d:
                return (self.d - x)/(self.d - self.c)

    class gaussmf:
        def __init__(self, width, center, l_min, l_max):
            self.width = width
            self.center = center
            self.l_min = l_min
            self.l_max = l_max

        def get_interval(self):
            return [self.l_min, self.l_max]

        def __call__(self, x):
            if x <= self.l_min or x >= self.l_max:
                raise f'{x} fuera del dominio [{self.l_min}, {self.l_max}]'
            return exp(-0.5*((x-self.center)/self.width)**2)

    class gbellmf:
        def __init__(self, width, m, center, l_min, l_max):
            self.width = width
            self.m = m
            self.center = center
            self.l_min = l_min
            self.l_max = l_max

        def get_interval(self):
            return [self.l_min, self.l_max]

        def __call__(self, x):
            return 1/(1 + abs((x-self.center)/self.width)**(2*self.m))

    class sigmf:
        def __init__(self, m, center, l_min, l_max):
            self.m = m
            self.center = center
            self.l_min = l_min
            self.l_max = l_max

        def get_interval(self):
            return [self.l_min, self.l_max]

        def __call__(self, x):
            if x <= self.l_min or x >= self.l_max:
                raise f'{x} fuera del dominio [{self.l_min}, {self.l_max}]'
            return 1/(1 + exp(-self.m*(x - self.center)))


class FuzzyModel:
    rules = []
    var = {}
    input_values = {}

    def __init__(self, aggregation="TSK", defuzzy=None):
        self.aggregation_methods = {
            'TSK': self.takagi_sugeno_kang,
            'Tsuka': self.tsukamoto
            }
        self.defuzzy_methods = {None: None}
        if aggregation not in self.aggregation_methods:
            raise f'Metodo de agregación no definido: {aggregation}'
        if defuzzy and defuzzy not in self.defuzzy_methods:
            raise f'Metodo de desifusificación no definido: {defuzzy}'
        self.aggregation = self.aggregation_methods[aggregation]
        self.defuzzy = self.defuzzy_methods[defuzzy]

    def add_input(self, name, var_type, value):
        self.input_values[name] = {
                'var_type': var_type,
                'm_value': {
                    i: self.var[var_type][i](value) for i in self.var[var_type]
                    }
            }

    def add_var(self, var_type, states, m_function):
        self.var[var_type] = {
            states[i]: m_function[i] for i in range(len(states))
            }

    def add_rule(self, pre, post):
        self.rules.append({pre: post})

    def takagi_sugeno_kang(self):
        pass

    def tsukamoto(self):
        pass

    def eval(self, pre):
        result = None
        term = []
        op = None
        negate = False
        pre = pre.split()
        for i in pre:
            if i == 'not':
                negate = True
                continue
            if i == 'and' or i == 'or':
                op = i
                continue
            if i == 'is':
                continue
            term.append(i)
            if len(term) == 2:
                e = self.input_values[term[0]]['m_value'][term[1]]
                term = []
                if negate:
                    e = 1 - e
                    negate = False
                if op is None:
                    result = e
                else:
                    if op == 'and':
                        result = min(result, e)
                    else:
                        result = max(result, e)
        return result

if __name__ == '__main__':
    pass
