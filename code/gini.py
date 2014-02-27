#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv

(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

CANDIDATES = {
    'P80003338': 'Obama',
    'P80003353': 'Romney',
}

############### Set up variables
# TODO: declare datastructures
ginis = []
split_ginis = []
zips = {}

############### Read through files
for row in csv.reader(fileinput.input(), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue

    candidate_name = CANDIDATES[candidate_id]
    zip_code = row[ZIP_CODE][:5]
    if len(zip_code) != 5:
        continue
    ###
    # TODO: save information to calculate Gini Index
    ##/
    if zip_code in zips:
        zips[zip_code][candidate_name] += 1
    else:
        zips[zip_code] = {}
        for elem in CANDIDATES:
            if candidate_name == CANDIDATES[elem]:
                zips[zip_code][CANDIDATES[elem]] = 1
            else:
                zips[zip_code][CANDIDATES[elem]] = 0


###
# TODO: calculate the values below:
total_count = 0
obama_count = 0
romney_count = 0

# get total count of obama, romney and both.
for elem in zips:
    for candidate in zips[elem]:
        total_count += zips[elem][candidate]
        if candidate == 'Obama':
            obama_count += zips[elem][candidate]
        else:
            romney_count += zips[elem][candidate]

for elem in zips:
    # for each zip code partition
    obama = 0
    romney = 0
    for candidate in zips[elem]:
        if candidate == 'Obama':
            obama = zips[elem][candidate]
        else:
            romney = zips[elem][candidate]

    total_currentstep = obama + romney
    # calculate gini index at each step of iteration partitioning by zip code
    gini_currentstep = float(total_currentstep) * (1 - (float(obama) / total_currentstep) ** 2 - (float(romney) / total_currentstep) ** 2) / total_count + \
        (float(total_count) - total_currentstep) * (1 - ((float(obama_count) - obama) / (total_count - total_currentstep)) ** 2 - ((float(romney_count) - romney) / (total_count - total_currentstep)) ** 2) / total_count
    split_gini_currentstep = (1 - (float(obama) / total_currentstep) ** 2 - (float(romney) / total_currentstep) ** 2) * float(total_currentstep) / total_count
    ginis.append((elem, gini_currentstep))
    split_ginis.append((elem, split_gini_currentstep))

gini = min(ginis, key = lambda x: x[1])
split_gini = sum(pair[1] for pair in split_ginis)

# (zip code used for partition, minimum gini index)
print "Gini Index:", gini
# weighted average of the Gini Indexes 
print "Gini Index after split:", split_gini