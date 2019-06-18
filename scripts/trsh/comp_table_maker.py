'''
Compares DPOR with BPOR by finding the lowest branch limit that can find the bug. It checks all the files SB_i.out ( i in [0..5] )
'''
import sys
import re

# versions = ["3.0","3.19", "4.3", "4.7", "4.9.6"]
versions = ["3.0","3.19", "4.9.6"]
failures = ["-"]
methods = ["Source-DPOR", "Classic-BPOR"]
#methods = ["VAN"]

force_failures = ["-DFORCE\_FAILURE\_" + str(i) for i in [1,3,5]]
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



if __name__ == "__main__":
	file = open(sys.argv[1],"r")
	dpor_text = file.read()
	file.close()

	dpor_results = process_text(dpor_text)
	#print(len(van_results))

	file_name = "outputs/PB_%d.out"
	file = open(file_name%0, "r")
	pb_text = file.read()
	file.close()
	pb_results = process_text(pb_text)

	for i,_ in enumerate(pb_results):
		if pb_results[i][2] == "F" :
			pb_results[i] = (pb_results[i][0], pb_results[i][1], "0")

	for b in range(1,5):
		file = open(file_name%b, "r")
		pb_text = file.read()
		file.close()
		temp_results = process_text(pb_text)
		for i,_ in enumerate(temp_results):
			if(pb_results[i][2] == "NF" and temp_results[i][2] == "F"):
				pb_results[i] = (temp_results[i][0], temp_results[i][1], str(b))

	#print(pb_results)
	#print(len(pb_results))
	results = list(zip(dpor_results,pb_results))
	#print(len(results))
	i = 0
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

	headers = "  "

	for v in versions:
		for m in methods:
			if m == "DPOR":
				method_mult += " & \\multicolumn{3}{c|}{" + m + "}"
				headers += " & traces & time & error" 
			else:
				method_mult += " & \\multicolumn{3}{c|}{" + m + "}"
				headers += " & traces & time & bound" 

	method_mult += " \\\\"
	headers += " \\\\"


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
