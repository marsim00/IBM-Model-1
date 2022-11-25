# IBM Model 1
Implementation of the statistical machine translation algorithm IBM Model 1. Model was trained for the translation from English to French.

## Project structure

The model itself is implemented in *IBM_utils.py* and is executed in *main.py*. 
*read_align.py* is used to read produced alignments for their further processing by evaluation scripts.

"data" folder contains the data for training (hansards.e - English sentences, hansards.f - French sentences, 100000 each) and testing (hansards.a - alignments of the first 37 sentences) (derived from Canadian Hansards, aligned by Ulrich Germann).

"alignment_outputs" folder contains output alignments for the implemented IBM model (three eng_fr_thr_\*\*\*.align for different thresholds), as well as outputs produced by Berkeley aligner using HMM (berkeley_hmm.align) and IBM Model 1 (berkeley_ibm.align). "produced_alignments.txt" contains examples of alignments produced by different models.

"berkeley_config" folder contains configuration files for both HMM and IBM1 used in Berkeley Aligner (for the further comparison with my model).

"jhu" folder contains a simple aligner (*align*) and evaluation scripts (*check_alignments.py* and *score_alignments.py*) from the [homework](http://mt-class.org/jhu/hw1.html) for the Machine Translation class at John Hopkins University ([repository](https://github.com/xutaima/jhu-mt-hw/tree/master/hw2)). These scripts are used for the evaluation of my model and for its comparison with the simple aligner.

## Training and Decoding
For training and decoding execute the main.py, having preliminary changed model parameters and decoding parameters if needed.

## Evaluation
Evaluation of alignments is performed by using evaluation.py, check-alignments.py and score-alignments.py. The output of the evaluation are precision, recall and alignment error rate (AER) estimates.

*Example*

Evaluation of a model with a 0.2 threshold.

**Command for the Windows command line**: *python read_align.py -f eng_fr_thr_0.2 | python jhu/check-alignments | python jhu/score-alignments*

## Evaluation Results and Model Comparison

All models were trained on the whole data set (100000 sentences). The IBM model (current implementation) was trained with normalization parameter e = 10 and until convergence rate reached 1000. That took 21 iterations of expectation maximization step with duration of approximately 40 minutes. 


|                  |     IBM (0.1)    |     IBM (0.2)    |     IBM (0.4)    |     Berkeley IBM    |     Berkeley HMM    |     Simple aligner (Dice 0.8)    |
|------------------|------------------|------------------|------------------|---------------------|---------------------|----------------------------------|
|     Precision    |     0.667        |     0.733        |     0.768        |     0.764           |     0.882           |     0.460                        |
|     Recall       |     0.701        |     0.639        |     0.459        |     0.772           |     0.935           |     0.251                        |
|     AER          |     0.320        |     0.311        |     0.415        |     0.233           |     0.099           |     0.670                        |

<sub>In brackets decoding thresholds are indicated: alignment was added if its probability exceded the threshold (IBM model) or Dice coefficient (simple aligner).</sub>

The best IBM model performance is achieved with the threshold 0.2 (although presicion is lower than for a model with a 0.4 threshold, AER is much lower).
All models are outperformed by Berkeley HMM, having the highest precision and recall and the lowest AER.

Examples of alignments produced by different models are provided in alignment_outputs/produced_alignments.txt

## References

[Adam Lopez. Word Alignment and the Expectation-Maximization Algorithm](http://mt-class.org/jhu/assets/papers/alopez-model1-tutorial.pdf)

[Philipp Koehn (2022). IBM Model 1 and the EM Algorithm](http://mt-class.org/jhu/slides/lecture-ibm-model1.pdf)

## Note

The project is created as a homework for the Computational Linguistics course at Language Science & Technology program, Saarland University. 
