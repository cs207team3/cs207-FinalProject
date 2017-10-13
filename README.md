[![Build Status](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/cs207team3/cs207-FinalProject.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/cs207team3/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/cs207team3/cs207-FinalProject?branch=master)

## cs207-FinalProject: A Chemical Kinetics Library
### Final Project repository for CS207 Team 3
##### Team Members: Jiacheng Shi, Weihang Zhang, & Andrew Lund

---

### User's Guide
**Introduction:**

The purpose of our library is to return the reaction rate of a system of N species undergoing M reactions. The reactions should be irreversible and elementary of the form:
##### reaction equation here

\sum_{i=1}^{N}{\nu_{ij}^{\prime}\mathcal{S}_{i}} \longrightarrow

In the future we intend on implementing features to handle both reversible and non-elementary reactions.

-----

The progress rate for each reaction is given by:
##### progress rate equation here
The reaction rate of each specie i can be written as:
##### Reaction rate equation here
Describe what problem the code is solving. You may borrow the Latex expressions from my lecture notes. Discuss in broad
strokes what the purpose of the code is along with any features. Do not describe the details of the code yet.

------

**Installation:**

All the code related to this library can be found in this repository, specifically in the files **parser.py** and **chemkin.py**.

In order to run the test suite accompanying these files, do the following:

----

We are not releasing this code as a package yet, but when we do that this section will include instructions how how to install the package.

----

### Basic Usage and Examples:
After downloading the files parser.py and chemkin.py:
1. Open a new python file
2. import parser and chemkin
3.
Provide a few examples on using your software in some common situations. You may want to show how the code works with a small set of reactions.

Note: The order the user inputs reaction concentrations will be matched to the reactants pulled from the '<phase>' tag
