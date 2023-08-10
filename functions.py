import fitz
import csv

def transCSV(file):
    responses = open('./csv files/trans.txt','w',newline='')
    write = csv.writer(responses)

    doc = fitz.open(file) # open a document
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
def answerCSV(file):
    def color(num):
        return 'Green' if num == 32512 else 'Red' if num == 16711680 else 'Other'
    data = open('./csv files/qp.txt','w',newline='')
    write = csv.writer(data)
    doc = fitz.open(file)
    #paper name saving
    page = doc[0]
    text = page.get_text().strip().split('\n')
    for line in text:
        if text.index(line)==7:
            write.writerow([line[0:-8]])
            break
    #questions data saving
    Question_id=None;Question_type=None;COptions=[];WOptions=[]
    for i in range(len(doc)):
        page = doc[i]
        blocks = page.get_text("dict", flags=11)["blocks"]
        for b in blocks:  # iterate through the text blocks
            for l in b["lines"]:  # iterate through the text lines
                for s in l["spans"]:  # iterate through the text spans
                    # write.writerow([s['text']])
                    # print(s["text"], color(s['color']), sep=' ') # color converter, main color code in binary
                    if (('Question Id' in s['text']) and 'COMPREHENSION' not in s['text']):
                        if Question_type in ['MSQ','MCQ']:
                            write.writerow([Question_id,Question_type,'$'.join(COptions),'$'.join(WOptions)])
                        elif Question_type in ['SA']:
                            write.writerow([Question_id,Question_type,':'.join(COptions[0].split(' to ')),'$'.join(WOptions)])
                        row = s['text'].split(' ')
                        Question_id = row[7];Question_type = row[11];COptions = [];WOptions = []
                    if Question_type in ['MCQ','MSQ']:
                        if s['text'][-2:]=='. ':
                            if color(s['color'])=='Green':
                                COptions.append(s['text'][:-2])
                            elif color(s['color'])=='Red':
                                WOptions.append(s['text'][:-2])
                    elif Question_type == 'SA':
                        if color(s['color'])=='Green':
                            COptions.append(s['text'])
                    #end page qeustion saving case:
                    if (i== len(doc)-1 and blocks.index(b)==len(blocks)-1):
                        if Question_type in ['MSQ','MCQ']:
                            write.writerow([Question_id,Question_type,'$'.join(COptions),'$'.join(WOptions)])
                        elif Question_type in ['SA']:
                            write.writerow([Question_id,Question_type,':'.join(COptions[0].split(' to ')),'$'.join(WOptions)])