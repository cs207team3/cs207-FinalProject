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
    filename:   str
                File name of .xml file to parse

    RETURNS:
    =======
    data: reaction information for each reaction in the file

    EXAMPLES:
    ========
    >>> data = read_data('t.xml')
    >>> data['species']
    ['H2', 'O2', 'OH', 'HO2', 'H2O']
    """
    tree = ET.parse(filename)
    rxns = tree.getroot()

    data = {}

    try:
        # get species list
        phase = rxns.find('phase')
        data['species'] = phase.find('speciesArray').text.split()

        # get reaction info
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
                reactions.append(Reaction(reactants, products,
                                         reversible, reac_type,
                                         reac_id, coef_type, coef))
                data['reactions'][reaction_id] = reactions
    except AttributeError as ex:
        print(ex)
        print('Warning: please check your xml format, ' + 
              'returns empty data because format doesn\'t match')
    return data
