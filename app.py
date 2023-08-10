# importing necessary
import os, functions

# GETTING FILES FROM USER AND WRITING CSV
print('\n*****************#_________Welcome to QuizEvaluator!_________#********************')
print('Note: ONLY Answer Key & Transcript should be in \'pdf files\' folder with original name downloaded from IITM\n')
folder_path = "./pdf files"
items = os.listdir(folder_path)
if len(items)>2:
    print('Please Remove unnesesary files in \'pdf files\' folder.')
else:
    for item in items:
        if item[:5]=='IIT M':
            AnswerKey= './pdf files/'+item
        else:
            Transcript= './pdf files/'+item
    print("Answer key location: %s\nTranscript location: %s" % (AnswerKey, Transcript))
functions.transCSV(Transcript)
functions.answerCSV(AnswerKey)

#EVALUATING TRANSCRIPT BY ANSWER KEY











# import fitz
# def color(num):
#     return 'Green' if num == 32512 else 'Red' if num == 16711680 else 'Other'

# doc = fitz.open('./pdf files/qp.pdf')
# for i in range(0,4):
#     page = doc[i]
#     blocks = page.get_text("dict", flags=11)["blocks"]
#     for b in blocks:  # iterate through the text blocks
#         for l in b["lines"]:  # iterate through the text lines
#             for s in l["spans"]:  # iterate through the text spans
#                 print("")
#                 print(s["text"], color(s['color']), sep='\n') # color converter, main color code in binary


# Asking if student wants to delete unnesessary files
