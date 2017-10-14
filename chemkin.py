import numpy as np

class Reaction():
	def __init__(self, reactants, products, reversible, reac_type, reac_id, coef_type, coef):
		self.reactants = reactants
		self.products = products
		self.reversible = reversible
		self.reac_type = reac_type
		self.reac_id = reac_id
		self.coef_type = coef_type
		self.coef = coef

	def set_reac_coefs(self, T):
		if self.coef_type == 'Constant':
			self.k = self.init_const_coef(self.coef['k'])
		elif self.coef_type == 'Arrhenius':
			self.k = self.init_arr_coef(self.coef['A'], self.coef['E'], T)
		elif self.coef_type == 'modifiedArrhenius':
			self.k = self.init_marr_coef(self.coef['A'], self.coef['b'], self.coef['E'], T)	

	def init_const_coef(self, k):
		"""Simply returns a constant reaction rate coefficient
		
		INPUTS:
		=======
		k: float, default value = 1.0
		   Constant reaction rate coefficient
		
		RETURNS:
		========
		k: float
		   Constant reaction rate coefficient
		
		EXAMPLES:
		=========
		>>> k_const(5.0)
		5.0
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
		
		EXAMPLES:
		=========
		>>> k_arr(2.0, 3.0, 100.0)
		1.9927962618542914
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
		
		EXAMPLES:
		=========
		>>> k_mod_arr(2.0, -0.5, 3.0, 100.0)
		0.19927962618542916
		"""
		if A < 0.0:
			raise ValueError("A = {0:18.16e}:  Negative Arrhenius prefactor is prohibited!".format(A))

		if T < 0.0:
			raise ValueError("T = {0:18.16e}:  Negative temperatures are prohibited!".format(T))

		if R < 0.0:
			raise ValueError("R = {0:18.16e}:  Negative ideal gas constant is prohibited!".format(R))

		return A * (T**b) * np.exp(-E / R / T)


class Reaction_system():
	def __init__(self, reactions, order, concs, T):
		self.concs = concs
		self.nu_react, self.nu_prod = self.init_matrices(reactions, order)
		self.ks = []
		for reac in reactions:
			reac.set_reac_coefs(T)
			self.ks.append(reac.k)


	def init_matrices(self, reactions, order):
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
			   size: num_reactions
			   progress rate of each reaction
		
		EXAMPLES:
		=========
		>>> progress_rate_2(np.array([[2.0, 1.0], [1.0, 0.0], [0.0, 1.0]]), np.array([2.0, 1.0, 1.0]), 10.0)
		array([ 40.,  20.])
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
		   size: num_species
		   reaction rate of each specie
		
		EXAMPLES:
		=========
		"""
		rates = self.progress_rate()
		print(rates)
		nu = self.nu_prod - self.nu_react
		
		return np.dot(nu, rates)
		# reac_rates = []
		# for i in range(len(nu)):
		# 	cum = 0
		# 	for j in range(len(rates)):
		# 		cum += nu[i][j] * rates[j]
		# 	reac_rates.append(cum)
		# return reac_rates

		
