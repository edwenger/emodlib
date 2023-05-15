from .._emodlib_py.malaria import Infection, IntrahostComponent, Susceptibility

import numpy as np

# copied from emodpy-malaria and idmtools-calibra (post-2017 settings)
# TODO: make accessible from IntrahostComponent::params
base_gametocyte_mosquito_survival = 0.002011099
cytokine_gametocyte_inactivation = 0.01667

# copied from EMOD
MICROLITERS_PER_BLOODMEAL = 2.0
FEVER_DEGREES_CELSIUS_PER_UNIT_CYTOKINES = 4.0

def basic_sigmoid(threshold, variable):
    return variable / (threshold + variable) if variable > 0 else 0.0

@property
def infectiousness(self: IntrahostComponent) -> float:
    cytokines = (self.fever_temperature - 37.0) / FEVER_DEGREES_CELSIUS_PER_UNIT_CYTOKINES
    fever_effect = basic_sigmoid(threshold=cytokine_gametocyte_inactivation, variable=cytokines)
    return 1-np.exp(-(self.gametocyte_density * MICROLITERS_PER_BLOODMEAL * base_gametocyte_mosquito_survival * (1 - fever_effect)))

IntrahostComponent.infectiousness = infectiousness

__all__ = ["IntrahostComponent", "Susceptibility", "Infection"]
