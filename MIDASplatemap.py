# -*- coding: utf-8 -*-
"""
MIDAS Plate Map Package
Author: Jeonghoon Choi, Kaitlyn Toy

Many parts based off pre-existing package "platemapping" by lawrencecollins
link - https://pypi.org/project/platemapping/

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import string
import os
import csv

dim = {6:(2,3), 12:(3,4), 24:(4,6), 96:(8,12), 384:(16,24)} 
defaultwell = {'sample_name','row','column','index'}
defaultplate = {'screen','date','Title'}
wellfields = {'pcr' : {'volume_gdna','volume_water', 'unit','injection'},'gdna' : {'volume', 'unit','avg_concentration','injection'}, 'kingfisher' : {'organ_weight','tattoo_number','volume_TL','unit','mg_tissue','organ','injection','cell_number','sample_type','treatment_id','cage','weight_g'}, 'p7 index' : {'index_barcode'}, 'quantit' : {'organ','concentration','dilution_factor','volume', 'unit','injection'}}
platefields = {'pcr' : {'mastermix'},'gdna' : {}, 'kingfisher' : {'sampletype'}, 'postpcr' : {}, 'quantit' : {}}

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
        if category is not None:
            fields.update(wellfields[category])
    elif classname =='Plate':
        fields = defaultplate
        if category is not None:
            fields.update(platefields[category])
    return fields

class Well:
    """Class for Well objects.
    
    Generate a structure to handle wells within plates and contents of the well.
    
        Args:
            _category (str): parameter that determines the loading of category dependent fields
            _fields (dict): dictionary of field values of well depending on category
    """
    
    def __init__(self, category):
        """Initiation object of Well class
        
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
    
    def __setfield__(self,name, value):
        """Function to set values of attributes within the field attribute of Well class
        
            Args:
                name: The field name
                value: The value for the field
        """
        
        if name in self._fields.keys():
            self._fields[name] = value
        else:
            raise TypeError('Field does not exist in Well object')
        
    def __getfield__(self, name):
        """Overwrites the attribute getter default function

            Args:
                name: The field name
                
            Returns:
                The value contained in the field

        """
        
        if name in self._fields.keys():
            return self._fields[name]
        else:
            raise TypeError('Field does not exist in Well object')
        
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
    
    def df_return(self):
        """Returns the Well object information organized in a pandas DataFrame format
        
            Returns:
                DataFrame object with information organized
        """
        df = pd.DataFrame([self._fields])
        return df   
    
    def df2well(self, df):
        """Returns Well object with information extracted from a pandas DataFrame
        
            Returns: 
                Well object with information organized
        """
        fields = list(df.index)
        for i in fields:
            header = i.lower()
            value = list(df.loc[i])
            value = value[0]
            self.__setfield__(header, value)
        
        
