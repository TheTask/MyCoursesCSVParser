#Assumed 18 column csv file with columns [ OrgDefinedId, Username, FirstName, LastName, Attempt #, Attempt Start,
#Attempt End, Section #, Q #, Q Type, Q Title, Q Text, Bonus?, Difficulty, Answer, Answer Match, Score, Out Of ]

import csv, os, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("csvdata",help="csv file to parse from MyCourses")
parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity in the output file")
args = parser.parse_args()

filename = args.csvdata

print( "Parsing started...")

with open(filename, newline='') as csvfile:
    i=0
    lastDirName = ""
    lastFileName = ""
    lastQuestionNum= -1
    master_dict = {}
    included_cols = [0, 1, 8, 11, 14, 15] # cols we need ['OrgDefinedId', 'Username', 'Q #', 'Q', 'Answer', 'Answer Match']
    spamreader = csv.reader(csvfile, delimiter=',') #read csv line delimit on comma
    
    for row in spamreader:
        content = list(row[i] for i in included_cols)
        if(content[0] == "OrgDefinedId"): #exclude first line
            continue

        #define output structure as results/studentID_mcgillEmail/result.txt
        newDirName = "results/" + content[0] + "_" + content[1]
        newFileName = newDirName + "/result.txt"

        if(content[2] != ''): #skip invalid lines
            if(lastDirName == ""):
                lastDirName = "results/" + content[0] + "_" + content[1]

            if(lastFileName == ""):
                lastFileName = lastDirName + "/result.txt"

            if(newFileName != lastFileName): #new person, write contents of master_dict into a file
                if not os.path.exists(lastDirName): #make a directory for each student
                    os.makedirs(lastDirName)

                if(master_dict.keys() != []): #master_dict of previous person is filled
                    f = open(lastFileName, "w")
                    
                    sorted_keys = sorted(master_dict.keys())

                    counter = 1 #Question counter, just for iteratively printing nubmbers
                    for question in sorted_keys:
                        f.write("\n" + "Question " + str(counter) + ":  " + question + "\n")
                        counter += 1
                        
                        sorted_ans = sorted(master_dict[question].keys())

                        for ans in sorted_ans:
                            if args.verbose:
                                f.write(ans + "  " +  master_dict[question][ans] + "\n")
                            else:
                                f.write(master_dict[question][ans] + "\n") #dont include answer template

                    f.close()
                    master_dict.clear() #clear for next person
                    
                lastDirName = newDirName
                lastFileName = newFileName

            #make new master_dict entry with empty data for each new question
            if(lastQuestionNum != content[2]):
                lastQuestionNum = content[2]
                master_dict[str(content[3])] = {}
            
            master_dict[str(content[3])][str(content[4])] = str(content[5]) #store the csv line in master_dict

        '''
        i+=1
        if i == 1000: Consider only first 1000 lines from csv file for debugging
            break
        '''
        
print("Done!")
