from numpy import exp


class Membership:

    def trimf(a, b, c):
        def _trimf(x):
            if x <= a or x >= c:
                return 0
            if a <= x <= b:
                return (x - a)/(b - a)
            if b <= x <= c:
                return (c - x)/(c - b)
        return _trimf

    def trapmf(a, b, c, d):
        def _trapmf(x):
            if x <= a or x >= d:
                return 0
            if a <= x <= b:
                return (x - a)/(b - a)
            if b <= x <= c:
                return 1
            if c <= x <= d:
                return (d - x)/(d - c)
        return _trapmf

    def gaussmf(width, center):
        def _gbellmf(x):
            return exp(-0.5*((x-center)/width)**2)
        return _gbellmf

    def gbellmf(width, m, center):
        def _gbellmf(x):
            return 1/(1 + abs((x-center)/width)**(2*m))
        return _gbellmf

    def sigmf(m, center):
        def _sigmf(x):
            return 1/(1 + exp(-m*(x - center)))
        return _sigmf


class FuzzyModel:
    aggregation_methods = {'TSK': FuzzyModel.takagi_sugeno_kang, 'Tsuka'}
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
    pass
