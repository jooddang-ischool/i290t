import csv
import pickle
import sys
import os 
import random

if os.path.exists('viz_dict.dic') == False:
	dic = {}
	with open(sys.argv[1], 'r') as data_csv:
		csvReader = csv.reader(data_csv, delimiter=',')
		for row in list(csvReader):
			if row[21] == '0':
				#not cancelled
				if (row[16] in dic.keys()) == False:
					dic[row[16]] = []
				if row[17] not in dic[row[16]]:
					dic[row[16]].append(row[17])

	pickle.dump(dic, open('viz_dict.dic', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

dic = pickle.load(open('viz_dict.dic', 'rb'))
f = open('vizData.json', 'w')
f.write('[\n')
for k in dic.keys():
	im = ['"flare.'+ x + '"' for x in dic[k]]
	im = str(im)
	im = im.replace('\'', '')
	f.write('{"name":"flare.' + k + '", "size":' + str(random.randint(400, 5000)) + ', "imports":' + im + '},\n')

f.write(']')
f.close()

#  {"name":"flare.CYS", "size":3390, "imports":[]},
# {"name":"flare.OGD", "size":2390, "imports":[]},