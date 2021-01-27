import csv
from sys import argv, exit

if len(argv) < 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit()

#Get the dna sample
with open(argv[2]) as sequences:
    sample = csv.reader(sequences)
    for row in sample:
        dnasample = row

#Convert dna sample to string
dnasample = str(dnasample[0])

#Get the database
sequences = {}
dnadata = {}
track = []
with open(argv[1]) as database:
    data = csv.reader(database)
    for row in data:
        dnadata[row[0]] = row[1:]
        
#Extract the dna that want to be tracked
for dna in dnadata["name"]:
    track.append(dna)
    
for dna in track:
        sequences[dna] = 1
        
# Start counting
for key in sequences:
    bigtmp = 0
    tmp = 0
    for i in range(len(dnasample)):
        #Start again from 0
        tmp = 0

        #Start counting the counters
        if dnasample[i: i + len(key)] == key:
            while dnasample[i - len(key): i] == dnasample[i: i + len(key)]:
                tmp += 1
                i += len(key)

            #choosing the biggest counter
            if tmp > bigtmp:
                bigtmp = tmp
                
    #saving counter
    sequences[key] += bigtmp

#start searching the guy
with open(argv[1], newline='') as peoplefile:
    people = csv.DictReader(peoplefile)
    for person in people:
        match = 0
        for dna in sequences:
            if sequences[dna] == int(person[dna]):
                match += 1
        if match == len(sequences):
            print(person['name'])
            exit()
        else:
            print("No match")
    
