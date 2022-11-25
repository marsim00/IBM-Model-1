# Implementation of the IBM Model 1 for Translation
Model is trained and tested for the translation from English to French.

## Project structure

The model itself is implemented in *IBM_utils.py* and is executed in *main.py*. 
*read_align.py* is used to read produced alignments for their further processing by evaluation scripts.

"data" folder contains the data for training (hansards.e - English sentences, hansards.f - French sentences, 100000 each) and testing (hansards.a - alignments of the first 37 sentences) (derived from Canadian Hansards, aligned by Ulrich Germann).

"alignment_outputs" folder contains output alignments for the implemented IBM model (three eng_fr_thr_\*\*\*.align for different thresholds), as well as outputs produced by Berkeley aligner using HMM (berkeley_hmm.align) and IBM Model 1 (berkeley_ibm.align)

"berkeley_config" folder contains configuration files for both HMM and IBM1 used in Berkeley Aligner (for the further comparison with my model).

"jhu" folder contains a simple aligner (*align*) and evaluation scripts (*check_alignments.py* and *score_alignments.py*) from the [homework](http://mt-class.org/jhu/hw1.html) for the Machine Translation class at John Hopkins University ([repository](https://github.com/xutaima/jhu-mt-hw/tree/master/hw2)). These scripts are used for the evaluation of my model and for its comparison with the simple aligner.

### Evaluation
Evaluation of alignments is performed by using evaluation.py, check-alignments.py and score-alignments.py. The output of the evaluation are precision, recall and AER estimates.

*Example*

Evaluation of a model with a 0.1 threshold.

Command for the Windows command line: python read_align.py -f eng_fr_thr_0.1 | python jhu/check-alignments | python jhu/score-alignments

## Evaluation Results and Model Comparison


