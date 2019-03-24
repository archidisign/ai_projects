import io
import sys
import csv

mycsv = open("./MCQ_DB/DB_Pyschology.csv", 'w')

headings = 'ID, question, Option 1, Option 2, Option 3, Option 4, Answer\n'
mycsv.write(headings)

with open("./MCQ_original/Psychology.txt", encoding="utf8") as mytxt:
	data = mytxt.readlines()

# initialize values
temp = ["None"]*7
ID=1
tempIndex=0

# loop to create Database
for line in data:
    # Start a new line
	if tempIndex == 0 and line != '\n':
		# ID of new MC question
		temp[0]=str(ID)
		# Save the question
		temp[1] = '"' + line.strip() + '"'
		tempIndex=tempIndex+1

	# Save the options
	elif (tempIndex==1 or tempIndex==2 or tempIndex==3 or tempIndex==4 or tempIndex==5) and line != '\n':
		a = line[:1]
		b = line[2:]
		# Save answer options
		temp[tempIndex+1]='"' + b.strip() + '"'
		# Save right Answer
		if a[0]==str(1):
			temp[6]='"' + b.strip()+ '"'
		# iterate
		tempIndex=tempIndex+1

	# Store in csv file
	if line=='\n':
		# Concatenate & write
		newline=','.join(temp) + '\n'
		mycsv.write(newline)
		# Reinitialize
		ID=ID+1
		tempIndex=0
mycsv.close()