from chemkin import *
from parser import *

def test_reaction_system():
    data = read_data('t.xml')
    concs = [2., 1., .5, 1., 1.]
    T = 1500
    system = Reaction_system(data['reactions']['test_mechanism'], data['species'], concs, T)
    reaction_rates = system.reaction_rate()
    expected_answer = np.array([-2.81117621e+08, -2.85597559e+08, 
        5.66715180e+08, 4.47993847e+06, -4.47993847e+06])
    assert(np.all(np.isclose(reaction_rates, expected_answer)))
    