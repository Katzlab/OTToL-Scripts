###################################################
#a preliminary script using ncbi eutils to deal with
#taxon name reconciliation when adding trees
#to open tree
###################################################

from Bio import Entrez 
Entrez.email = "jgrant@smith.edu"  #Change
import re

outfile = open('out','a')

def makeDicts(x):
	print 'Processing data....'
	parDict = {}
	lineDict = {}
	taxDict = {}
	for line in open(x,'r').readlines():
		taxid =  line.split('\t')[0]
		parid = line.split('\t')[1]
		taxon = line.split('\t')[3]
		
		parDict[taxid] = parid
		lineDict[taxid] = line
		try:
			taxDict[taxon].append(line)
		except:
			taxDict[taxon] = []
			taxDict[taxon].append(line)
		
	print 'Dictionaries made.'
	return parDict, lineDict, taxDict 
		
		
		
		
def getNCBIName(x,query,parDict, lineDict,taxDict): 
###################################################
#uses ncbi espell to find mis-spellings and then summary to get scientific name
#from common name (i.e. Eutheria not placental)
#If not found, taxon will need to be added to OTToL
###################################################
	record = Entrez.read(Entrez.espell(term = query, db = 'taxonomy'))
	record2 = Entrez.read(Entrez.esearch(term = record['CorrectedQuery'], db = 'taxonomy'))
	flag = 0
	for taxid in record2['IdList']:
	
		record3 = Entrez.read(Entrez.esummary(id = taxid, db = 'taxonomy'))
		ans = raw_input('Your list contains ' + query + '. Do you mean ' + record3[0]['ScientificName'] + '? ' )
		if ans[0] == 'y':
			flag = 1
			searchOTToL(x,record3[0]['ScientificName'],parDict, lineDict, taxDict)
	if flag == 0:
		print 'You need to add the taxon: ' + query + ' to OTToL'
		out2 = open('taxa_to_add','a')
		out2.write(query + '\n')
		out2.close()
		
def searchOTToL(x,query,parDict, lineDict, taxDict):
###################################################
#Searches OTToL for the names on the given list
#calls getHom() if not found if the taxon name is marked homonym in OTToL
#calls getNCBIName() if not found
###################################################
	print '.'
	flag = 0
	homList = []
	for line in open(x,'r').readlines():
		taxid = line.split('\t')[0]
		taxon = line.split('\t')[3]
		if line.split('\t')[3] == query:
			flag = 1
			#print line
			if re.search('_hom',line.split('\t')[2]):
				homtax = getHom(x,taxon,parDict, lineDict, taxDict)
				outfile.write(homtax + ',' + lineDict[homtax].split('\t')[3] + ',' + lineDict[parDict[taxid]].split('\t')[3] + '\n')
				return
			else:
				try:
					outfile.write(taxid + ',' + line.split('\t')[3] + ',' + lineDict[parDict[taxid]].split('\t')[3] + '\n')
					return
				except:
					outfile.write(taxid + ',' + line.split('\t')[3] + ',no parent\n')
					return
	if flag == 0:
		getNCBIName(x,query,parDict, lineDict,taxDict)

def getHom(x, taxon,parDict, lineDict, taxDict):
###################################################
#Searches OTToL for the parent names of the homonym
#asks user to choose between taxon with one parent or the other
###################################################
	homList = []
	i = 0		
	print taxon + ' is a homonym. These are the parents of the different homonymic taxa: '
	
	for line in taxDict[taxon]: #open(x,'r').readlines():
		
		if line.split('\t')[3] == taxon:
			i = i + 1
			print str(i) + ')' + lineDict[parDict[line.split('\t')[0]]].split('\t')[3]
			homList.append((lineDict[parDict[line.split('\t')[0]]].split('\t')[3], line.split('\t')[0]))
	q = input('Do you want the one that has one of these as a parent? (type in number next to your selection) ')
	#try:
	r = raw_input('you selected ' + homList[q - 1][0] + '. Is that right? (y/n) ')
	if r == 'y':
		return homList[q - 1][1]
	else:
		print 'try again. '
		getHom(x, taxon,parDict, lineDict)
		



def main():
	x = raw_input('What file do you want to search? ')
	#x = 'OTToL090712.txt'
	try:
		o = open(x,'r')
	except:
		print 'Trouble opening your file.  Make sure you typed the name correctly and that the file is in the directory. '
		main()
	query = raw_input('enter the file with your list of taxon names ')
	#query = 'taxonlist.txt'
	try:
		o = open(query,'r')
	except:
		print 'Trouble opening your file.  Make sure you typed the name correctly and that the file is in the directory. '
		main()	
		
	parDict, lineDict, taxDict =  makeDicts(x)
	for taxon in open(query,'r'):
		searchOTToL(x,taxon.strip(),parDict, lineDict, taxDict)


main()