'''
Creates a table from one result file.
'''
import sys
import re

versions = ["3.0","3.19", "4.3", "4.7", "4.9.6"]
failures = ["-", "-DASSERT\_0"]
methods = ["DPOR"]
#methods = ["VAN"]

force_failures = ["-DFORCE\_FAILURE\_" + str(i) for i in range(1,7)]
liveness_check = ["-DLIVENESS\_CHECK\_" + str(i) for i in range(1,4)]

failures = failures + force_failures + liveness_check
def process_text(text):
	#print(text)
	times = re.findall('\W*Total wall-clock time:\D*(\d+\.\d+)', text)
	traces = re.findall('\W*Trace count:\D*(\d+)\W*\(also\W*(\d+)\W*sleepset blocked', text)
	errors = re.findall('(Error detected:)|(No errors were detected)',text)
	times = [str(float(t)) for t in times]
	traces = [str(int(t[0]) + int(t[1])) for t in traces]
	errors = ["F" if len(e[0]) > len(e[1])  else "NF" for e in errors]
	results = list(zip(traces,times,errors))
	#print(results)
	return results


if __name__ = "__main__":

	file = open(sys.argv[1], "r")
	pb_text = file.read()
	file.close()

	pb_results = process_text(pb_text)

	results = pb_results
	#print(len(results))

	i = 0
	for v in versions:
		for f_i,f in enumerate(failures):
			f_r = " & ".join([x for x in results[i]]) 
			failures[f_i] = failures[f_i] + " & " + f_r
			#print(v,failures[f_i])
			i+=1

	columns = failures[0].count("&")
	#print(columns)
	columns = "|c|" + columns*"c|"
	#print(columns)

	multicolumn = "\\multicolumn{1}{|c|}{ver:}"
	for v in versions:
		multicolumn += " & \\multicolumn{3}{c|}{" + v + "}"

	multicolumn += " \\\\"

	method_mult = "\\multicolumn{1}{|c|}{method:}"
	for v in versions:
		for m in methods:
			method_mult += " & \\multicolumn{3}{c|}{" + m + "}"

	method_mult += " \\\\"

	headers = "  " + len(methods)*len(versions)*" & traces & time & error" + " \\\\"

	#[print(f) for f in failures]

	#print("\\begin{center}")
	print("\\begin{tabular}{" + columns + "}")
	print("\\hline")
	print(multicolumn)
	print("\\hline")
	print(method_mult)
	print("\\hline")
	print(headers)
	print("\\hline")
	for f in failures:
		print(f + " \\\\")
		print("\\hline")

	print("\\end{tabular}")
	#print("\\end{center}")
