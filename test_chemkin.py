from chemkin import *
from parser import *

def test_reaction_system():
    # data = read_data('t.xml')
    # print(data)
    r1 = Reaction({'O2': 1.0, 'H2': 2.0}, {'OH': 2.0, 'H2': 1.0}, False, 'Elementary', 'reaction01', 'modifiedArrhenius', {'E': 50000.0, 'b': 0.5, 'A': 100000000.0})
    data = {'reactions': {'test_mechanism': [r1]}, 'species': ['H2', 'O2', 'OH', 'HO2', 'H2O']}
    concs = [2., 1., .5, 1., 1.]
    T = 1500
    system = ReactionSystem(data['reactions']['test_mechanism'], data['species'], concs, T)
    reaction_rates = system.reaction_rate()
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
system = ReactionSystem(data['reactions']['test_mechanism'], data['species'], concs, T)

# --------------------------------------------------------------------------------------------------------------------------------

def test_reaction_system_init_1():
    assert (system.concs == concs)

def test_reaction_system_init_2():
    concs = [2., 1., .5, 1., -1.]
    try:
        system = ReactionSystem(data['reactions']['test_mechanism'], data['species'], concs, T)
    except ValueError as err:
        assert (type(err) == ValueError)

def test_init_matrices():
    expected = np.array([[2., 0.], [1., 0.], [0., 1.], [0., 1.], [0., 0.]])
    assert (np.all(np.isclose(system.nu_react, expected)))
    expected = np.array([[1., 0.],[ 0., 1.], [ 2.,  0.], [0., 0.], [0., 1.]])
    assert (np.all(np.isclose(system.nu_prod, expected)))

def test_progress_rate():
    expected = np.array([281117620.76487046, 5000.0])
    assert (np.all(np.isclose(system.progress_rate(), expected)))

def test_reaction_rate():
    expected = np.array([ -2.81117621e+08, -2.81112621e+08, 5.62230242e+08, -5.00000000e+03, 5.00000000e+03])
    assert (np.all(np.isclose(system.reaction_rate(), expected)))

def test_full_process():
    data = read_data('t.xml')
    concs = [2., 1., .5, 1., 1.]
    T = 1500
    system = ReactionSystem(data['reactions']['test_mechanism'], data['species'], concs, T)
    assert(len(system) == 3)
    expected = np.array([-2.81117621e+08, -2.85597559e+08, 5.66715180e+08, 4.47993847e+06, -4.47993847e+06])
    assert (np.all(np.isclose(system.reaction_rate(), expected)))

def test_system_read_from_file_name():
    concs = [2., 1., .5, 1., 1.]
    T = 1500
    system = ReactionSystem(concs=concs, T=T, filename='t.xml')
    assert(len(system) == 3)
    expected = np.array([-2.81117621e+08, -2.85597559e+08, 5.66715180e+08, 4.47993847e+06, -4.47993847e+06])
    assert (np.all(np.isclose(system.reaction_rate(), expected)))

test_reaction_system_init_2()
