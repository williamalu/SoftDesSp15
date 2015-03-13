class DNASequence(object):
    """ Represents a sequence of DNA """
    def __init__(self, nucleotides):
        """ constructs a DNASequence with the specified nucleotides.
             nucleotides: the nucleotides represented as a string of
                          capital letters consisting of A's, C's, G's, and T's """
        self.sequence = nucleotides
 
    def __str__(self):
        """ Returns a string containing the nucleotides in the DNASequence
        >>> seq = DNASequence("TTTGCC")
        >>> print seq
        TTTGCC
        """
        return self.sequence

    def get_reverse_complement(self):
        """ Returns the reverse complement DNA sequence represented
            as an object of type DNASequence

            >>> seq = DNASequence("ATGC")
            >>> rev = seq.get_reverse_complement()
            >>> print rev
            GCAT
            >>> print type(rev)
            <class '__main__.DNASequence'>
        """
        seq_complement = []

        for a in self.sequence:
            if a is 'A':
                seq_complement.append('T')
            elif a is 'C':
                seq_complement.append('G')
            elif a is 'T':
                seq_complement.append('A')
            elif a is 'G':
                seq_complement.append('C')

        delimiter = ''
        rev = delimiter.join(seq_complement)
        rev = rev[::-1]

        return DNASequence(rev)

    def get_proportion_ACGT(self):
        """ Computes the proportion of nucleotides in the DNA sequence
            that are 'A', 'C', 'G', and 'T'
            returns: a dictionary where each key is a nucleotide and the
                corresponding value is the proportion of nucleotides in the
            DNA sequence that are that nucleotide.
            (NOTE: this doctest will not necessarily always pass due to key
                    re-ordering don't worry about matching the order)
        >>> seq = DNASequence("AAGAGCGCTA")
        >>> d = seq.get_proportion_ACGT()
        >>> print (d['A'], d['C'], d['G'], d['T'])
        (0.4, 0.2, 0.3, 0.1)
        """
        count = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
        for a in self.sequence:
            count[a] += float(1)

        total = len(self.sequence)
        
        proportion = {}
        for key in count:
            proportion[key] = count[key] / total

        return proportion

if __name__ == '__main__':
    import doctest
    doctest.testmod()
