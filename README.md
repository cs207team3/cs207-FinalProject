[![Build Status](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/cs207team3/cs207-FinalProject/badge.svg?branch=master&maxAge=0)](https://coveralls.io/github/cs207team3/cs207-FinalProject?branch=master&maxAge=0)

## cs207-FinalProject: A Chemical Kinetics Library and WebApp
### Final Project repository for CS207 Team 3
##### Team Members: Jiacheng Shi, Weihang Zhang, & Andrew Lund

---

### User's Guide:
There are two ways to use our chemical kinetics library:
1. Download and install this repository following the instruction in the **Library Installation** section below.
2. Visit our chemkin [webapp](http://chemkin.pythonanywhere.com/) and upload your properly formatted .xml reactions file.

For more details about correctly formatting the input file, please refer to the [sample input file](https://github.com/cs207team3/cs207-FinalProject/blob/master/tests/t.xml)

---

**Introduction:**

...Please see the chart below for equation symbols and their meaning...

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

### Library Installation:
All the code related to this library can be found in this repository. This includes the NASA polynomials stored as an SQL database `nasa.sqlite` in order to calculate the backwards reaction rate coefficients for reversible elementary reactions.

To install this library and run the test suite:
1. Download or clone this repository.
2. Using your terminal, navigate to the local `cs207-FinalProject` folder.
3. Enter `python setup.py install` - This will install the library.
4. Enter `python setup.py test` - This will run the library's test suite.
5. You are now ready to start calculating reaction rates.

See the "Input Format" and "Basic Usage" for more step-by-step instructions.

----

### Input Format

The data of the relative reactions can be stored in an .xml file.

The user needs to have a **\<phase\>** tag to specify a list of species involved in the reaction. Pay particular attention to the `reversible="no"` or `reversible="yes"` in the **\<reaction>** tag when specifying reaction types. The order should also be consistent with the input for concentrations when a user calculates the reaction rates.

The second tag of the .xml file needs to store reaction information wrapped by **\<reactionData\>**. The parser supports multiple reactionData tags when parsing the .xml file.

The user also needs to specify reaction temperature.

For more details of correctly formatting the input file, please refer to the [sample input file](https://github.com/cs207team3/cs207-FinalProject/blob/master/tests/t.xml).

If the .xml file is not properly formatted, the parser.py will print a warning and return an empty data structure to the user.

----

### Basic Usage and Examples:

After cloning this repository:
1. Follow installation instructions above: `python setup.py install`, `python setup.py test`.

2. Create the reaction system directly from an .xml data file (see 3.1), obtain reaction data by parsing a properly formatted .xml file using the `read_data()` function (see 3.2), or manually create reactions using the constructor in the `Reaction()` class.

#### Code Examples:

3.1 To create a reaction system directly from a [properly formatted](https://github.com/cs207team3/cs207-FinalProject/blob/master/tests/t.xml) .xml input file, use the following code. The 'rxns_reversible.xml' file is found in the 'tests' folder of this repository.
```
>>> from chem3.chemkin import *
>>> from chem3.parser import *
>>> concs = [2., 1., .5, 1., 1., .5, .5, .5] #reactant concentrations
>>> T = 900 #temperature
>>> system = ReactionSystem(filename='rxns_reversible.xml') #local reaction .xml file
>>> # calculate reaction rates
>>> reaction_rates = system.reaction_rate(concs, T)
>>> reaction_rates
[7.58794849e+15 -7.55388022e+15 -7.87055958e+15 3.01455401e+13 1.88251730e+14 7.73916703e+15 -8.79625439e+13 -3.31104554e+13]
```

3.2 To calculate the reaction rate of a system, you must specify the current concentration of each species and the temperature under which the reaction takes place. The order of the concentrations will be matched to the order of the reactants list obtained from the .xml file.

```
>>> from chem3.chemkin import *
>>> from chem3.parser import *
>>> import os
>>> # parse data from xml file
>>> db_file = os.path.join(os.path.dirname(chem3.__file__), 'nasa.sqlite')
>>> data = read_data('rxns_reversible.xml', db_file)
>>> # specify concentration list and current temperature
>>> concs = [2., 1., .5, 1., 1., .5, .5, .5]
>>> T = 1500
>>> # create a system of the reactions
>>> system = ReactionSystem(data['reactions']['hydrogen_air_mechanism'], data['species'], data['low'], data['high'], data['T_cutoff'], data['T_range'])
>>> # calculate reaction rates
>>> reaction_rates = system.reaction_rate(concs, T)
>>> reaction_rates
[2.23407833e+14 -3.53181969e+14 -2.11084849e+14 3.52252690e+13 4.70006140e+13 3.84606136e+14 -7.51713182e+13 -5.08017161e+13]
```

Note: The order the user inputs reaction concentrations will be matched to the reactants pulled from the "phase" tag in the .xml file.

----

### New Feature - A Chemkin Webapp:
The newest exciting feature of this library is an accompanying webapp found at [http://chemkin.pythonanywhere.com/](http://chemkin.pythonanywhere.com/). The webapp includes all the code inherent to this library, but offers the convenience of a browser based application and eliminates the need to install this library ahead of time. You can upload a porperly formatted .xml file just like with the library and receive the same reaction rate outputs as using this library.

**Webapp Usage:**

Navigate to the webapp [homepage](http://chemkin.pythonanywhere.com/):

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/webapp1.png "webapp1")

Upload a [properly formatted](https://github.com/cs207team3/cs207-FinalProject/blob/master/tests/t.xml) .xml file using the 'Choose File' button and click 'SUBMIT'. If your file is not properly formatted you will receive an 'Incorrect file format!' message. After uploading, your reactions will be displayed in the 'REACTION SYSTEM' column below:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/webapp2.png "webapp2")

Input temperatures (within the NASA coefficient temperature range for each species) as well as species concentrations (in the same order as the .xml input file) using the gray 'example' input as a guide and click 'CALCULATE.' You will receive applicable error messages if you leave an input box blank, your temperature is outside the coefficient range, or your concentrations are too short, long, or strings. Your system reaction rates will be displayed in the right column as shown below.

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/webapp3.png "webapp3")

We hope you enjoy this new user-friendly feature.

**Motivation and Description:**

The primary motivation for providing users of this library a webapp is that it can offer users with little or no knowledge of python the ability to run their chemical kinetics calculations with confidence from a familiar looking web-based user-interface.

Our webapp is a user-friendly chemical kinetics tool with the same underlying functionality of this python library. Users will be restricted to specific inputs and offered hints or recommendations directly in the webapp to ensure they use the underlying library correctly.

Most users will be familiar with webapps from their day-to-day use of modern operating systems and web browsers, so adding a webapp to accompany this library makes sense from a basic usability standpoint.

**Implementation Details**

All webapp implementation code can be found at this [Github Repository](https://github.com/cs207team3/chemkin_web). We used a separate repository for the webapp implementation in order to ensure proper indication from the Travis CI and Coveralls badges of this repository.

The webapp is hosted by [pythonanywhere](https://www.pythonanywhere.com/) and uses their internal terminal to employ the same installation procedure as this library along with the necessary html and webapp-specific python files to allow it to function in the browser.



Implementation details including any new modules, classes, or methods. I can find the exact implementation in your code base, so your job here is to make sure I can understand why you made certain design decisions and how everything works together.

**How the GUI will fit into this code base (and package):**

The GUI will be integrated into the existing code as a graphical overlay to the underlying modules. It will be installed as part of the `python setup.py install` operation.

**Modules to be written:**

* gui.py

**Methods to implement:**

* Several classes (gui, interface, windows)
* Event listeners for buttons to collect input
* Parsers for button listeners (including checks for proper format)
* Popup for system reaction rates

**Envisioned user experience:**

After installing the underlying library, the user will run a command in their terminal to bring up the GUI. They will be presented with a welcome window that offers radio button options to either `Use reaction input file` or `Manually input reactions`. There should be a link to see a `LINK: Properly formatted input file`.

If the user has an input file, there will be a directory search function to find the input file.

If they want to input reactions manually, there will be a series of input boxes to add applicable system reaction information found in a properly formatted file: `species, reaction id, reversible?, type, equation, type of reaction rate coefficient, A, b, E, reactants, and products`.

The GUI will display all the reactions in the GUI after parsing the input file or manual user addition.

After the GUI has the reactions, the user specifies specie concentrations (in the order specified by the species array).

There will be a `Calculate Reaction Rates` button, which presents the system reaction rates at the bottom of the window.

Rough GUI layout:

![img](https://github.com/cs207team3/cs207-FinalProject/blob/master/images/gui.png "gui")

**Required external dependencies:**

* Tkinter
* PyQt
