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

defaultwell = {'sample_name','row','column','category', 'index'}
wellfields = {'pcr' : {'volume', 'unit'},'gdna' : {'volume', 'unit'}, 'kingfisher' : {}, 'postpcr' : {}, 'quantit' : {'dilution_factor','volume', 'unit'}}
# platefields = {'pcr' : {'mastermix'},'gdna' : {}, 'kingfisher' : {'sampletype'}, 'postpcr' : {}, 'quantit' : {}}

def _getfields(classname, category):
    """Get the fields/keys of class object for object initialization.
    
        Args:
            classname (str): the name of the class object that is being initialized
            category (str): the category of the class that distinguishes type of content
        Returns:
            The dictionary stored within the specific key/field.
    """
    if classname == 'Well':
        fields = defaultwell
        fields.update(wellfields[category])
        return fields
    # else classname =='Plate':
    #     fields = defaultplate
    #     fields = fields.update(platefields[category])
        
    
        

class Well:
    """Class for Well objects.
    
    Generate a structure to handle wells within plates and contents of the well.
    
        Args:
            _category (str): parameter that determines the loading of category dependent fields
            _fields (dict): dictionary of field values of well depending on category
    """
    
    def __init__(self, category):
        """Initiation object of Well object
        
            Args:
                _category (str): parameter that determines the loading of category dependent fields
                _fields (dict): dictionary of field values of well depending on category
        """
        
        defaultlist = _getfields('Well', category)
        default = {}
        
        for name in defaultlist:
            default[name] = None
        self._fields = default
        self._category = category
        
    def __getattr__(self, name):
        """Overwrites the attribute getter default function

            Args:
                name: The field name
                
            Returns:
                The value contained in the specified field

        """
        
        if name in self._fields.keys():
            return self._fields[name].value
        else:
            return TypeError('Field does not exist in Well object')
        
    def get_row(self):
        """Returns the value of a the 'row' field of a Well class object
                
            Returns:
                The row value of specified well
        """
        
        return self._fields['row']
    
    def get_column(self):
        """Returns the value of the 'column' field of a Well class object
                
            Returns:
                The column value of specified well
        """
        
        return self._fields['column']
    
    def get_index(self):
        """Returns the value of the 'index' field of a Well class object
                
            Returns:
                The well index value of specified well
        """
        
        return self._fields['index']
    
    def get_sample_name(self):
        """Returns the value of a 'sample_name' field of a Well class object
                
            Returns:
                The column value of specified well
        """
        
        return self._fields['sample_name']
      
        
class Plate:
    """Class for Plate objects.
    
    Generate a structure to handle plates and contents of plate and according metadata.
    
    Default Attributes:
        screen (str): unique identification string for screen
        size (int): number of wells in plate
        date (str): date of plate creation/sample processing
        content (str): content of plate - determines the nondefault field creation
    """
    
def main():
    hello = Well('gdna')
    return 0

main()
        