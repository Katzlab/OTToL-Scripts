######################################################################################
#This script finds taxa that do not have dependents that are genera or species (or subgenera
#or subspecies) by following these up to their parents and taking those that aren't in any paths
#that lead from the lower level taxa.  It then removes these 'dead end taxa'
######################################################################################


parDict = {}
taxDict = {}
spgenList = []

toRemove = []

def findParPaths(file):
	infile = open(file,'r').readlines()
	outfile = open('deadendTaxa','a')
	for line in infile:
		#lineDict[line.split('\t')[0]] = line
		parDict[line.split('\t')[0]] = line.split('\t')[1]
		if line.split('\t')[-2] == 'genus' or line.split('\t')[-2] == 'species' or line.split('\t')[-2] == 'subspecies' or line.split('\t')[-2] == 'subgenus':
			spgenList.append(line.split('\t')[0])
	
	for taxon in spgenList:
		makeList(taxon)

	for line in infile:
		
		try:
			taxDict[line.split('\t')[0]]
		except:
			outfile.write(line)
			

	outfile.close()


def makeList(taxon):
		if taxon == '':
			return
		try:
			x = taxDict[taxon]
		except:
			taxDict[taxon] = 'ok'
			makeList(parDict[taxon])
		else:
			return

		
def removeDeadEnds(file):
	outfile2 = open(file + 'noDeadEnds' ,'a')
	infile2 = open('deadendTaxa','r').readlines()
	for line in infile:
		if line not in infile2:
			outfile2.write(line)
	
	
def main():
	file = raw_input('What file do you want to check? ' )	
	try:
		x = open(file,'r')		
	except:
		print ' Trouble opening that file.  Try again. '
		main()	
	findParPaths(file)
	removeDeadEnds(file)
main()