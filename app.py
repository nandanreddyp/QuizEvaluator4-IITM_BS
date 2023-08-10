# importing necessary
import os, sys, functions

# GETTING FILES FROM USER AND WRITING CSV with them
print('\n*****************#_________Welcome to QuizEvaluator!_________#********************')
print('Note: ONLY Answer Key & Transcript should be in \'pdf files\' folder with original name downloaded from IITM\n')
will = input('Are you sure that your 2 files present in \'pdf files\' folder? (y/n): ')
if will[0].lower()=='y': pass
else: sys.exit()
folder_path = "./pdf files"
items = os.listdir(folder_path)
if len(items)>2:print('Please Remove unnesesary files in \'pdf files\' folder.');sys.exit()
elif len(items)<2:print('Please Add all required files in to \'pdf files\' folder');sys.exit()
else:
    AnswerKey=None;Transcript=None
    for item in items:
        if item[:5]=='IIT M':
            AnswerKey= './pdf files/'+item
        elif item[:3]=='POD':
            Transcript= './pdf files/'+item
    if AnswerKey == None or Transcript == None:
        print('Please make sure File names are not modified!\nAnswer key should start with \'IIT M\' and Transcript with \'POD\'')
        sys.exit()
    print("Answer key location: %s\nTranscript location: %s" % (AnswerKey, Transcript))
functions.transCSV(Transcript)
functions.answerCSV(AnswerKey)
print('\nSuccessfully read fies and made csv files\n')

#EVALUATING TRANSCRIPT BY ANSWER KEY
functions.evaluate('./csv files/qp.txt','./csv files/trans.txt')






#Delte csv files
