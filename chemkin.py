"""
This is a chemical kinetics module which can be used to calculate the reaction
rate of a system of elementary, irreversible reactions.

Future updates are intended to address more reaciton types (duplicate,
three-body, and reversible).

For more infomation regarding chemical kinetics, please visit:
https://en.wikipedia.org/wiki/Chemical_kinetics
"""
import numpy as np

class Reaction():
	"""Reaction Class for chemical kinetics calculations

	ATRIBUTES:
	=========
	reactants: list of reaction reactant species
	products: list of reaction product species
	reversible: boolean
	reac_type: reaction type (elementary, duplicate(not yet supported),
				three-body(not yet supported)
	reac_id: ID of reaction
	coef_type: Reaction rate coefficient (constant, Arrhenius, Modified Arrhenius)
	coef: list of reaction rate variables (A, E, b, T)

	METHODS:
	=======
	.__init__: init attributes
	.set_reac_coefs: sets reaction coefficients (k, A, E, b, T)
	.init_const_coef: returns k for constant reaction rate
	.init_arr_coef: returns Arrhenius reaction rate
	.init_marr_coef: returns Modified Arrhenius reaction rate

	# EXAMPLES:
	# ========
	# >>>TBD
	"""
	def __init__(self, reactants, products, reversible, reac_type, reac_id, coef_type, coef):
		"""Returns class attributes:
		self.reactants
		self.products
		self.reversible
		self.reac_type
		self.reac_id
		self.coef_type
		self.coef
		"""
		self.reactants = reactants
		self.products = products
		self.reversible = reversible
		self.reac_type = reac_type
		self.reac_id = reac_id
		self.coef_type = coef_type
		self.coef = coef

	def __eq__(self, other):
		return self.reactants == other.reactants \
			and self.products == other.products \
			and self.reversible == other.reversible \
			and self.reac_type == other.reac_type \
			and self.coef == other.coef \

	def set_reac_coefs(self, T):
		"""Set reaction coefficients as:
		Constant, Arrhenius, or Modified Arrhenius

		INPUTS:
		======
		T: 	float
			Temperature
			Must be positive
		"""
		if self.coef_type == 'Constant':
			self.k = self.init_const_coef(self.coef['k'])
		elif self.coef_type == 'Arrhenius':
			self.k = self.init_arr_coef(self.coef['A'], self.coef['E'], T)
		elif self.coef_type == 'modifiedArrhenius':
			self.k = self.init_marr_coef(self.coef['A'], self.coef['b'], self.coef['E'], T)

	def init_const_coef(self, k):
		"""Returns a constant reaction rate coefficient

		INPUTS:
		=======
		k: float, default value = 1.0
		   Constant reaction rate coefficient

		RETURNS:
		========
		k: float
		   Constant reaction rate coefficient

		# EXAMPLES:
		# =========
		# >>> init_const_coef(5.0)
		# 5.0
		"""
		if k < 0:
			raise ValueError("Negative reaction rate coefficients are prohibited.")

		return k

	def init_arr_coef(self, A, E, T, R=8.314):
		"""Calculates the Arrhenius reaction rate coefficient

		INPUTS:
		=======
		A: float
		   Arrhenius prefactor
		   Must be positive
		E: float
		   Activation energy
		T: float
		   Temperature
		   Must be positive
		R: float, default value = 8.314
		   Ideal gas constant
		   Must be positive

		RETURNS:
		========
		k: float
		   Arrhenius reaction rate coefficient

		# EXAMPLES:
		# =========
		# >>> init_arr_coef(2.0, 3.0, 100.0)
		# 1.9927962618542914
		"""

		if A < 0.0:
			raise ValueError("A = {0:18.16e}:  Negative Arrhenius prefactor is prohibited!".format(A))

		if T < 0.0:
			raise ValueError("T = {0:18.16e}:  Negative temperatures are prohibited!".format(T))

		if R < 0.0:
			raise ValueError("R = {0:18.16e}:  Negative ideal gas constant is prohibited!".format(R))

		return A * np.exp(-E / R / T)

	def init_marr_coef(self, A, b, E, T, R=8.314):
		"""Calculates the modified Arrhenius reaction rate coefficient

		INPUTS:
		=======
		A: float
		   Arrhenius prefactor
		   Must be positive
		b: float
		   Modified Arrhenius parameter
		E: float
		   Activation energy
		T: float
		   Temperature
		   Must be positive
		R: float, default value = 8.314
		   Ideal gas constant
		   Must be positive

		RETURNS:
		========
		k: float
		   Modified Arrhenius reaction rate coefficient

		# EXAMPLES:
		# =========
		# >>> init_marr_coef(2.0, -0.5, 3.0, 100.0)
		# 0.19927962618542916
		"""
		if A < 0.0:
			raise ValueError("A = {0:18.16e}:  Negative Arrhenius prefactor is prohibited!".format(A))

		if T < 0.0:
			raise ValueError("T = {0:18.16e}:  Negative temperatures are prohibited!".format(T))

		if R < 0.0:
			raise ValueError("R = {0:18.16e}:  Negative ideal gas constant is prohibited!".format(R))

		return A * (T**b) * np.exp(-E / R / T)



