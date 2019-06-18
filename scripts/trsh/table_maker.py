'''
Creates a table that compares Naive-BPOR and BPOR.
Gets two parameters: The simple results and the BPOR results
'''
import sys
import re

versions = ["3.0","3.19", "4.9.6"]
methods = ["Naive-BPOR", "Classic-BPOR"]
#methods = ["VAN"]

#failures = ["-", "-DASSERT\_0"]
failures = ["-"]
force_failures = ["-DFORCE\_FAILURE\_" + str(i) for i in [1,3,5]]
liveness_check = ["-DLIVENESS\_CHECK\_" + str(i) for i in range(1,4)]

failures = failures + force_failures + liveness_check
def process_text(text):
	'''
	@params: text file with traces
	@returns: a list of tuples containing the number of traces, time and whether the error was found.
	'''
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



if __name__ == "__main__":
	with open(sys.argv[1],"r") as file:
		van_text = file.read()
	van_results = process_text(van_text)
	# print((van_results))
	with open(sys.argv[2], "r") as file:
		pb_text = file.read()

	pb_results = process_text(pb_text)
	#print(pb_results)
	#print(len(pb_results))
	results = list(zip(van_results,pb_results))
	#print(len(results))
	i = 0
	# The results for each version are together in the list.
	for v in versions:
		for f_i,f in enumerate(failures):
                    f_r = " & ".join([y for x in results[i] for y in x])
                    failures[f_i] = failures[f_i] + " & " + f_r
                    #print(v,failures[f_i])
                    i+=1

	columns = failures[0].count("&")
	#print(columns)
	columns = "|c|" + columns*"c|"
	#print(columns)

	multicolumn = "\\multicolumn{1}{|c|}{ver:}"
	for v in versions:
		multicolumn += " & \\multicolumn{6}{c|}{" + v + "}"

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
