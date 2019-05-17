from numpy import exp, linspace


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
            if x < self.l_min or x > self.l_max:
                raise 'argumento fuera del dominio'
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
            if x < self.l_min or x > self.l_max:
                raise 'argumento fuera del dominio'
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
            if x < self.l_min or x > self.l_max:
                raise 'argumento fuera del dominio'
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
            if x < self.l_min or x > self.l_max:
                raise 'argumento fuera del dominio'
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
            if x < self.l_min or x > self.l_max:
                raise 'argumento fuera del dominio'
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
        self.defuzzy_methods = {
            None: None,
            'centroid': self.centroid,
            'bis': self.bisectriz,
            'MoM': self.MoM,
            'LoM': self.LoM,
            'GoM': self.GoM
            }
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
        self.rules.append([pre, post])

    def takagi_sugeno_kang(self):
        w = 0
        wf = 0
        for i in self.rules:
            e = tuple(self.eval(i[0]).values())
            wf += i[1](*e)
            w += min(e)
        return wf/w

    def tsukamoto(self):
        w = 0
        wz = 0
        for i in self.rules:
            f = i[1].split(" is ")
            f = self.var[f[0]][f[1]]
            self.get_interval = f.get_interval()
            e = min(tuple(self.eval(i[0]).values()))
            w += e
            wz += e*self.defuzzy(lambda x: min(e, f(x)))
        return wz/w

    def eval(self, pre):
        result = {}
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
                v = term[0]
                term = []
                if negate:
                    e = 1 - e
                    negate = False
                if op is None or v not in result:
                    result[v] = e
                else:
                    if op == 'and':
                        result[v] = min(result[v], e)
                    else:
                        result[v] = max(result[v], e)
        return result

    def solve(self):
        return self.aggregation()

    def centroid(self, f):
        interval = self.get_interval
        u = 0
        d = 0
        for i in linspace(interval[0], interval[1], 10**4):
            u += i*f(i)
            d += f(i)
        if u == 0:
            return 0
        return u/d

    def MoM(self, f):
        interval = self.get_maximun(f)
        return interval[1]
    
    def LoM(self, f):
        interval = self.get_maximun(f)
        return interval[0]

    def GoM(self, f):
        interval = self.get_maximun(f)
        return (interval[1] + interval[0])/2

    def get_maximun(self, f):
        from numpy import fabs
        interval = self.get_interval
        minimum, maximum = 10**9, -10**9
        value = -10**9
        s = linspace(interval[0], interval[1], 10**4)
        for i in s:
            if f(i) > value:
                minimum = maximum = i 
                value = f(i)
            if abs(f(i) - value) < 10**-9:
                minimum = min(minimum, i)
                maximum = max(maximum, i)
        return minimum, maximum

    def bisectriz(self, f):
        from math import fabs
        interval = self.get_interval
        l = interval[0]
        r = interval[1]
        m = 0
        for _ in range(100):
            m = (l + r)/2
            a, b = self.area(f, [interval[0], m]), self.area(f, [m, interval[1]])
            if fabs(a - b) < 10**-6:
                return m
            if a > b:
                r = m
            else:
                l = m
        return m

    def area(self, f, interval):
        a = 0
        s = linspace(interval[0], interval[1], 100)
        for i in s:
            a += f(i)
        return a

if __name__ == '__main__':
    pass
