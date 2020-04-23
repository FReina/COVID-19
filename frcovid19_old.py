import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import math as m 
import scipy as sp 
import csv

def confidence_ellipse(x,y,ax,width_coeff=6,**kwargs):
    """
    from https://stackoverflow.com/questions/20126061/creating-a-confidence-ellipses-in-a-sccatterplot-using-matplotlib
    """

    from matplotlib.patches import Ellipse
    
    cov = np.cov(x, y)
    lambda_, v = np.linalg.eig(cov)
    lambda_ = np.sqrt(lambda_)  
    ell = Ellipse(xy=(np.mean(x), np.mean(y)),width=lambda_[0]*width_coeff, height=lambda_[1]*width_coeff,angle=np.rad2deg(np.arccos(v[0, 0])),**kwargs)

    return ax.add_patch(ell)

def last_update(dates,language):
    """
    A very short function that prints when the analysis was latest updated.

    INPUT:
    dates = the list with the dates in the data dictionary
    language = ITA or ENG
    """
    if language =='ITA':
        print("Ultimo aggiornamento il {}".format(dates[-1]))
    elif language == 'ENG':
        print("Last updated on {}".format(dates[-1]))

def region_names():
    """
    reminder of region names
    """
    regnames = ['Abruzzo', 'Basilicata', 'P.A. Bolzano', 'Calabria', 'Campania','Emilia-Romagna','Friuli Venezia Giulia','Lazio','Liguria','Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia','Toscana','P.A. Trento']
    print('Seleziona la regione tra le seguenti. Attenzione agli spazi, trattini, ecc./These are the names of the regions in Itaian.')
    print(regnames)


def data_loader_generic(filename):
    """
    generic csv data loader. Takes a csv file, 
    and gives out a dict in which the keys are 
    defined by the first row of the csv file.
    All elements are string.

    INPUT:

    filename = PATH string of the csv file

    OUTPUT: 
    
    out = a dictionary
    keys = the keys of out
    """
        #initialize reader
    content = []
    #open the file and load the contents into it
    with open(filename) as datafile:
        rawcontents = csv.reader(datafile, delimiter=',')
        for row in rawcontents:
            content.append(row)

    keys = content[0]
    out={}
    for i in range(0,len(keys)):
        out[keys[i]] = [];
        for j in range(1,len(content)):
            out[keys[i]].append(content[j][i])
    
    return keys, out

def data_loader_nazionali(filename):
    """
    This function loads the data from the Protezione Civile and 
    returns a dictionary in which they are all divided by field. 
    The dates are in MM-DD format. This version leaves the least
    control to the user.

    INPUT:
    filname = PATH string of the Protezione Civile .csv file

    OUTPUT
    out = a dictionary containing the data. The Keys for this dict are the fields in the CSV file
    """
    keys, content = data_loader_generic(filename)
    out={}
    for key in keys:
        out[key] = []
        for element in content[key]:
            if key == 'data':
                #dates get separated from the 'T18:00:00' string, the format gets switched to DD/MM
                giorno = element[8:10]
                mese = element[5:7]
                out[key].append((giorno + '/'+ mese))
            elif key not in ['note_en','note_it','stato']:
                out[key].append(int(element))

    for key in ['note_en','note_it','stato']:
        out.pop(key)

    return out

def data_loader_region(filename,region_name):
    """
    This function loads the file where the data by region is stored. 
    The file structure is a little different and contains a number identifier by region, that we can use.
    region_handle is necessary. Unfortunately, our life is made difficult by the fact 
    that Trento and Bolzano have different names, but the same region code.
    For now, these two provinces will be considered separately.
    """
    
    keys, content = data_loader_generic(filename)
    out = {}
    for key in keys:
        out[key] = []
        for j in range(0,len(content[key])):
            if content['denominazione_regione'][j] == region_name:
                if key == 'data':
                    giorno = content[key][j][8:10]
                    mese = content[key][j][5:7]
                    out[key].append((giorno + '/'+ mese))
                elif key not in ['stato','denominazione_regione','lat','long','note_it','note_en']:
                    out[key].append(int((content[key][j])))
    
    for key in ['stato','denominazione_regione','lat','long','note_it','note_en']:
        out.pop(key)
    
    return out

def moving_average(x,N=1,mode = 'same'):
    ''' This is a function that makes a moving average of a 1d vector using numpy.convolve
    INPUTS: 
    x: one-dimensional vector
    N: dimension of the moving average
    mode: the mode of numpy.convolve, that determines the behaviour at the edges of the moving average. Valid values are full, same and valid. Check the doc for numpy.convolve for details.
    OUTPUT:
    out: the result of the averaging operation'''
    
    import numpy as np

    averaging_window = ([1]*N)
    averaging_window = [i/N for i in averaging_window]

    return np.convolve(x,averaging_window,mode)


def data_loader_nazionali_OLD(filename):
    """
    DEPRECATED
    This function loads the data from the Protezione Civile and 
    returns a dictionary in which they are all divided by field. 
    The dates are in MM-DD format. This version leaves the least
    control to the user.

    INPUT:
    filname = PATH string of the Protezione Civile .csv file

    OUTPUT
    out = a dictionary containing the data. The Keys for this dict are the fields in the CSV file
    """
    #initialize reader
    content = []
    #open the file and load the contents into it
    with open(filename) as datafile:
        rawcontents = csv.reader(datafile, delimiter=',')
        for row in rawcontents:
            content.append(row)
    
    #define the dictionary keys from the reader
    keys = content[0];
    #initialize output
    out={}
    for i in range(0,len(keys)):
        out[keys[i]] = [];
    #load the data into the dictionary
    for i in range(0,len(keys)):
        for j in range(1,len(content)):
            if 2<i<13:
                 #numerical data is passed as numbers
                out[keys[i]].append(int(content[j][i]))
            elif keys[i] == 'data':
                #dates get separated from the 'T18:00:00' string
                giorno = content[j][i][8:10]
                mese = content[j][i][5:7]
                out[keys[i]].append((giorno + '/'+ mese))
                #out[keys[i]].append(content[j][i][5:10])  
            else:
                #The rest is passed as it is
                out[keys[i]].append(content[j][i])
    
    #return the data
    return out


