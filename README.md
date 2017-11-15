[![Build Status](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/cs207team3/cs207-FinalProject/badge.svg?branch=master&maxAge=0)](https://coveralls.io/github/cs207team3/cs207-FinalProject?branch=master&maxAge=0)

## cs207-FinalProject: A Chemical Kinetics Library
### Final Project repository for CS207 Team 3
##### Team Members: Jiacheng Shi, Weihang Zhang, & Andrew Lund

---

### User's Guide:
### FIX IMAGES

...Please see the chart below for equation symbols and their meaning...

**Introduction:**

The purpose of our library is to return the reaction rate of a system of N species undergoing M reactions. The reactions can be reversible or irreversible, and should be elementary of the form:

Irreversible:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/irreversible_reaction_form.png "Irreversible Reaction Form")

Reversible:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/reversible_reaction_form.png "Reversible Reaction Form")

-----

The progress rate for each reaction is given by:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/progress_rate.png "Progress Rate")

The reaction rate of each specie i in an irreversible reaction can be written as:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/reaction_rate.png "Reaction Rate")

The reaction rate for each specie in an elementary reversible reaction can be written as:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/backward_reaction_rate.png "Backward_Reaction Rate")

where:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/equilibrium_coeff.png "Equilibrium Coefficient")

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/equilibrium_coeff2.png "Equilibrium Coefficient2")

P0 is the pressure of the reactor (we will use 100,000 Pa in this library). Using the NASA polynomials and relationships between the specific heat, enthalpy and entropy, we use the following equations to compute the backwards reaction rate coefficient for elementary reversible reactions:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/NASA_polynomials.png "NASA Polynomials")

This library will read in the relevant NASA polynomial coefficients from a database and store them in a data structure based on which species the user specifies in the .xml input file. See more below in the "Input Format" section.

----
![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/variables.png "Variables")

------

### Installation:

All the code related to this library can be found in this repository. This includes the NASA polynomials as an SQL database in order to calculate the backwards reaction rate coefficients for reversible elementary reactions.

To install this library and run the test suite, download or clone this repository and do the following:

`python setup.py install` - This will install the library

`python setup.py test` - This will run the test suite

----

### Input Format

The data of the relative reactions can be stored in an .xml file.

The user needs to have a **\<phase\>** tag to specify a list of species involved in the reaction. Pay particular attention to the `reversible="no"` or `reversible="yes"` in the **\<reaction>** tag when specifying reaction types. The order should also be consistent with the input for concentrations when a user calculates the reaction rates.

The second tag of the .xml file needs to store reaction information wrapped by **\<reactionData\>**. Our parser supports multiple reactionData tags when parsing the .xml file.

The user also needs to specify reaction temperature.

For more details of correctly formatting the input file, please refer to our [sample input](https://github.com/cs207team3/cs207-FinalProject/blob/master/rxns.xml).

If the .xml file is not properly formatted, the parser.py will print a warning and return an empty data structure to the user.

----

### Basic Usage:
### UPDATE SECTION

After checking out this repository:
1. Import relative classes and functions from **parser.py** and **chemkin.py**.

2. Create the reaction system directly from an .xml data file (see 3.1), obtain reaction data by parsing a properly formatted .xml file using the `read_data()` function (see 3.2), or manually create reactions using the constructor in the `Reaction()` class.

#### Code Examples:
### UPDATE SECTION

3.1 To create a reaction system directly from .xml file, use the following code.
```
>>> from chemkin import *
>>> from parser import *
>>> concs = [2., 1., .5, 1., 1.] #reactant concentrations
>>> T = 1500 #temperature
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

----

### Future Feature:
Our proposed future feature will incorporate a Graphical User Interface (GUI) for use with this chemical kinetics library.

**Motivation and Description:**

Perhaps the biggest motivation for providing users of our library a GUI is that it can offer users with basic knowledge of python the ability to run their chemical kinetics calculations with confidence. A GUI will offer a user friendly tool with the same functionality of the underlying library. Users will be restricted to specific inputs and offered hints or recommendations directly in the GUI to ensure they use the library properly. Most users will be familiar with GUIs from their daily interaction with modern operating systems, so using a GUI makes sense from a basic usability standpoint.

**How the GUI will fit into this code base (and package):**

The GUI will be integrated into the existing code as a graphical overlay to the underlying modules. It will be installed as part of the `python setup.py install` operation.

**Modules to be written:**

FILL IN HERE

**Methods to implement:**

FILL IN HERE

**Envisioned user experience:**

After installing the underlying library, the user will run a command in their terminal to bring up the GUI. They will be presented with a welcome window that offers radio button options to either `Use reaction input file` or `Manually input reactions`. There should be a link to see a `LINK: Properly formatted input file`.

If the user has an input file, there will be a directory search function to find the input file.

If they want to input reactions manually, there will be a series of input boxes to add applicable system reaction information found in a properly formatted file: `species, reaction id, reversible?, type, equation, type of reaction rate coefficient, A, b, E, reactants, and products`.

The GUI will display all the reactions in the GUI after parsing the input file or manual user addition.

After the GUI has the reactions, the user specifies specie concentrations (in the order specified by the species array).

There will be a `Calculate Reaction Rates` button, which presents the system reaction rates at the bottom of the window.

**Required external dependencies:**

FILL IN HERE
