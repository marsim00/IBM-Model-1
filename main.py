"""
Created at 17:15 22.11.2022 using PyCharm

@author: Mariam Bangura
@e-mail: maba00008@stud.uni-saarland.de

"""

from IBM_utils import *

thresholds = [0.1, 0.2, 0.4] #thresholds for decoding (alignment is added if its probability excedes the threshold)

trained_model = IBM_model(source_file="hansards.e", target_file="hansards.f", data_path = "data", start = 0, stop = None, teta = None, e = 10, convergence = 1000)

for t in thresholds:
    #files with alignments are written for each threshold in the thresholds lists
    IBM_decode(model=trained_model, output_filename="eng_fr_thr_"+str(t), tsd=t, output_path = "alignment_outputs")