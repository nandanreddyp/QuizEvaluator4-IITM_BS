import fitz
import csv

responses = open('./csv files/trans.txt','w',newline='')
write = csv.writer(responses)

doc = fitz.open('./pdf files/trans.pdf') # open a document
text = chr(12).join([page.get_text() for page in doc]) # text in doc

lines = text.strip().split('\n')
for line in lines:
    index = lines.index(line)
    line = line.replace("", "")
    if index==1: write.writerow([line])
    if index==3: write.writerow([line[10:]])
    if index>10 and index%2!=0:
        Qid = line
        Res = lines[index+1]
        if Res!='Unanswered':
            if Qid[:4]==Res[:4]:
                write.writerow([Qid, '$'.join(Res.split(','))])
            else:
                write.writerow([Qid, Res])

responses.close()
doc.close()