class Reaction_system():
	"""Reaction_system Class for chemical kinetics calculations

	ATRIBUTES:
	=========
	concs: 		list of floats
				Reactant concentrations
				Must be positive
	nu_react: 	list of floats
	 			Stoichiometric coefficients for reactants
	nu_prod: 	list of floats
				Stoichiometric coefficients for products
	ks:			list of floats
				Reaction rate coefficients

	METHODS:
	=======
	.__init__: init attributes
	.init_matrices: returns reactant and product matrices
	.progress_rate: returns progress rate of system of reactions
	.reaction_rate: returns reaction rate of system of reactions

	# EXAMPLES:
	# ========
	# >>> TBD
	"""
	def __init__(self, reactions, order, concs, T):
		"""Returns class attributes, and sets reaction
		temperatures and reaction rate coefficients

		ATTRIBUTES:
		============
		self.reactions
		self.order
		self.concs
		self.T
		"""
		if any(c < 0 for c in concs):
			raise ValueError('Concentration should not be Negative!')

		self.concs = concs
		self.nu_react, self.nu_prod = self.init_matrices(reactions, order)
		self.ks = []
		for reac in reactions:
			reac.set_reac_coefs(T)
			self.ks.append(reac.k)

	def init_matrices(self, reactions, order):
		"""Initializes reactant and product matrices for progress rate calculations

		INPUTS
		======
		reactions: 	list of floats
					System reactant species
		order:		list of floats

		RETURNS:
		=======
		nu_react: 	array of floats
		 			Stoichiometric coefficients for reactants
		nu_prod: 	array of floats
					Stoichiometric coefficients for products

		# EXAMPLES:
		# ========
		# >>> TBD
		"""
		nu_reac = np.zeros((len(order), len(reactions)))
		nu_prod = np.zeros((len(order), len(reactions)))
		for i in range(len(order)):
			for j in range(len(reactions)):
				if order[i] in reactions[j].reactants:
					nu_reac[i, j] = reactions[j].reactants[order[i]]
				if order[i] in reactions[j].products:
					nu_prod[i, j] = reactions[j].products[order[i]]
		return nu_reac, nu_prod

	def progress_rate(self):
		"""Returns the progress rate of a system of irreversible, elementary reactions

		RETURNS:
		========
		omega: numpy array of floats
			   size: number of reactions
			   progress rate of each reaction

		# EXAMPLES:
		# =========
		# This should be updated
		# >>> progress_rate(np.array([[2.0, 1.0], [1.0, 0.0], [0.0, 1.0]]), np.array([2.0, 1.0, 1.0]), 10.0)
		# array([ 40.,  20.])
		"""

		progress = self.ks.copy() # Initialize progress rates with reaction rate coefficients
		for jdx, prog in enumerate(progress):
			if prog < 0:
				raise ValueError("k = {0:18.16e}:  Negative reaction rate coefficients are prohibited!".format(prog))
			for idx, xi in enumerate(self.concs):
				nu_ij = self.nu_react[idx, jdx]
				if xi  < 0.0:
					raise ValueError("x{0} = {1:18.16e}:  Negative concentrations are prohibited!".format(idx, xi))
				if nu_ij < 0:
					raise ValueError("nu_{0}{1} = {2}:  Negative stoichiometric coefficients are prohibited!".format(idx, jdx, nu_ij))

				progress[jdx] *= xi**nu_ij
		return progress

	def reaction_rate(self):
		"""Returns the reaction rate of a system of irreversible, elementary reactions

		RETURNS:
		========
		f: numpy array of floats
		   size: number of species
		   reaction rate of each species

		# EXAMPLES:
		# =========
		# >>> data = read_data('t.xml')
		# concs = [2., 1., .5, 1., 1.]
		# T = 1500
		# system = Reaction_system(data['reactions']['test_mechanism'], data['species'], concs, T)
		# system.reaction_rate()
		# [ -2.81117621e+08  -2.85597559e+08   5.66715180e+08   4.47993847e+06
  # 		-4.47993847e+06]
		"""
		rates = self.progress_rate()
		print(rates)
		nu = self.nu_prod - self.nu_react

		return np.dot(nu, rates)
