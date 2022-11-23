import os
from operator import itemgetter as ig
import math
from itertools import product
import sys
import time

class IBM_model:

    def __init__(self, source_file, target_file, data_path = "data", start = 0, stop = None, teta = None, e = 10, convergence = 100):

        """

        Args:
            source_file: source filename
            target_file: target filename
            data_path: folder with files (file prefix)
            start: index of the first sentence (for choosing a subset of sentences for training)
            stop: index of the last sentence (for choosing a subset of sentences for training)
                by default all sentences are chosen for training
            teta: initial uniform translation probability
            e: normalization parameter
            convergence: difference in perplexity between current and previous training step after which training stops
        """

        self.source, self.target = self.read_data(source_file, target_file, data_path, start, stop) #writing source and target sentences to variables
        self.set_align, self.set_source, self.set_target, self.all_tetas = self.init_step(teta) #writing set of alignments, set of words in source, set of words in target, dictionary with initial translation probabilities to variables
        self.em_tetas = self.EM_steps(e, convergence) #writing final translation probabilities to dictionary

    def read_data(self, source_file, target_file, data_path, start, stop):
        """

        Args:
            source_file: source filename
            target_file: target filename
            data_path: folder with files
            start: index of the first sentence (for choosing a subset of sentences for training)
            stop: index of the last sentence (for choosing a subset of sentences for training)

        Returns: lists with source and target sentences

        """

        # source English dataset. The 'NULL' element is added to the beginning of each sentence
        with open(os.path.join(data_path, source_file), "r", encoding="utf-8") as file:
            source = [line.strip().split() for line in ['NULL ' + sent for sent in file]][start:stop]

        # target French dataset
        with open(os.path.join(data_path, target_file), "r", encoding="utf-8") as file:
            target = [line.strip().split() for line in file][start:stop]

        return source, target

    def init_step(self, teta):
        """
        Args:
            teta: initial uniform translation probability

        Returns: set of alignments, set of words in source, set of words in target, dictionary with initial translation probabilities

        """

        print("Probabilities initialization")
        list_all_align = []

        # writing all possible target-source word pairs to the list
        for s in range(len(self.target)):
            list_all_align += list(product(self.target[s], self.source[s]))

        set_align = set(list_all_align)  # set of all possible target-source pairs
        set_target = set(map(ig(0), list_all_align))  # set of all words in target (target vocabulary)
        set_source = set(map(ig(1), list_all_align))  # set of all words in source (source vocabulary)

        # creating a dictionary with initial translation probabilities for all possible target-source word pairs (key - a tuple with a word pair, value - translation probability.
        # If teta = None (which is by default), then sets probability to the 1/number of words in a target vocabulary.
        all_tetas = {al: 1 / len(set_target) if not teta else teta for al in set_align}

        return set_align, set_source, set_target, all_tetas

    def EM_steps(self, e, convergence):
        """
        Trains a model by performing expectation maximization

        Args:
            e: normalization parameter
            convergence: difference in perplexity between current and previous training step after which training stops

        Returns: dictionary with final translation probabilities

        """

        last_log2_pplx = 0  # a variable to store the -log2(perplexity) from the previous iteration
        k = 0  # current iteration
        k_iterations = 3  # number of iterations to perform. Initially set to 3, but will eventually increase
        all_tetas = self.all_tetas
        min_float = sys.float_info[3] #minimal possible float

        print("Start training")
        start = time.time()

        while k < k_iterations:

            tetas_k = {}  # a dictionary to store translation probabilities for target-source word pairs at the current iteration

            # initialising counts to 0 in dictionaries
            counts_al = {ak: 0 for ak in self.set_align}  # word pair counts: key - a tuple with a target-source word pair
            counts_src = {sk: 0 for sk in self.set_source}  # source counts: key - a source word
            total_counts_tg = {tk: 0 for tk in self.set_target}  # total target counts: key - a target word

            for s in range(len(self.target)):  # for sentence in target sentences

                for i in self.target[s]:  # for word in a target sentence
                    total_counts_tg[i] = 0  # total target counts for the target word i = 0

                    for j in self.source[s]:  # for word in a source sentence
                        total_counts_tg[i] += all_tetas[i, j]  # sum total target counts for the target word i and a translation probability for the target-source word pair

                for i in self.target[s]:  # for word in a target sentence
                    for j in self.source[s]:  # for word in a source sentence
                        c = all_tetas[i, j] / total_counts_tg[i]  # normalizing a translation probability for a word pair by total target words count
                        counts_al[i, j] += c  # adding c to word pair counts
                        counts_src[j] += c  # adding c to source word counts

            for fe in counts_al:  # for target-source word pair in word pair counts
                tetas_k[fe] = counts_al[fe] / counts_src[fe[1]]  # translation probability for that pair = word pair counts/source word counts

            log2_pplx = 0  # initialization of a log2(perplexity) at a current step

            for s in range(len(self.target)):  # for s in a number of target sentences
                sent_prob = 1  # initialization of a sentence probability
                for i in self.target[s]:  # for target word in a target sentence
                    tetas_sum = 0  # initialization of a sum of translation probabilities
                    for j in self.source[s]:  # for source word in a source sentence
                        tetas_sum += tetas_k[i, j]  # summing up translation probabilities
                    sent_prob *= tetas_sum * e / len(self.source[s])  # multiplication of a sentence probability with an translation probability sum (here we use the law of distributivity)
                    if tetas_sum ==0: print("tetas_nul")
                    # and e/n (not n+1 as the NULL element is already added to source sentences)

                # probabilities very close to zero may be rounded to zero leading to the math.log2 throwing a ValueError
                try:
                    log2_pplx += math.log2(sent_prob)  # adding probability logarithms
                except ValueError:
                    log2_pplx += math.log2(min_float) #adding logarithm of the smallest possible probability if zero is passed

            log2_pplx = -log2_pplx  # make the logarithm positive (it's negative initially)
            if k >0:
                print("Iteration\t" + str(k+1) + "\tperplexity\t" + str(log2_pplx) + "\tdifference\t" + str(last_log2_pplx - log2_pplx))  # printing out the logarithm of perplexity for each iteration
            else:
                print("Iteration\t" + str(k + 1) + "\tperplexity\t" + str(log2_pplx))

            # if the difference between the -log2(perplexity) at the previous iteration and the current iteration is greater than the value of convergence parameter (100 by default),
            # then the model continues to iterate
            if k > 1 and last_log2_pplx - log2_pplx > convergence:
                k_iterations += 1
            k += 1

            all_tetas = tetas_k  # store translation probabilities obtained during current iteration to use them at the next iteration
            last_log2_pplx = log2_pplx  # store the -log2(perplexity) for the current iteration
             # if the error in logarithm calculation occured, stops after current iteration

        stop = time.time()

        print("Training finished in", (stop-start)/60, "minutes")
        # return translation probabilities
        return all_tetas

