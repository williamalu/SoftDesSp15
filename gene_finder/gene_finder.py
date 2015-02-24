# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: William Lu

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###

def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    >>> get_complement('T')
    'A'
    >>> get_complement('G')
    'C'
    """
    #added last two doctests for completeness - original doctests don't reflect their "flipped" counterparts
    if nucleotide is 'A':
        return 'T'
    elif nucleotide is 'C':
        return 'G'
    elif nucleotide is 'T':
        return 'A'
    elif nucleotide is 'G':
        return 'C'
    # read http://stackoverflow.com/questions/2988017/string-comparison-in-python-is-vs. Know that is and == are not always the same, and that in some cases the two comparisons will yield different answers. 

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    #no new doctests added - all letters and their pairs are sufficiently tested for already
    res = []
    for c in dna:
        res.append(get_complement(c))
    delimiter = ''
    res = delimiter.join(res)
    #you can take an empty string and just do res += get_complement(c). Converting between string and list is something you can skip.
    return res[::-1] #extended slice allows for third argument, which tells the slice the "step" to slice in

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    >>> rest_of_ORF("CAATGCCC")
    'CAATGCCC'
    >>> rest_of_ORF("ATG")
    'ATG'
    """
    #added doctest that tests a situation with a start codon in the middle of the sequence
    #added doctest that only has a start codon to make sure the code won't break in that situation
    orig = dna[:]
    stopcodons = ['TAG','TAA','TGA']
    res = []
    for i in range(0, len(dna), 3):
        if dna[i:(i+3)] in stopcodons:
            return dna[0:i] #the 0 is unnessecary
    return dna


def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe("AAAAAAAAAAAAAAAAAAA")
    []
    """
    #added a doctest to see what happens when a dna sequence has no start codon in any frame
    orig = dna[:]
#this orig stuff doesn't look like it's being used
    res = []
    startcodon = 'ATG'
    stopcodons = ['TAG','TAA','TGA']

    index = 0
    while index < (len(dna) - 2):
        if dna[index:(index+3)] in startcodon: #I would use == startcodon. 
            dnachunk = rest_of_ORF(dna[index:])
            res.append(dnachunk)
            index += len(dnachunk)
        else:
            index += 3
    return res

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    #no doctest added because the current doctest already tests for orfs in all 3 possible frames
    res = []
    res += find_all_ORFs_oneframe(dna)
    res += find_all_ORFs_oneframe(dna[1:])
    res += find_all_ORFs_oneframe(dna[2:])
    return res

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    #no doctest added because if find_all_ORFs works correctly, this function will work correctly
    res = []
    reversedna = get_reverse_complement(dna)
    res += find_all_ORFs(dna)
    res += find_all_ORFs(reversedna)
    return res


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    >>> longest_ORF("AAAAAAAAAAAAAAAAAAA")
    ''
    """
    #added doctest for situation where there is no orf to be found
    if find_all_ORFs_both_strands(dna) == []:
        return ''
    return max(find_all_ORFs_both_strands(dna), key=len)


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    #doctests not possible with this func, easier to use print statements to manually check if function works properly
    orfs = []
    for i in range(num_trials):
        shuffled_dna = shuffle_string(dna)
        orfs.append(longest_ORF(shuffled_dna))
    #print orfs
    #print len(max(orfs, key=len))
    return len(max(orfs, key=len))

