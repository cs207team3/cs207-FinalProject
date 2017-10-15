"""
This is a module to parse .xml files containing checmical kinetics reactions
for use with the chemkin.py module also found in this library.

An example of a properly formated reactions .xml file can be found in the
main directory of this library, titled 'rxns.xml'
"""

import xml.etree.ElementTree as ET
from chemkin import *

def string_to_dict(s):
    """returns dictionary of species in reaction

    INPUTS:
    =======
    s:  string

    RETURNS:
    =======
    ret: dictionary of species

    EXAMPLES:
    ========
    >>> string_to_dict('H:1 O2:1')['H']
    1.0
    """
    ret = {}
    for kv in s.split():
        kv = kv.split(':')
        ret[kv[0]] = float(kv[1])
    return ret

def read_data(filename):
    """reads data from .xml reaction file

    INPUTS:
    =======
    .xml file

    RETURNS:
    =======
    data: reaction information for each reaction in the file

    EXAMPLES:
    ========
    # >>>read_data('t.xml')
    # {'H2': 2.0, 'O2': 1.0} {'OH': 2.0, 'H2': 1.0} False Elementary reaction01 modifiedArrhenius {'A': 100000000.0, 'b': 0.5, 'E': 50000.0}
    # {'OH': 1.0, 'HO2': 1.0} {'H2O': 1.0, 'O2': 1.0} False Elementary reaction02 Constant {'k': 10000.0}
    # {'H2O': 1.0, 'O2': 1.0} {'HO2': 1.0, 'OH': 1.0} False Elementary reaction03 Arrhenius {'A': 10000000.0, 'E': 10000.0}
    """
    tree = ET.parse(filename)
    rxns = tree.getroot()

    data = {}
    # get species list
    phase = rxns.find('phase')
    if phase: # check if tag 'phase' is found

        ##### DO WE NEED TO CHECK ??? #####

        data['species'] = phase.find('speciesArray').text.split()

    # Reaction(reactants, products, reversible, reac_type, reac_id, coef_type):
    data['reactions'] = {}
    for reaction_data in rxns.findall('reactionData'):
        reaction_id = reaction_data.get('id')
        reactions = []
        for reaction in reaction_data.findall('reaction'):
            reactants = string_to_dict(reaction.find('reactants').text)
            products = string_to_dict(reaction.find('products').text)
            reversible = reaction.get('reversible') != 'no'
            reac_type = reaction.get('type')
            reac_id = reaction.get('id')
            coefs_block = reaction.find('rateCoeff')
            coef = {}
            for arr in coefs_block:
                coef_type = arr.tag
                params_block = coefs_block.find(coef_type)
                for param in params_block:
                    key = param.tag
                    coef[key] = float(params_block.find(key).text)
            print(reactants, products,
                                     reversible, reac_type,
                                     reac_id, coef_type, coef)
            reactions.append(Reaction(reactants, products,
                                     reversible, reac_type,
                                     reac_id, coef_type, coef))
            data['reactions'][reaction_id] = reactions
    return data


"""
Example code below
"""
data = read_data('t.xml')
print(data)
print(data['reactions']['test_mechanism'][0])
concs = [2., 1., .5, 1., 1.]
T = 1500
system = Reaction_system(data['reactions']['test_mechanism'], data['species'], concs, T)
print(system.reaction_rate())