class Plate:
    """Class for Plate objects.
    
    Generate a structure to handle plates and contents of plate and according metadata.
    
    Attributes:
        _category (str): content of plate - determines the nondefault field creation
        _fields (dict): dictionary of field values of well depending on category 
        _size (int): number of wells in plate
        _wells (list(Well)): 2D list of Well objects that correspond to plate dimensions
    """
    def __init__(self, category, size):
        """Initiation object of Plate class
        
            Args:
                _category (str): content of plate - determines the nondefault field creation
                _fields (dict): dictionary of field values of well depending on category 
                _size (int): number of wells in plate
                _wells (list(Well)): 2D list of Well objects that correspond to plate dimensions
        """
        defaultlist = _getfields('Plate', category)
        default = {}
        for name in defaultlist:
            default[name] = None
        self._fields = default
        self._category = category
        self._size = size
        if size not in dim.keys():
            self._wells = None
            raise TypeError('Invalid Plate Size')
        else: 
            wells = []
            letters = list(string.ascii_uppercase)
            rows = letters[0:(dim[size])[0]]
            rowindex = rows*(dim[size])[1]
            rowindex.sort()
            columns = list(range(1, (dim[size])[1]+1))
            columnindex = columns*(dim[size])[0]

            for i in range(size):
                temp = Well(category)                
                temp.__setfield__('row', rowindex[i])
                temp.__setfield__('column', columnindex[i])
                temp.__setfield__('index' , rowindex[i]+str( columnindex[i]))
                wells.append(temp)
                
            self._wells = wells
        
    def __getfield__(self, name):
        """Overwrites the attribute getter default function

            Args:
                name: The field name
                
            Returns:
                The value contained in the field

        """
        
        if name in self._fields.keys():
            return self._fields[name].value
        else:
            raise TypeError('Field does not exist in Plate object')
        """Overwrites the attribute getter default function
    
            Args:
                name: The field name
                
            Returns:
                The value contained in the field
        """
        if name in self._fields.keys():
            return self._fields[name].value
        else:
            raise TypeError('Field does not exist in Well object')
            
    def get_category(self):
        """Returns the category attribute of the Plate class object
        
            Returns:
                The string the describes the category of the content in the plate.
        """
        """Returns the category the palte is classified as
        
            Returns:
                String of category name
        """
        return self._category
        return self.category
    
    def get_size(self):
        """Returns the number of wells within the plate
        
            Returns:
                Integer value of number of wells in plate
        """
        return(self._size)
        
    def df_platemap(self, attr = 'sample_name'):
        """Displays specified information of all Well objects in Plate as a pandas DataFrame format organized in the platemap dimensions.
            Arg:
                attr(string): the specific field name of interest to be sent as content in the DataFrame. Defaults to sample_name.
            Returns:
                df (DataFrame): DataFrame object with information organized
        """

        attr_df = [0]*len(self._wells)
        for i in range(len(self._wells)):
            attr_df[i] = self._wells[i]._fields[attr]
        reshaped = np.asarray(attr_df).reshape(dim[self._size])
        letters = list(string.ascii_uppercase)
        rowindex = letters[0:(dim[len(self._wells)])[0]]
        columnindex = list(range(1, (dim[len(self._wells)])[1]+1))
        df = pd.DataFrame(reshaped, index = rowindex, columns = columnindex)
        print(df)
        
        return df
    
    def df_fieldinfo(self, attr = 'sample_name'):
        """Displays specified information of all Well objects in Plate as a linear tabular DataFrame format.
        
            Args:
                attr (str): the specific field name of interest to be sent as content in the DataFrame. Defaults to sample_name.
            
            Returns:
                df (DataFrame): DataFrame of the plate information with index as the well index, and column as attr.
        """
        index = []
        field = []
        for i in self._wells:
            index.append(i.__getfield__('index'))
            field.append(i.__getfield__(attr))
        df = pd.DataFrame({attr: field}, index = index)
        print(df)
        
        return df
        
    def df_allfields(self):
        """Organizes all information of each well in Plate and combines it as a linear tabular DataFrame.
            
            Returns: 
                df (DataFrame): DataFrame of the plate information with index as the wmetell index.
        """ 
        table = []
        for i in self._wells:
            temp = i.df_return()
            table.append(temp)
        df = pd.concat(table)
        df = df.set_index('index')
        print(df)
        
        return df
    
    def visualize(self, attr = 'sample_name'):
        """Provides an image of the visualized format of platemap.
        
        Arg: 
            attr(str): String input of field name(s) to visualize
        Returns:
            None.
        """
        df = self.df_platemap(attr).values
        fig = plt.figure(dpi = 150)
        grid = gridspec.GridSpec(dim[self._size][0]+1, dim[self._size][1]+1, wspace = 0.1, hspace=0.1, figure = fig)
         # plot row labels in extra row
        for i in range(1, (dim[self._size][0]+1)):
            ax = plt.subplot(grid[i, 0])
            ax.axis('off')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.text(0.5, 0.5, list(string.ascii_uppercase)[i-1], size = 10, ha = "center", va="center")
            
        # plot column labels in extra column
        for i in range(1, (dim[self._size][1]+1)):
            ax = plt.subplot(grid[0, i])
            ax.axis('off')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.text(0.5, 0.5, list(range(1, (dim[self._size])[1]+1))[i-1], size = 8, ha = "center", va="center")
        fig.suptitle('{}'.format(self._fields['Title']))
        for i in range(1, (dim[self._size][1]+1)):
            for j in range(1, (dim[self._size][0]+1)):
                ax = plt.subplot(grid[j,i])
                # ax.axis('off')
                ax.set_xticklabels([])
                ax.set_yticklabels([])
                plt.tick_params(left = False, bottom = False)
                ax.text(0.5,0.5,df[j-1][i-1] ,color='red',ha = "center", va="center")
        return fig
    

def readcsv(path, well_type):
    df = pd.read_csv(path, header=None)
    table_names = ["metadata", "plate_data"]
    groups = df[0].isin(table_names).cumsum()
    tables = {g.iloc[0,0]: g.iloc[1:] for k,g in df.groupby(groups)}
    
    metadata = tables['metadata']
    raw_plate_data = tables['plate_data']
    #go through the metadata table and make some 
    
    metadata_col = list(metadata.iloc[0])
    metadata_val = list(metadata.iloc[1])
    
    plate_info = pd.DataFrame(metadata_val,index=metadata_col).transpose()
    
    plate_data_header = list(raw_plate_data.iloc[0])
    plate_data_value = (raw_plate_data.iloc[1:]).reset_index(drop=True)
    plate_data_value.columns = plate_data_header
    
    wells = []
    
    for i in range(len(plate_data_value)):
        row = plate_data_value.iloc[i]
        row = pd.DataFrame(row)
        temp = Well(well_type)
        temp.df2well(row)
        wells.append(temp)
    
    
    plate_count = int(len(plate_data_value)/24)+1
    empty_wells = 24-len(plate_data_value)%24
    empty_wells = [Well(well_type)]*empty_wells
    
    plates = [0]*plate_count
    for i in range(len(plates)):
        if i == plate_count-1:
            well_list = wells[0+(24*i)::]
            well_list.extend(empty_wells)
            temp_plate = Plate(well_type,24)
            temp_plate._wells = well_list
            temp_plate._fields['Title'] = 'Plate ' + str(i+1)
            plates[i] = temp_plate
            
        else:
            temp_plate = Plate(well_type,24)
            temp_plate._wells = wells[0+(24*i):24+(24*i)]
            temp_plate._fields['Title'] = 'Plate ' + str(i+1)
            plates[i] = temp_plate
            
    return plates
            

    
def main():
    hello = Well('gdna')
    df = (hello.df_return())
    # print(df)
    goodbye = Plate('gdna',size = 96)
    df2 = goodbye.df_platemap('index')
    df3 = goodbye.df_fieldinfo('sample_name')
    df4 = goodbye.df_allfields()
    fig = goodbye.visualize()
    df5 = readcsv(r"/Users/jeonghoonchoi/Desktop/MIDASplatemap/MIDASplatemap/M22-S06-Lung-Organ_Weights.csv",'kingfisher')
    
    return 0

main()