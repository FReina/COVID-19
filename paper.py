#import nbformat
from nbparameterise import (extract_parameters, replace_definitions,parameter_values)
import notebooktoall.transform as trans

#with open("masso.ipynb") as f:
#    nb = nbformat.read(f,as_version=4)

#orig_parameters = extract_parameters(nb)

#params = parameter_values(orig_parameters, filename = './dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv')

#new_nb = replace_definitions(nb, params)

#with open("masso2.ipynb","w") as f:
#    nbformat.write(new_nb,f)


trans.transform_notebook(".\\analysis_v0.2.ipynb",export_list=['html'])

#nodeof = trans.get_notebook('.\masso2.ipynb')

#trans.write_files(['html'],nodeof,'..\analysis_v0.2.html')