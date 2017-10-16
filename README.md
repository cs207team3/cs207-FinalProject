[![Build Status](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/cs207team3/cs207-FinalProject/badge.svg?branch=master&maxAge=0)](https://coveralls.io/github/cs207team3/cs207-FinalProject?branch=master&maxAge=0)

## cs207-FinalProject: A Chemical Kinetics Library
### Final Project repository for CS207 Team 3
##### Team Members: Jiacheng Shi, Weihang Zhang, & Andrew Lund

---

### User's Guide

...Please see the chart below for equation symbols and their meaning...

**Introduction:**

The purpose of our library is to return the reaction rate of a system of N species undergoing M reactions. The reactions should be irreversible and elementary of the form:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/reaction_form.png "Reaction Form")

In the future we intend on implementing features to handle both reversible and non-elementary reactions.

-----

The progress rate for each reaction is given by:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/progress_rate.png "Progress Rate")

The reaction rate of each specie i can be written as:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/reaction_rate.png "Reaction Rate")
----
![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/variables.png "Variables")

------

### Installation:

All the code related to this library can be found in this repository, specifically in the files **parser.py** and **chemkin.py**.

In order to run the test suite accompanying these files, do the following:

`pytest --doctest-modules --cov-report term-missing --cov chemkin`

----

We are not releasing this code as a package yet, but when we do that this section will include instructions how how to install the package.

----

### Input Format
The data of the relative reactions can be stored in an .xml file. 

The user needs to have **\<phase\>** tab to specify a list of species involved in the reaction. The order should also be consistent with the input for concentration when a user calculates the reaction rates.
  
The second tab of the .xml file needs to store reaction information wrapped by **\<reactionData\>**. Our parser supports multiple reactionData tabs when parsing the .xml file. 
  
For more details of correctly formatting the input file, please refer to our [sample input](https://github.com/cs207team3/cs207-FinalProject/blob/master/rxns.xml).

If the .xml file is not properly formatted, the parser.py will print a warning and return an empty data to the user.

----

### Basic Usage:
After checking out this repository:
1. Import relative classes and functions from parser.py and chemkin.py.

2. User can create the reaction system directly from an .xml data file (see 3.1), obtain reaction data by parsing a properly formatted .xml file using `read_data()` function by user (see 3.2), or manually create reactions using the constructor in the `Reaction()` class.

#### Code Examples:
3.1 To create a reaction system directly from .xml file, use the following code.
```
>>> from chemkin import *
>>> from parser import *
>>> concs = [2., 1., .5, 1., 1.]
>>> T = 1500
>>> system = ReactionSystem(concs=concs, T=T, filename='t.xml')
>>> # calculate reaction rates
>>> reaction_rates = system.reaction_rate()
[ -2.81117621e+08  -2.85597559e+08   5.66715180e+08   4.47993847e+06  -4.47993847e+06]
```

3.2 To calculate the reaction rate of a system, you must specify the current concentration of each species and the temperature under which the reaction takes place. The order of the concentrations will be matched to the order of the reactants list obtained from the .xml file.

```
>>> from chemkin import *
>>> from parser import *
>>> # parse data from xml file
>>> data = read_data('t.xml')
>>> # specify concentration list and current temperature
>>> concs = [2., 1., .5, 1., 1.]
>>> T = 1500
>>> # create a system of the reactions
>>> system = ReactionSystem(data['reactions']['test_mechanism'], data['species'], concs, T)
>>> # calculate reaction rates
>>> reaction_rates = system.reaction_rate()
[ -2.81117621e+08  -2.85597559e+08   5.66715180e+08   4.47993847e+06  -4.47993847e+06]
```

Note: The order the user inputs reaction concentrations will be matched to the reactants pulled from the "phase" tag in the .xml file.
