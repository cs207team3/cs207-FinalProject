from chemkin import *
from parser import *

def test_reaction_system():
    # data = read_data('t.xml')
    # print(data)
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'modifiedArrhenius', {'E': 50000.0, 'b': 0.5, 'A': 100000000.0})
    data = {'reactions': {'test_mechanism': [r1]}, 'species': ['H2', 'O2', 'OH', 'HO2', 'H2O']}
    concs = [2., 1., .5, 1., 1.]
    T = 1500
    system = Reaction_system(data['reactions']['test_mechanism'], data['species'], concs, T)
    reaction_rates = system.reaction_rate()
    expected_answer = np.array([-2.81117621e+08, -2.81117621e+08,   
                                5.62235242e+08,  0.00000000e+00, 0.00000000e+00])
    print('1',reaction_rates)
    assert(np.all(np.isclose(reaction_rates, expected_answer)))

#test_reaction_system()