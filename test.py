import fitz, csv
def color(num):
        return 'Green' if num == 32512 else 'Red' if num == 16711680 else 'Other'
data = open('./csv files/qp.txt','w',newline='')
write = csv.writer(data)
doc = fitz.open('./pdf files/IIT M.pdf')
#paper name saving
page = doc[0]
text = page.get_text().strip().split('\n')
for line in text:
    if text.index(line)==7:
        write.writerow([line[0:-8]])
        break
#questions data saving
Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
for i in range(9,10):
    page = doc[i]
    blocks = page.get_text("dict", flags=11)["blocks"]
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans
                # write.writerow([s['text']])
                if s['text']=='Maths2':
                    #print(s["text"], s['color'], sep=' ') # color converter, main color code in binary
                    print(s)
                print(s['text'], s['size'])
                # if (('Question Id' in s['text']) and 'COMPREHENSION' not in s['text']):
                #     if Question_type in ['MSQ','MCQ']:
                #         write.writerow([Question_id,Question_marks,Question_type,'$'.join(COptions),'$'.join(WOptions)])
                #     elif Question_type in ['SA']:
                #         write.writerow([Question_id,Question_marks,Question_type,':'.join(COptions[0].split(' to ')),'$'.join(WOptions)])
                #     row = s['text'].split(' ')
                #     Question_id = row[7];Question_marks=0;Question_type=row[11];COptions=[];WOptions=[]
                # if 'Correct Marks' in s['text']:
                #     Question_marks = s['text'].split()[3]
                # if Question_type in ['MCQ','MSQ']:
                #     if s['text'][-2:]=='. ':
                #         if color(s['color'])=='Green':
                #             COptions.append(s['text'][:-2])
                #         elif color(s['color'])=='Red':
                #             WOptions.append(s['text'][:-2])
                # elif Question_type == 'SA':
                #     if color(s['color'])=='Green':
                #         COptions.append(s['text'])
                # #end page qeustion saving case:
                # if (i== len(doc)-1 and blocks.index(b)==len(blocks)-1):
                #     if Question_type in ['MSQ','MCQ']:
                #         write.writerow([Question_id,Question_marks,Question_type,'$'.join(COptions),'$'.join(WOptions)])
                #     elif Question_type in ['SA']:
                #         write.writerow([Question_id,Question_marks,Question_type,':'.join(COptions[0].split(' to ')),'$'.join(WOptions)])