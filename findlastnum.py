###############################################
#This script finds the highest number used in OTToL for a given database (i.e. CoL)
###############################################

print 'This script finds the highest number used in OTToL for a given database (i.e. CoL)'




import re
numlist = []
def findlastnum(filename, dbname):

	infile = open(filename,'r').readlines()
	for line in infile:
		db = line.split('\t')[2]
		if re.search(dbname,db):
			numlist.append(line.split('\t')[0])
		
	numlist.sort()
	print numlist
	print numlist.pop()
def main():
	filename = raw_input('what is the file you want to look at? ')
	dbname	 = raw_input('what is the dbfield you want to look at? ')

	findlastnum(filename, dbname)


main()