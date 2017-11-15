"""
This is a module to parse .xml files containing checmical kinetics reactions
for use with the chemkin.py module also found in this library.

An example of a properly formated reactions .xml file can be found in the
main directory of this library, titled 'rxns.xml'
"""

import xml.etree.ElementTree as ET
import sqlite3
import numpy as np
from chem3.chemkin import *

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


def get_coeffs(db_name, species):
    """reads the database and gets coefficients 

    INPUTS:
    =======
    db_name:    str
                Database name storing coefficients
    species:    array of str
                A list of species to ensure coefficient 
                and matrix will use the same order of species array

    RETURNS:
    =======
    low:        numpy array
                Coefficient matrix for low temperature reactions
    high:       numpy array
                Coefficient matrix for high temperature reactions

    EXAMPLES:
    ========
    >>> high = get_coeffs('nasa.sqlite', ['O', 'O2', 'H', 'H2', 'OH', 'H2O', 'HO2', 'H2O2'])[1]
    >>> high[2][2]
    -1.99591964e-15
    """

    db = sqlite3.connect(db_name)
    cursor = db.cursor()

    def get_species_coeffs(species_name, temp_range):
        query = 'SELECT * FROM ' + temp_range.upper() + ' WHERE species_name = "' + species_name + '"'
        q = cursor.execute(query).fetchall()
        if len(q) == 0: 
            print('Warning, did not find rows given species_name and temp_range. Please double check.')
            return []
        return q[0][2], list(q[0][3:])  # coeffs, high

    low = np.zeros((len(species), 7))
    high = np.zeros((len(species), 7))
    temps = np.zeros(len(species))
    for i, s in enumerate(species):
        temps[i], low[i]  = get_species_coeffs(s, 'low')
        _, high[i] = get_species_coeffs(s, 'high')
    db.close()
    return low, high, temps


def read_data(filename, db_name):
    """reads data from .xml reaction file

    INPUTS:
    =======
    filename:   str
                File name of .xml file to parse
    db_name:    str
                Database name storing coefficients

    RETURNS:
    =======
    data: dictonary of reactions and species for each reaction in the file
    (keys = ['reactions', 'species', 'low', 'high', 'T_cutoff'])

    EXAMPLES:
    ========
    >>> data = read_data('t.xml', 'nasa.sqlite')
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

        # get coefficients
        data['low'], data['high'], data['T_cutoff'] = get_coeffs(db_name, data['species'])
        
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
        return {}
    return data



