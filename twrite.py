import fitz
import csv

responses = open('./csv files/trans.txt','w',newline='')
write = csv.writer(responses)

doc = fitz.open('./pdf files/trans.pdf') # open a document
i=0
text = chr(12).join([page.get_text() for page in doc])
lines = text.strip().split('\n')
for line in lines:
    index = lines.index(line)
    line = line.replace("", "")
    if i==1: write.writerow([line])
    if i==3: write.writerow([line[10:]])
    if i>10 and i%2!=0:
        Qid = line
        Res = lines[index+1]
        if Res!='Unanswered':
            write.writerow([Qid, '$'.join(Res.split(','))])
    i+=1