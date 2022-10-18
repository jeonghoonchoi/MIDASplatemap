# -*- coding: utf-8 -*-
"""
MIDAS Plate Map Package
Author: Jeonghoon Choi, Kaitlyn Toy

Many parts based off pre-existing package "platemapping" by lawrencecollins
link - https://pypi.org/project/platemapping/

"""

import numpy as np
import pandas as pd
import matplotlib
import string


# metadata_tags
metadata_pcr = ['Primer', 'Concentration Lysate', ''] ##work on this list
metadata_kingfisher = []
metadata_quantit = []

# well_dimensions
wells = {6:(2, 3), 12:(3, 4), 24:(4, 6), 48:(6, 8), 96:(8, 12), 384:(16, 24)}

# default parameters
default_param  = {'Well ID', 'Concentration', 'Concentration Unit', 'Content'}

# making an empty plate map
def empty_map(size = 96):
    """ Returns an empty platemap of user defined size.
    
    Contains columns 'Well ID', 'Concentration', 'Concentration Unit', 'Content'
    
    :param size: Size of well plate - 6, 12, 24, 48, 96, 384, default = 96
    :param type: int
    
    :return: Pandas Dataframe of empty plate map
    """
    
    letters = list(string.ascii_uppercase)
    rows = letters[0:(wells[size])[0]]
    
    
# loading from a csv

# 
