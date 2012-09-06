######################################################################################
#This script finds species names that do not match the taxon name of their parent
#These may be pointing to the wrong genus or they may be synonyms.
######################################################################################
print '######################################################################################'
print 'This script finds species names that do not match the taxon name of their parent'
print 'These may be pointing to the wrong genus or they may be synonyms.'
print 'They will be writte out to a file called "species_check_genera" in the format <species line : genus line>.'
print 'Problematic lines will be printed to the terminal.'
print '######################################################################################'

import re
idDict = {} # taxid points to (parent id, genus name, line)
outfile = open('species_check_genera','a')

def checkGenus(x):
	infile = open(x,'r').readlines()
	
	for line in infile:
		if line.split('\t')[0] != '2822864':
			taxid = line.split('\t')[0]
			genusname =  line.split()[3] #first word in taxon name = genus
			parid = line.split('\t')[1]
			idDict[taxid] = (parid, genusname,line)
	
	for line in infile:# want for every species to know if the genus name of its parent is the same as its own
		if line.split('\t')[-2] == 'species': 
			taxid = line.split('\t')[0]
			taxname = line.split('\t')[3]
			parid = line.split('\t')[1]

			try:
				if not re.search(idDict[taxid][1],idDict[parid][1]):
					outfile.write(idDict[taxid][2].strip() + ' : ' + idDict[parid][2])
			except:
				print line
			
	outfile.close()	

def main():

	
	x = raw_input('What file do you want to check? ')
	try:
		o = open(x,'r')
	except:
		print 'Trouble opening your file.  Make sure you typed the name correctly and that the file is in the directory. '
		main()
	
	checkGenus(x)

main()