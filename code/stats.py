#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv

candidateIds = {}
amount = []


for row in csv.reader(fileinput.input(), delimiter='|'):
    # store all candidate IDs
    trimmedId = row[16].strip()
    if len(trimmedId) > 0:
        candidateIds.setdefault(trimmedId, []).append(float(row[14]))
    amount.append(float(row[14]))

def get_square_data(_list, _mean):
    squareData = 0.0
    for elem in _list:
        squareData += (elem - _mean) ** 2
    return squareData

#sort the amount
sorted_amount = sorted(amount)
total = sum(sorted_amount)
minimum = sorted_amount[0]
maximum = sorted_amount[-1]
mean = total / len(sorted_amount)
##### Print out the stats
print "Total: %s" % total
print "Minimum: %s" % minimum
print "Maximum: %s" % maximum
print "Mean: %s" % mean
print "Median: %s" % (sorted_amount[len(sorted_amount) / 2])
# square root can be calculated with N**0.5
# squareData = 0.0
# for elem in sorted_amount:
#     squareData += (elem - mean) ** 2
squareData = get_square_data(sorted_amount, mean)
sd = (squareData / len(sorted_amount)) ** 0.5
print "Standard Deviation: %s" % sd

##### Comma separated list of unique candidate ID numbers
print "Candidates: "
i = 0
printable = ''
for elem in candidateIds.keys():
    printable += elem + ', '
    i += 1
    if i % 10 == 0:
        print printable
        printable = ''
print printable

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    ###
    # TODO: replace line below with the actual calculations
    norm = (value - minimum) / (maximum - minimum)
    ###/

    return norm

##### Normalize some sample values
# print "Min-max normalized values: %r" % map(minmax_normalize, sorted_amount)


print "\n\n=======================================\n\n"
print "Extra Credit problems"

for elem in candidateIds.keys():
    sorted_per_candi = sorted(candidateIds[elem])
    sum_per_candi = sum(sorted_per_candi)
    min_per_candi = sorted_per_candi[0]
    max_per_candi = sorted_per_candi[-1]
    mean_per_candi = sum_per_candi / len(sorted_per_candi)
    print "Candidate ID: ", elem
    print "Minimum: ", min_per_candi
    print "Maximum: ", max_per_candi
    print "Mean: ", mean_per_candi
    print "Median: ", (sorted_per_candi[len(sorted_per_candi) / 2])
    squareData = get_square_data(sorted_per_candi, mean_per_candi)
    print "Standard Deviation: ", ((squareData / len(sorted_per_candi)) ** 0.5)
    print "z-score: ", ((sum_per_candi - mean) / sd)
    print " "