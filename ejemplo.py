from fuzzpy import *

m = FuzzyModel('Tsuka', 'MoM')
m.add_var(
    'tamaño',
    ['larga', 'normal', 'corta'],
    [
        Membership.trapmf(10, 15, 30, 30, 0, 30),
        Membership.trapmf(8, 9, 11, 12, 0, 30),
        Membership.trapmf(0, 0, 7, 10, 0, 30)
        ]
    )
m.add_var(
    'velocidad',
    ['lenta', 'normal', 'rapida'],
    [
        Membership.trapmf(0, 0, 3, 5, 0, 5),
        Membership.trimf(1, 2, 3, 0, 5),
        Membership.trapmf(2, 3, 5, 5, 0, 5)
    ]
)
m.add_var(
    'bronca',
    ['alta', 'media', 'baja'],
    [
        Membership.trapmf(50, 75, 100, 100, 0, 100),
        Membership.trimf(40, 50, 60, 0, 100),
        Membership.trapmf(0, 0, 50, 25, 0, 100)
    ]
)
m.add_input('cola', 'tamaño', 19)
m.add_input('tenderos', 'velocidad', 2)
m.add_rule('tenderos is lenta', 'bronca is alta')
m.add_rule('cola is larga', 'bronca is alta')
m.add_rule('cola is normal and tenderos is normal', 'bronca is media')
print(f'La probabilidad de bronca es {m.solve()}%')
