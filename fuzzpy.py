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
    defuzzy_methods = {}
    rules = []
    var = {}
    input_values = []

    def __init__(self, aggregation="TSK", defuzzy=None):
        if aggregation not in self.aggregation_methods:
            raise f'Metodo de agregación no definido: {aggregation}'
        if defuzzy and defuzzy not in self.defuzzy_methods:
            raise f'Metodo de desifusificación no definido: {defuzzy}'
        self.aggregation = self.aggregation_methods[aggregation]
        self.defuzzy = self.defuzzy_methods[defuzzy]
        self.aggregation_methods = {
            'TSK': takagi_sugeno_kang,
            'Tsuka': tsukamoto
            }

    def add_input(self, name, var_type, value):
        self.input_values[name] = {
                'var_type': var_type,
                'm_value': [f(value) for f in self.var[var_type]['m_function']]
            }

    def add_var(self, var_type, states, m_function):
        self.var[var_type] = {"states": states, "m_function": m_function}

    def add_rule(self, pre, post):
        self.rules.append({pre: post})

    def takagi_sugeno_kang(self):
        pass

    def tsukamoto(self):
        pass

if __name__ == '__main__':
    t = Membership.trimf(1, 2, 3, 0, 4)
    print(t.get_interval(), t(2))