def IBM_decode(model:IBM_model, output_filename, tsd=0, output_path = "alignment_outputs"):

    """
    Writes best alignments

    Args:
        model: object of the IBM_model class
        output_filename: output filename
        tsd: threshold - the minimal value of a translation probability that should be exceeded to add the alignment.
        output_path: output folder

    """

    print("Start decoding")
    start = time.time()

    alignments = []  # a list to store alignments for the whole training set

    for s in range(len(model.target)):  # for sentence number in target sentences
        sentence_align = []  # a list to store alignments for each sentence

        for i in range(len(model.target[s])):  # for word number in a target sentence
            best_prob = tsd  # best probability initialization
            best_trans = ()  # a variable to store tuples with a pair of indices: of a target and a source word in a sentence

            for j in range(len(model.source[s])):  # for word number in a source sentence

                if model.em_tetas[model.target[s][i], model.source[s][j]] > best_prob:
                    best_prob = model.em_tetas[model.target[s][i], model.source[s][j]]
                    best_trans = (i, j - 1)  # 1 is subtracted from source word index, because the NULL element is at index 0

            # best translation is added to a list if best_trans is not empty (if all probabilities for the target word in a sentence <= tsd) and if the NULL element is not in the alignment
            if best_trans and best_trans[1] != -1:
                best_trans = str(best_trans[0]) + "-" + str(best_trans[1])  # tuple is reformated to a "i-j" form
                sentence_align.append(best_trans)

        alignments.append(sentence_align)
    stop = time.time()

    print("Decoding finished in", (stop - start) / 60, "minutes")

    print("Writing best alignments")
    with open(os.path.join(output_path, output_filename+".align"), "w") as file:
        for line in alignments:
            file.write(' '.join(line))
            file.write('\n')
    print("Finished")