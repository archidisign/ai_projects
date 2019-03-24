import csv
import re
import sys
import random


def QuizMe(sName):
	##tmpPath=path+'DB_'+sName+'.csv'
	tmpPath="./MCQ_DB/DB_"+sName+".csv"
	numQuestions=0
	allQuestions=[]
	correctQuestions=[]
	wrongQuestions=[]
	isSmart=False
	numAnswers=0
	#skip first row
	cRow=1
	tempI=0
	#first pass

	with open(tmpPath,'r') as quizFile:
		reader=csv.reader(quizFile)
		currentQuestion=0
		
		data=[]
		for row in reader:
			if tempI ==0 :
				tempI+=1
				continue
			else:
				data.append(row)

	for i in range(1, len(data)+1):
		random.shuffle(data)
		row=data[0]
		tmpRow = row
		#collect numAnswers here
		numAnswers=len(row)-3
		#else: randomize the answers
		tmpChoices=[]
		allQuestions.append(row)

		#store temporarily the choices to randomize it
		for y in range(2, numAnswers+2):
			tmpChoices.append(tmpRow[y])
		#tmp store the answer
		tmpAns=tmpRow[numAnswers+2]

		random.shuffle(tmpChoices)

		#print question
		printQ=str(i)
		printQ+=". "+row[1]
		print(printQ)
		for x in range(1, numAnswers+1):
			print("     "+str(x)+'. '+tmpChoices[x-1])
		input_var=""
		ans=1
		isAnsValid=False

		#verify answer ()check if int && is between 1 and numQuestions
		while not isAnsValid:
			input_var=input('Your Answer: ')
			if not (isinstance(input_var,int)!=True):
				print("Invalid Answer. Please enter a number!")
				continue
			else:
				ans=int(input_var)
				if(ans>numAnswers or ans<1):
					print("Invalid Answer. Please enter a number between 1 and "+str(numAnswers)+"!")
					continue
				else:
					isAnsValid=True

		if tmpChoices[ans-1]==tmpAns:
			print("Correct Answer! Good Job!\n\n\n")
			correctQuestions.append(row)
		else:
			print("Wrong Answer! >:(")
			print("Answer is: "+ tmpAns +"\n\n\n")
			wrongQuestions.append(row)
		numQuestions+=1
		data.remove(row)


	#check if any wrong questions
	if len(wrongQuestions)==0:
		isSmart=True
		print("Wow! You are so smart! You got all the questions right!\n")
		print("\t█▀█ ▀ █─▄▀ ▄▀▄ ▄▀ █── █─█")
		print("\t█▄█ █ █▀▄─ █▀█ █─ █▀▄ █─█")
		print("\t█── ▀ ▀─▀▀ ▀─▀ ─▀ ▀─▀ ─▀\n")

		print("\t_*___________***")
		print("\t_**__________*__*")
		print("\t*__*_________*___*")
		print("\t*___*________*___*")
		print("\t*____*_______*____******")
		print("\t*_____*______*__________**")
		print("\t*______***__*_**_________*************")
		print("\t*_____*___**_****________________****")
		print("\t_*___*___**___**___________******")
		print("\t__*__*__*___*_____*___****_*")
		print("\t___*_*_*______________****_*")
		print("\t***__**_________****______*")
		print("\t*___*__*_________**____*__*")
		print("\t_*___*_*_________________*")
		print("\t__*__*_*________________**")
		print("\t___*_**___________________**")
		print("\t____**_________________**___*")
		print("\t____*_________________*__*___*")
		print("\t___*_________________*____****")
		print("\t__*___________________*")
		print("\t__*____________________*")
		print("\t__*_____********_______*")
		print("\t___*__**________**____*")
		print("\t___*__*___________*____**")
		print("\t__****_____________********")
	else:
		print("You only have "+str(len(correctQuestions))+" out of "+str(numQuestions)+" questions right! Let's study some more!")
	

	#secondpass, loops until you get all questions right
	while(isSmart!=True):
		nQ=0
		tmpQuestions=wrongQuestions
		#reset questions stats
		wrongQuestions=[]
		correctQuestions=[]
		print("\nAnother round! You still have "+ str(len(tmpQuestions))+ " questions to answer correctly. \n\n")
		for i in range(0, len(tmpQuestions)):
			random.shuffle(tmpQuestions)
			row=tmpQuestions[0]

			nQ+=1
			tmpChoices=[]
			#store temporarily the choices to randomize it
			for y in range(2, numAnswers+2):
				tmpChoices.append(row[y])
			#tmp store the answer
			tmpAns=row[numAnswers+2]

			random.shuffle(tmpChoices)
			#print question
			print(""+str(nQ)+". "+row[1])
			for x in range(1, numAnswers+1):
				print("     "+str(x)+'. '+tmpChoices[x-1])
			input_var=""
			ans=1
			isAnsValid=False

			#verify answer ()check if int && is between 1 and numQuestions
			while not isAnsValid:
				input_var=input('Your Answer: ')
				if not (isinstance(input_var,int)!=True):
					print("Invalid Answer. Please enter a number!")
					continue
				else:
					ans=int(input_var)
					if(ans>numAnswers or ans<1):
						print("Invalid Answer. Please enter a number between 1 and "+str(numAnswers)+"!")
						continue
					else:
						isAnsValid=True
			numQuestions+=1
			if tmpChoices[ans-1]==tmpAns:
				print("Correct Answer! Good Job!\n\n\n")
				correctQuestions.append(row)
				tmpQuestions.remove(row)
			else:
				print("Wrong Answer! >:(")
				print("Answer is: "+ tmpAns +"\n\n\n")
				wrongQuestions.append(row)
		if (len(wrongQuestions)==0):
			isSmart=True

			print("Wow you finished answering all the questions!! You are ready to ace that test! :D \n")
			print("\t█▀█ ▀ █─▄▀ ▄▀▄ ▄▀ █── █─█")
			print("\t█▄█ █ █▀▄─ █▀█ █─ █▀▄ █─█")
			print("\t█── ▀ ▀─▀▀ ▀─▀ ─▀ ▀─▀ ─▀\n")

			print("\t_*___________***")
			print("\t_**__________*__*")
			print("\t*__*_________*___*")
			print("\t*___*________*___*")
			print("\t*____*_______*____******")
			print("\t*_____*______*__________**")
			print("\t*______***__*_**_________*************")
			print("\t*_____*___**_****________________****")
			print("\t_*___*___**___**___________******")
			print("\t__*__*__*___*_____*___****_*")
			print("\t___*_*_*______________****_*")
			print("\t***__**_________****______*")
			print("\t*___*__*_________**____*__*")
			print("\t_*___*_*_________________*")
			print("\t__*__*_*________________**")
			print("\t___*_**___________________**")
			print("\t____**_________________**___*")
			print("\t____*_________________*__*___*")
			print("\t___*_________________*____****")
			print("\t__*___________________*")
			print("\t__*____________________*")
			print("\t__*_____********_______*")
			print("\t___*__**________**____*")
			print("\t___*__*___________*____**")
			print("\t__****_____________********")

print(sys.argv[1])
QuizMe(str(sys.argv[1]))
