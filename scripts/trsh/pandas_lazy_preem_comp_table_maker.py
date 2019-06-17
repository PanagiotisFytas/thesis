import sys
import re
import pandas as pd
from IPython import embed

# versions = ["3.0","3.19", "4.9.6"]
versions = ["3.0","3.19", "4.3", "4.7", "4.9.6"]
failures = ["-", '-ASSERT_0']
methods = ["Nidhugg-BPOR", "Lazy-BPOR"]
#methods = ["VAN"]

force_failures = ["-DFORCE_FAILURE_%d"%i for i in [1,3,5]]
force_failures = ["-DFORCE_FAILURE_%d"%i for i in range(6)]
liveness_check = ["-DLIVENESS_CHECK_%d"%i for i in range(1,4)]

failures = failures + force_failures + liveness_check
attributes = ['time','traces','bound']
file_types = ['SB_%d.out', 'LB_%d.out']

def process_text(text):
	#print(text)
	times = re.findall('\W*Total wall-clock time:\D*(\d+\.\d+)', text)
	traces = re.findall('\W*Trace count:\D*(\d+)\W*\(also\W*(\d+)\W*sleepset blocked', text)
	errors = re.findall('(Error detected:)|(No errors were detected)',text)
	for time,t, e in zip(times,traces,errors):
		rtime = str(float(time))
		rt = str(int(t[0]) + int(t[1]))
		rer = "F" if len(e[0]) > len(e[1])  else "NF"
		yield [rtime,rt,rer]


header = pd.MultiIndex.from_product([versions,methods,attributes], names= ['ver.', 'method', ''])
df = pd.DataFrame(columns=header, index= failures)
df = df.where((pd.notnull(df)), None)

for i in range(2):
    for b in range(5):
        with open(file_types[i]%b, "r") as file:
            text = file.read()
            results = process_text(text)
            for v in versions:
                for f in failures:
                    cell = df.loc[f,(v,methods[i],'bound')]
                    value_to_store = next(results)
                    if cell == None or cell == 'NF':
                        if value_to_store[2] == 'F': value_to_store[2] = b
                        df.loc[f,(v,methods[i])] = value_to_store


#### PRINTING SECTION                        

l = ['c']
cols = len(versions) * len(methods)*len(attributes) + 1
col_form = '|' + '|'.join(cols*l) + '|'
df = df[:-3]
table = df.to_latex(column_format=col_form, multicolumn_format='c|')
table = table.split('\n')
table = [t for t in table if not "rule" in t]
table = '\n\\hline\n'.join(table[:-1])
print(table)