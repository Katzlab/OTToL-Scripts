###############################################
#This script reads in the OTToL file and outputs the # of species, genera and 'above genera'
###############################################
print "This script reads in the OTToL file and outputs the # of species, genera and 'above genera'"


def getStats(file):
	spcount = 0
	gencount = 0
	othercount = 0
	infile = open(file,'r').readlines()
	for line in infile:
		rank = line.split('\t')[-2]
	
		if rank == 'species':
			spcount = spcount + 1
		elif rank == 'genus':
			gencount = gencount + 1
		else:
			othercount = othercount + 1
	print 'species: ' + str(spcount)		
	print 'genera: ' + str(gencount)		
	print 'other: ' + str(othercount)		
		
def main():
	file = raw_input('What file do you want to check? ' )
	
	try:
		x = open(file,'r')
		
	except:
		print ' Trouble opening that file.  Try again. '
		main()
	getStats(file)
main()