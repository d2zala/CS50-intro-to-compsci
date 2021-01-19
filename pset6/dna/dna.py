from sys import argv, exit
import csv
import re

if len(argv) != 3:
    print("Missing command line arguments")
    exit(0)

str_counts = open(argv[1], "r")
dna_sequence = open(argv[2], "r").read()

reader1 = csv.reader(str_counts)
reader2 = csv.reader(dna_sequence)

strands = []
people = {}
for ind, row in enumerate(reader1):
    if ind == 0:
        strands = row[1:]
    else:
        people[row[0]] = row[1:]


final_numbers = []
for strand in strands:
    for row in reader2:
        for j in row:
            numofnucleotides = len(j)
for strand in strands:
    i = 0
    current_max = 0
    total_max = 0
    while i < len(dna_sequence):
        curr_seq = dna_sequence[i:i+len(strand)]
        if curr_seq == strand:
            current_max += 1
            if current_max >= total_max:
                total_max = current_max
            i += len(strand)
        else:
            current_max = 0
            i += 1
    final_numbers.append(total_max)

for person, num in people.items():
    index = 0
    while index < len(final_numbers):
        if int(num[index]) == final_numbers[index]:
            if index == len(final_numbers) - 1:
                print(f"{person}")
                exit(1)
            index += 1
        else:
            break

print("No match")

