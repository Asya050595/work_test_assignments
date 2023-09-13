from Bio.SeqUtils import MeltingTemp as mt
import pandas as pd
import primer3

with open("PATH", 'r') as f:
    file = f.readlines()

name = None
sequences = dict()
for line in file:
    line = line.rstrip()
    if line[0] == '>':
        name = line[1:]
        sequences[name] = ''
    else:
        sequences[name] = sequences[name] + line
df = pd.DataFrame.from_dict(sequences, orient='index', columns=['Sequence'])
df["length"] = df["Sequence"].apply(len)
my_sequence_list = df['Sequence'].values[:]

for i in my_sequence_list:
    print(i, mt.Tm_Wallace(i, strict=False), file=open('PATH + NAME', 'a'))
    print(i, primer3.bindings.calc_homodimer(i), file=open('PATH + NAME', 'a'))
    print(i, primer3.bindings.calc_hairpin(i), file=open('PATH + NAME', 'a'))
