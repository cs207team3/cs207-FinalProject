[![Build Status](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/cs207team3/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/cs207team3/cs207-FinalProject?branch=master)

## cs207-FinalProject: A Chemical Kinetics Library
### Final Project repository for CS207 Team 3
##### Team Members: Jiacheng Shi, Weihang Zhang, & Andrew Lund

---

### User's Guide

Describe what problem the code is solving. You may borrow the Latex expressions from my lecture notes. Discuss in broad
strokes what the purpose of the code is along with any features. Do not describe the details of the code yet. **(delete before releasing)**

**Introduction:**

The purpose of our library is to return the reaction rate of a system of N species undergoing M reactions. The reactions should be irreversible and elementary of the form:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/equations/reaction_form.png "Reaction Form")

In the future we intend on implementing features to handle both reversible and non-elementary reactions.

-----

The progress rate for each reaction is given by:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/equations/progress_rate.png "Progress Rate")

The reaction rate of each specie i can be written as:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/equations/reaction_rate.png "Reaction Rate")

------

**Installation:**

All the code related to this library can be found in this repository, specifically in the files **parser.py** and **chemkin.py**.

In order to run the test suite accompanying these files, do the following:

`pytest --doctest-modules --cov-report term-missing --cov chemkin`

----

We are not releasing this code as a package yet, but when we do that this section will include instructions how how to install the package.

----

### Basic Usage:
After checking out this repository:
1. import relative class and functions from parser.py and chemkin.py.

  ```
  from parser import *
  from chemkin import *
  ```
  
2. User can obtain reaction data by parsing an existing xml file using `read_data()` function or manually create reactions using the constructor in `Reaction()` class.

3. To calculate the reaction rate of a system, a user also needs to specify the current concentration of each species and the temperature under which the reaction rate is calculated.

### Code Example:
```
from chemkin import *
from parser import *
# parse data from xml file
data = read_data('t.xml')
# specify concentration list and current temperature
concs = [2., 1., .5, 1., 1.]
T = 1500
# create a system of the reactions
system = Reaction_system(data['reactions']['test_mechanism'], data['species'], concs, T)
# calculate reaction rates
reaction_rates = system.reaction_rate()
```

** TODO?: provide a more specific example (maybe we can use the example from L11 exercise) **

Provide a few examples on using your software in some common situations. You may want to show how the code works with a small set of reactions.

Note: The order the user inputs reaction concentrations will be matched to the reactants pulled from the '<phase>' tag
