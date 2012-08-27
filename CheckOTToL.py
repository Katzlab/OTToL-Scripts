
import os,re
removeList = []
iddict = {}
linedict = {}
childdict = {}


def makeDicts(x):
	iddict = {}
	linedict = {}
	infile = open(x,'r').readlines()

	for line in infile:
		try:
			rank =  line.split('\t')[-2]
			taxid =  line.split('\t')[0]
			parid = line.split('\t')[1]
			db =  line.split('\t')[2]
			taxon =  line.split('\t')[3]
			
			try:
				childdict[parid].append(taxid)
			except:
				childdict[parid] = []
				childdict[parid].append(taxid)
			try:
				iddict[taxon].append(taxid)
			except:
				iddict[taxon] = []
				iddict[taxon].append(taxid)	
			linedict[taxid] = line


		
		except:
			print line

	return iddict,linedict,childdict
	
def getparentlessquick(x,linedict):
	outfile = open('QuickListofParentlessTaxa_' + x,'w')
	parentlessList = []
	for line in open(x,'r'):
		parid =  line.split('\t')[1]
		taxid =  line.split('\t')[0]
		taxon =  line.split('\t')[3]
		try:
			parent = linedict[parid]
		except:
			if taxid != '2822864':
				parentlessList.append(taxid)
				outfile = open('QuickListofParentlessTaxa_' + x,'a')
				outfile.write(line)
				outfile.close()
	try:
		return parentlessList
	except:
		print 'no parentless taxa in this file'
		
			
def findAllChildren(x,iddict,childdict,linedict):
	parentlessList = getparentlessquick(x,linedict) #list of taxon ids without parents
	i = 0
	
	#print parentlessList
	for parentlessid in parentlessList:
		if parentlessid != '2822864':
			#print parentlessid, childdict[parentlessid]
			removelist = makeRemoveList(parentlessid,childdict)
			
	outfile= open('ParentlessTaxa_' + x,'w')	
	for item in removelist:		
		outfile.write(linedict[item])
	outfile.close()

	
	
def makeRemoveList(parentlessid,childdict): #find children of parentless taxon and add them to list to be removed
	removeList.append(parentlessid)
	if parentlessid in childdict.keys():
		for child in childdict[parentlessid]:
			#removeList.append(child)
			makeRemoveList(child,childdict)

	return removeList

	

			
def findDups(x,iddict,linedict):
	outfile2 = open(x + '_duplicates','w')
	for taxon in iddict.keys():
		if len(iddict[taxon]) > 1:
			for id in iddict[taxon]:
				if not re.search('_hom',linedict[id].split('\t')[2]):
					outfile2 = open(x + '_duplicates','a')
					outfile2.write(linedict[id])
					outfile2.close()
	
	

def checktabs(x):
	infile = open(x,'r').readlines()
	outfile3 = open(x + '_problems','w')
	for line in infile:
		try:
			x = line.split('\t')[7] # line doesn't have > 6 tabs
			outfile3.write('line too long: ' + line)
		except:
			try: 
				x = line.split('\t')[6] # line doesn't have < 6 tabs
			except:
				outfile3.write('line too short: ' + line)
			try:
				a = int(line.split('\t')[0])
				b = int(line.split('\t')[1]) #id and parid are numbers
			except:
				if line.split('\t')[0] != '2822864':
					outfile3.write('check id numbers: ' + line)
				
	
		
def main():

	
	x = raw_input('What file do you want to check? ')
	try:
		o = open(x,'r')
	except:
		print 'Trouble opening your file.  Make sure you typed the name correctly and that the file is in the directory. '
		main()
	
	y = raw_input('Do you want to check for duplicate genera and species? y/n ')
	try:
		assert y[0] == 'y' or y[0] == 'n'
	except:
		print 'you must enter y or n.  Please try again.'
		main()
	
	z = raw_input('Do you want to check for parentless taxa? y/n ')
	try:
		assert z[0] == 'y' or z[0] == 'n'
	except:
		print 'you must enter y or n.  Please try again.'
		main()
	if z[0] == 'y':
		a = raw_input('Do you want a quick list of parentless taxa or a slow list (this can take up to 24 hours) of parentless taxa and all their decendents? q/s ')
		try:
			assert  a[0] == 's' or a[0] == 'q'	
		except:
			print 'you must enter s or q.  Please try again.'
			main()	
	checktabs(x) 
	iddict,linedict,childdict = makeDicts(x)
	if y[0] == 'y':
		findDups(x,iddict,linedict)
	try:
		if a[0] == 's':
			findAllChildren(x,iddict,childdict,linedict)
		elif a[0] == 'q':
			getparentlessquick(x,linedict)
	except:
		pass

	
main()