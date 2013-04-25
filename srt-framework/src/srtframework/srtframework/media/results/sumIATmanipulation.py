#!/usr/bin/env python2.6
"""
summarizeIAT.py
 
calculates IAT score using "D2" method from Greenwald, Nosek, & Banaji

output: filename, White Faces or Black Faces, D-score, block 1 mean, block 2 mean

the second column states the direction of the test.  So the IAT score
reflects the extent to which the participant associates category A with
category 1 and category B with category 2 more than the reverse.
"""
__author__ = "Winter Mason, Ben Sigmon"
__version__ = "0.1"
__license__ = "public domain"


import os, numpy

# Delete Header and Menu
def headerGetLabels():
    os.system("clear")
    print "-"*140
    print "Summarize IAT output".center(140)
    print "-"*140
    print "\n"
    print "Existing IATs:\n"

def GetLabels():
	iatdb = open('types.txt', 'ab+')
	while(True): # exits when user cancels
		headerGetLabels()
		# Read and display existing IATs
		iatList = []
		iatString = ""
		i = 1
		iatdb.seek(0)
		for line in iatdb:
			iatList.append(line)
			print str(i) + ". " + line
			i = i + 1

		# Read and check userInput
		userInput = raw_input("\nEnter the number of the IAT to delete or R to return to the main menu: ")
		if(not userInput):
			continue
		if(userInput[0]=='r' or userInput[0]=='R'):
			break
		if(not userInput.isdigit() or int(userInput) > i-1):
			raw_input("\nInvalid input! Press ENTER to continue... ")
			continue

		# If userInput checks out, have user confirm
		iatNumber = userInput # Save number of IAT to delete
		filename = iatList[int(iatNumber)-1].strip() + ".txt"
                print filename
		userInput = raw_input("\nAre you sure you want to use "+filename+" to process the output? [Y/N]: ")
		if(not userInput or (userInput[0]!='y' and userInput[0]!='Y')):
			raw_input("\n"+filename+" not used. Press ENTER to continue... ")
			continue

		# After confirm, open file, get and return labels
		filename = '../../static/iat/text/' + filename 
		iatInputFile = open(filename, 'r')
		iatRawFile=[]
		iatLines=[]
		iatInputFile.seek(0)
		for line in iatInputFile:
                    iatRawFile.append(line)
                    i = i + 1
		iatLines.append(iatRawFile[39])
		iatLines.append(iatRawFile[55])
		print "Using "+filename
		raw_input("\nPress ENTER to continue... ")
		iatInputFile.close()
	iatdb.close()
	return iatLines

def calculateIAT(fh, iatLines):        
    catA = ''
    catB = ''
    cat1 = ''
    cat2 = ''
    block1 = []
    block2 = []
    for line in fh:
        try:
            block, round, category, item, errors, RT = line.split(',')
        except:
            print 'err: wrong number of items in ', line
        else:
            if block=='0' and (catA == '' or catB == ''):
                if catA == '':
                    catA = category
                elif catB == '' and catA != category:
                    catB = category
            if block=='1' and (cat1 == '' or cat2 == ''):
                if cat1 == '':
                    cat1 = category
                elif cat2 == '' and cat1 != category:
                    cat2 = category
            if block=='3' or block=='4':
                block1.append(int(RT))
            if block=='6' or block=='7':
                block2.append(int(RT))
    
    label = iatLines[1].strip()
    
    firstMean  = numpy.mean(block1)
    secondMean = numpy.mean(block2)
    score = (firstMean - secondMean)
    block1.extend(block2)
    score = score / numpy.std(block1)
    return label,score,firstMean,secondMean


def parseFiles(iatLines):
    curpath = os.getcwd()
    filenames = os.listdir(curpath)

    try:
        ofh = open('summaryIAT.txt','w')
    except IOerror:
        print 'unable to open output file'
    
    for fname in filenames:
        if fname[0:3].lower() == 'iat':
            try:
                fh = open(fname, 'r')
            except IOerror:
                print 'Unable to open ', fname
            else:
                id = fname.split("_")[1].split("-")[0]
		label, score, firstMean, secondMean = calculateIAT(fh, iatLines)
                ofh.write(id + "," + label + "," + str(score)+ "," + str(firstMean) + "," + str(secondMean) + "\n")
		print 'Successfully processed file ', fname
		fh.close()
    ofh.close()

if __name__ == "__main__":
    print "Started parsing files"
    parseFiles(GetLabels())
    print "Sinished parsing files"
