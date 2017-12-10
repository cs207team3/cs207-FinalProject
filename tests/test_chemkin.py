import chem3
from chem3.chemkin import *
from chem3.parser import *
import os

test_data_dir = os.path.join(os.path.dirname(chem3.__file__), '../tests/test_data')
test_file = os.path.join(test_data_dir, 't.xml')
db_file = os.path.join(os.path.dirname(chem3.__file__), 'nasa.sqlite')

def test_reaction_system():
    # data = read_data('t.xml')
    # print(data)
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'modifiedArrhenius', {'E': 50000.0, 'b': 0.5, 'A': 100000000.0})
    data = {'reactions': {'test_mechanism': [r1]}, 'species': ['H2', 'O2', 'OH', 'HO2', 'H2O']}
    concs = [2., 1., .5, 1., 1.]
    T = 1500
    system = ReactionSystem(data['reactions']['test_mechanism'], data['species'])
    reaction_rates = system.reaction_rate(concs, T)
    expected_answer = np.array([-2.81117621e+08, -2.81117621e+08,
                                5.62235242e+08,  0.00000000e+00, 0.00000000e+00])
    assert (np.all(np.isclose(reaction_rates, expected_answer)))

def test_reaction_init_():
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'modifiedArrhenius', {'E': 50000.0, 'b': 0.5, 'A': 100000000.0})
    assert (r1.reactants == {'O2': 1.0, 'H2': 2.0})
    assert (r1.products == {'OH': 2.0, 'H2': 1.0})
    assert (r1.reversible == False)
    assert (r1.reac_type == 'Elementary')
    assert (r1.reac_id == 'reaction01')
    assert (r1.coef_type == 'modifiedArrhenius')
    assert (r1.coef == {'E': 50000.0, 'b': 0.5, 'A': 100000000.0})

def test_set_reac_coefs_1():
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'modifiedArrhenius',\
                {'E': 50000.0, 'b': 0.5, 'A': 100000000.0})
    r1.set_reac_coefs(500)
    assert (np.isclose(r1.k, 13360.7963743))

def test_set_reac_coefs_2():
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'Constant',\
                {'k': 5000})
    r1.set_reac_coefs(500)
    assert (r1.k == 5000)

def test_set_reac_coefs_3():
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'Arrhenius',\
                {'E': 50000.0, 'A': 100000000.0})
    r1.set_reac_coefs(500)
    assert (np.isclose(r1.k, 597.512978529))

def test_set_reac_coefs_4():
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'Constant',\
                {'k': -5000})
    try:
        r1.set_reac_coefs(500)
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_reac_coefs_5():
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'modifiedArrhenius',\
                {'E': 50000.0, 'b': -0.5, 'A': 100000000.0})
    try:
        r1.set_reac_coefs(500)
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_reac_coefs_6():
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'Arrhenius',\
                {'E': 50000.0, 'A': -100000000.0})
    try:
        r1.set_reac_coefs(500)
    except ValueError as err:
        assert (type(err) == ValueError)

def test_eq_():
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'modifiedArrhenius',\
                {'E': 50000.0, 'b': 0.5, 'A': 100000000.0})
    r2 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction02', 'modifiedArrhenius',\
                {'E': 50000.0, 'b': 0.5, 'A': 100000000.0})
    assert (r1 == r2)

# --------------------------------------------------------------------------------------------------------------------------------

r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'modifiedArrhenius',\
                {'E': 50000.0, 'b': 0.5, 'A': 100000000.0})
r2 = Reaction({'OH': 1.0, 'HO2': 1.0}, {'H2O': 1.0, 'O2': 1.0}, False, 'Elementary', 'reaction02', 'Constant', \
                {'k': 10000.0})
data = {'reactions': {'test_mechanism': [r1, r2]}, 'species': ['H2', 'O2', 'OH', 'HO2', 'H2O']}
concs = [2., 1., .5, 1., 1.]
T = 1500
system = ReactionSystem(data['reactions']['test_mechanism'], data['species'])

# --------------------------------------------------------------------------------------------------------------------------------

def test_init_matrices():
    expected = np.array([[2., 0.], [1., 0.], [0., 1.], [0., 1.], [0., 0.]])
    assert (np.all(np.isclose(system.nu_react, expected)))
    expected = np.array([[1., 0.],[ 0., 1.], [ 2.,  0.], [0., 0.], [0., 1.]])
    assert (np.all(np.isclose(system.nu_prod, expected)))

def test_reaction_rate():
    expected = np.array([ -2.81117621e+08, -2.81112621e+08, 5.62230242e+08, -5.00000000e+03, 5.00000000e+03])
    assert (np.all(np.isclose(system.reaction_rate(concs, T), expected)))

def test_full_process():
    test_data_dir = os.path.join(os.path.dirname(chem3.__file__), '../tests/test_data')
    test_file = os.path.join(test_data_dir, 't.xml')

    data = read_data(test_file, db_file)
    concs = [2., 1., .5, 1., 1.]
    T = 1500
    system = ReactionSystem(data['reactions']['test_mechanism'], data['species'])
    assert(len(system) == 3)
    expected = np.array([-2.81117621e+08, -2.85597559e+08, 5.66715180e+08, 4.47993847e+06, -4.47993847e+06])
    assert (np.all(np.isclose(system.reaction_rate(concs, T), expected)))

def test_full_process_rev():
    test_data_dir = os.path.join(os.path.dirname(chem3.__file__), '../tests/test_data')
    test_file = os.path.join(test_data_dir, 'rxns_reversible.xml')

    data = read_data(test_file, db_file)
    concs = [2., 1., .5, 1., 1., .5, .5, .5]
    T = 900
    system = ReactionSystem(data['reactions']['hydrogen_air_mechanism'], data['species'], data['low'], data['high'],\
                data['T_cutoff'], data['T_range'])
    expected = np.array([7.58800198e+15, -7.55393354e+15, -7.87061311e+15, 3.01454055e+13,\
                             1.88251887e+14, 7.73922038e+15, -8.79625439e+13, -3.31104554e+13])
    assert(np.all(np.isclose(system.reaction_rate(concs, T), expected)))

def test_full_process_rev_1():
    test_data_dir = os.path.join(os.path.dirname(chem3.__file__), '../tests/test_data')
    test_file = os.path.join(test_data_dir, 'rxns_reversible.xml')

    data = read_data(test_file, db_file)
    concs = [2., 1., .5, 1., 1., .5, .5, .5]
    T = 100
    system = ReactionSystem(data['reactions']['hydrogen_air_mechanism'], data['species'], data['low'], data['high'],\
                 data['T_cutoff'], data['T_range'])

    try:
        system.reaction_rate(concs, T)
    except ValueError as err:
        assert (type(err) == ValueError)


def test_system_read_from_file_name():
    concs = [2., 1., .5, 1., 1.]
    T = 1500
    system = ReactionSystem(filename=test_file)
    assert(len(system) == 3)
    expected = np.array([-2.81117621e+08, -2.85597559e+08, 5.66715180e+08, 4.47993847e+06, -4.47993847e+06])
    assert (np.all(np.isclose(system.reaction_rate(concs, T), expected)))
    