salmonella_dna = "GGATCCGACAGGGAAAATCGTTGAGCGTTTTACCCCTGAAGTGGCGCCGATTAGCGAAGAACGCGTTATTGATGTCGCACCGCCGTCTTACGCTTCACGCGTTGGCGTCCGTGAACCGCTGATTACCGGTGTGCGCGCGATTGACGGGTTATTGACCTGTGGCGTAGGCCAGCGAATGGGCATTTTTGCCTCCGCAGGATGCGGTAAGACCATGCTGATGCATATGCTGATCGAGCAAACGGAGGCGGATGTCTTTGTTATCGGTCTTATCGGTGAACGAGGCCGTGAGGTCACTGAATTCGTGGATATGTTGCGCGCTTCGCATAAGAAAGAAAAATGCGTGCTGGTTTTTGCCACTTCCGATTTCCCCTCGGTCGATCGCTGCAATGCGGCGCAACTGGCGACAACCGTAGCGGAATATTTTCGCGACCAGGGAAAACGGGTCGTGCTTTTTATCGATTCCATGACCCGTTATGCGCGTGCTTTGCGAGACGTGGCACTGGCGTCGGGAGAGCGTCCGGCTCGTCGAGGTTATCCCGCCTCCGTATTCGATAATTTGCCCCGCTTGCTGGAACGCCCAGGGGCGACCAGCGAGGGAAGCATTACTGCCTTTTATACGGTACTGCTGGAAAGCGAGGAAGAGGCGGACCCGATGGCGGATGAAATTCGCTCTATCCTTGACGGTCACCTGTATCTGAGCAGAAAGCTGGCCGGGCAGGGACATTACCCGGCAATCGATGTACTGAAAAGCGTAAGCCGCGTTTTTGGACAAGTCACGACGCCGACACATGCTGAACAGGCATCTGCCGTGCGTAAATTAATGACGCGTTTGGAAGAGCTCCAGCTTTTCATTGACTTGGGAGAATATCGTCCTGGCGAAAATATCGATAACGATCGGGCGATGCAGATGCGGGATAGCCTGAAAGCCTGGTTATGCCAGCCGGTAGCGCAGTATTCATCCTTTGATGACACGTTGAGCGGTATGAATGCATTCGCTGACCAGAATTAAAGTATTGCAGCGGCGCTGTACGGTATTTCATTCACAGTGTGAGTCGATATTACTTCGCTATCAGGATGAGGACCGCGGGCTGCAGGCCGAGGAGGAGGCGATCCTTGAACAAATAGCGGGTCTGAAATTGTTATTAGATACGCTGCGTGCAGAAAACAGACAGCTCAGTCGTGAGGAAATTTATACGTTATTACGTAAGCAGTCTATTGTTCGCCGGCAGATAAAAGATTTAGAACTCCAGATTATACAAATTCAGGAAAAACGGAGCGAGCTGGAAAAGAAAAGGGAAGAGTTTCAGAAAAAAAGTAAATATTGGTTGCGCAAAGAAGGGAACTATCAACGCTGGATAATCCGTCAGAAAAGATTCTATATCCAGCGAGAGATACAGCAGGAAGAGGCCGAGTCAGAGGAGATAATTTAATGGGCGATGTGTCAGCTGTCAGTTCATCCGGGAACATTTTACTGCCGCAGCAGGATGAGGTTGGCGGTTTATCAGAAGCATTAAAAAAAGCGGTGGAAAAACATAAGACAGAATATTCCGGTGATAAAAAAGATCGCGACTATGGCGATGCTTTCGTAATGCATAAAGAAACGGCTTTACCGTTATTACTGGCGGCATGGCGACATGGCGCGCCAGCGAAATCAGAACATCACAATGGCAACGTTTCTGGTCTGCATCATAACGGAAAAAGCGAACTCAGGATTGCTGAAAAACTGTTGAAAGTCACTGCTGAAAAATCTGTCGGTTTGATCTCTGCGGAGGCCAAAGTAGATAAATCCGCAGCGTTGCTATCGTCTAAAAATAGGCCGTTAGAAAGCGTAAGCGGTAAAAAATTATCTGCTGATTTAAAAGCTGTGGAATCCGTTAGTGAAGTAACCGATAACGCCACGGGAATCTCTGACGATAATATCAAGGCATTGCCTGGGGATAATAAAGCCATCGCGGGCGAAGGCGTTCGTAAAGAGGGCGCGCCGCTGGCGCGGGATGTCGCACCTGCCCGAATGGCCGCAGCCAATACCGGTAAGCCTGAAGATAAAGATCATAAAAAGGTTAAAGATGTTTCTCAGCTTCCGCTGCAACCAACCACTATCGCCGATCTTAGCCAATTAACCGGCGGCGATGAAAAAATGCCTTTAGCGGCGCAATCAAAGCCGATGATGACTATTTTTCCCACTGCCGATGGCGTGAAAGGAGAGGATAGCTCGCTGACTTACCGTTTTCAGCGCTGGGGAAATGACTATTCCGTCAATATTCAGGCGCGGCAAGCAGGGGAGTTTTCGTTAATACCGTCAAATACGCAGGTTGAACATCGTTTGCATGATCAATGGCAAAACGGTAATCCCCAGCGCTGGCACCTGACGCGAGACGATCAACAAAATCCGCAGCAGCAACAGCACAGACAGCAATCTGGCGAGGAGGATGACGCCTGATGTCATTGCGTGTGAGACAGATTGATCGTCGCGAATGGCTATTGGCGCAAACCGCGACAGAATGCCAGCGCCATGGCCGGGAAGCGACGCTGGAATATCCGACGCGACAGGGAATGTGGGTTCGGTTGAGCGATGCAGAAAAACGGTGGTCGGCCTGGATTAAACCTGGGGACTGGCTTGAGCATGTCTCTCCCGCTCTGGCTGGGGCGGCGGTTTCTGCTGGCGCTGAGCACCTGGTCGTTCCCTGGCTTGCTGCAACAGAGCGACCGTTTGAGTTGCCCGTGCCGCATTTGTCCTGTCGGCGTTTATGCGTAGAGAACCCCGTACCGGGAAGCGCGCTGCCGGAAGGGAAATTGTTGCACATTATGAGCGATCGGGGCGGCCTGTGGTTTGAGCATCTTCCTGAACTGCCTGCAGTCGGGGGCGGCAGGCCGAAAATGCTGCGTTGGCCGTTGCGCTTTGTAATCGGTAGCAGTGATACGCAGCGTTCGTTGCTGGGCCGAATCGGGATCGGAGATGTACTCCTGATTCGTACTTCCCGTGCGGAAGTTTATTGCTACGCGAAAAAGTTAGGTCATTTCAACCGTGTTGAAGGGGGAATTATTGTGGAAACGTTAGATATTCAACATATCGAAGAAGAAAATAATACAACTGAAACTGCAGAAACTCTGCCTGGCTTGAATCAATTGCCCGTCAAACTGGAATTTGTTTTGTATCGTAAGAACGTTACCCTCGCCGAACTCGAAGCCATGGGGCAGCAACAGCTATTATCACTGCCGACCAATGCTGAACTTAACGTTGAAATTATGGCGAATGGTGTTTTGCTGGGTAATGGCGAACTGGTACAGATGAATGACACCTTAGGCGTTGAGATCCATGAATGGCTGAGCGAGTCTGGTAATGGGGAATGATATCTCATTAATTGCCTTACTGGCATTTTCCACCCTGTTGCCATTTATTATTGCGTCAGGAACCTGTTTCGTTAAATTTTCTATTGTATTTGTCATGGTGCGTAACGCCCTGGGATTACAGCAGATACCTTCAAATATGACGCTTAACGGCGTCGCATTGCTGCTTTCTATGTTTGTTATGTGGCCCATAATGCATGATGCCTACGTCTATTTTGAGGACGAAGATGTCACCTTTAATGATATTTCATCATTAAGTAAACACGTTGATGAAGGTCTGGATGGTTATCGCGATTATCTGATCAAATATTCAGATCGCGAGTTAGTTCAGTTTTTTGAAAACGCGCAACTGAAGCGTCAGTATGGAGAAGAGACCGAGACGGTAAAGCGTGACAAAGATGAAATTGAAAAACCTTCAATATTTGCGTTATTACCTGCTTATGCGCTGAGCGAAATAAAAAGCGCGTTTAAAATTGGTTTTTATCTTTATTTGCCCTTTGTCGTCGTCGACCTGGTGGTATCCAGCGTGCTACTGGCGCTGGGGATGATGATGATGAGTCCGGTGACGATATCTACACCTATTAAGCTGGTGCTTTTTGTCGCGCTTGATGGCTGGACCTTACTGTCTAAGGGATTGATATTACAGTATATGGACATTGCAACATGACATCATTACGAGACGGGATAGTTAAATGGATGATTTAGTGTTTGCAGGTAATAAGGCGCTCTATCTTGTTTTGATCCTGTCAGGGTGGCCGACGATTGTCGCAACGATTATCGGCCTCCTGGTAGGGTTATTCCAGACGGTAACGCAATTACAGGAACAGACGCTGCCTTTTGGCATTAAATTACTTGGCGTGTGTTTATGCTTGTTTTTACTGTCTGGCTGGTATGGCGAAGTTTTACTCTCTTACGGGCGTCAGGTGATATTCCTGGCGTTGGCTAAGGGGTAAAAAATGTTTTACGCGTTGTACTTTGAAATTCATCACCTGGTTGCGTCTGCGGCGCTAGGGTTTGCTCGCGTGGCGCCGATTTTTTTCTTCCTGCCGTTTTTGAATAGCGGGGTATTAAGCGGTGCGCCGAGAAACGCCATTATCATCCTGGTGGCATTGGGAGTATGGCCGCATGCATTGAACGAGGCGCCGCCGTTTTTATCGGTGGCGATGATCCCGTTAGTTCTGCAAGAAGCGGCGGTAGGCGTCATGCTGGGCTGTCTGCTGTCATGGCCTTTTTGGGTTATGCATGCGCTGGGTTGTATTATCGATAACCAGCGAGGGGCAACGCTAAGTAGTAGTATCGATCCGGCAAACGGTATTGATACCTCGGAAATGGCTAATTTCCTGAATATGTTTGCCGCTGTCGTTTATTTACAAAACGGCGGTCTGGTCACGATGGTTGACGTGTTAAATAAAAGCTATCAGCTATGCGATCCGATGAACGAGTGCACGCCTTCATTACCGCCGCTATTAACGTTTATTAATCAGGTGGCTCAAAACGCCTTGGTTCTGGCCAGTCCGGTGGTATTAGTGCTGTTGCTGTCAGAAGTATTCCTGGGTTTATTGTCGCGCTTTGCTCCGCAAATGAACGCTTTTGCGATTTCACTGACGGTAAAAAGCGGTATTGCCGTTTTAATTATGCTGCTTTATTTCTCTCCGGTACTACCGGACAATGTACTGCGACTCTCTTTCCAGGCCACAGGGTTAAGCAGTTGGTTTTACGAGCGAGGGGCGACGCATGTCCTCGAATAAAACAGAAAAACCGACTAAAAAACGGCTGGAAGACTCCGCTAAAAAAGGCCAGTCATTTAAAAGTAAAGATCTCATTATCGCCTGCCTGACGCTGGGAGGAATTGCCTATCTGGTGTCGTATGGCTCATTTAATGAGTTTATGGGGATAATTAAGATCATTATTGCGGATAATTTTGATCAGAGCATGGCTGACTACAGTTTGGCCGTTTTTGGGATAGGGTTAAAATATCTGATTCCATTTATGCTGCTCTGCTTAGTGTGTTCCGCATTACCGGCGTTATTACAGGCCGGTTTTGTGCTGGCGACAGAAGCATTAAAGCCTAATTTATCGGCGTTAAACCCGGTAGAAGGGGCAAAAAAACTTTTTAGTATGCGCACGGTTAAAGATACGGTCAAAACCCTACTGTATCTCTCATCCTTTGTGGTGGCCGCCATCATTTGCTGGAAGAAATATAAGGTTGAAATCTTTTCTCAGCTAAATGGCAATATTGTAGGTATTGCCGTCATTTGGCGTGAACTTCTCCTCGCATTGGTATTAACTTGCCTTGCTTGCGCATTGATTGTCTTATTATTGGATGCTATTGCGGAATATTTCCTGACCATGAAAGATATGAAAATGGATAAGGAAGAAGTGAAGCGTGAAATGAAGGAGCAGGAAGGGAACCCAGAGGTTAAATCTAAAAGACGTGAAGTTCATATGGAAATTCTGTCTGAACAGGTGAAATCTGATATTGAAAACTCACGCCTGATTGTTGCCAACCCCACGCATATTACGATCGGGATTTATTTTAAACCCGAATTGATGCCGATTCCGATGATCTCGGTGTATGAAACGAATCAGCGCGCACTGGCCGTCCGCGCCTATGCGGAGAAGGTTGGCGTACCTGTGATCGTCGATATCAAACTGGCGCGCAGTCTTTTCAAAACCCATCGCCGTTATGATCTGGTGAGTCTGGAAGAAATTGATGAAGTTTTACGTCTTCTGGTTTGGCTGGAAGAGGTAGAAAACGCGGGCAAAGACGTTATTCAGCCACAAGAAAACGAGGTACGGCATTGAGCCGCGTAAGGCAGTAGCGATGTATTCATTGGGCGTTTTTTGAATGTTCACTAACCACCGTCGGGGTTTAATAACTGCATCAGATAAACGCAGTCGTTAAGTTCTACAAAGTCGGTGACAGATAACAGGAGTAAGTAATGGATTATCAAAATAATGTCAGCGAAGAACGTGTTGCGGAAATGATTTGGGATGCCGTTAGTGAAGGCGCCACGCTAAAAGACGTTCATGGGATCC"
#longest_ORF_noncoding(salmonella_dna, 4)

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    #no doctest added - the second doctest already covers the case where the dna is not in triplets
    index = 0
    aa_string = ''
    #should use a for loop here instead.
    while index < (len(dna) - 2):
        aa_string += aa_table[dna[index:index+3]]
        index += 3
    return aa_string

def gene_finder(dna):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
                
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    #doctests not possible due to random nature of longest_orf_noncoding
    threshold = longest_ORF_noncoding(dna, 1500)
    all_orfs = find_all_ORFs_both_strands(dna)
    aa_seqs = []
    for orf in all_orfs:
        if len(orf) > threshold:
            aa_seqs.append(coding_strand_to_AA(orf))
    return aa_seqs

if __name__ == "__main__":
    import doctest
    doctest.testmod()
