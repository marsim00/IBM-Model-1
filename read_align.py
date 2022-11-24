import optparse
import sys

optparser = optparse.OptionParser()
optparser.add_option("-p", "--path", dest="path", default="alignment_outputs", help="Data filename prefix")
optparser.add_option("-f", "--file", dest="file", help="The file with alignments")
optparser.add_option("-x", "--suffix", dest="suffix", default="align", help="Suffix of the output file")
(opts, _) = optparser.parse_args()

filepath = "%s/%s.%s" % (opts.path, opts.file, opts.suffix)

def align_eval(path_to_file, start=0, stop=37):
    with open(path_to_file, "r") as file:
        lines = file.readlines()[start:stop]
    for line in lines:
        sys.stdout.write(line)

align_eval(filepath)