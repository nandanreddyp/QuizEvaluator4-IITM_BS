import csv, subprocess, sys
try:
    import fitz
except ImportError:
    print("PyMuPDF is not installed. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])
        print("PyMuPDF installed successfully.")
        import fitz
    except subprocess.CalledProcessError:
        print("Failed to install PyMuPDF.\nPlease use internet to resolve this issue.")
        sys.exit()

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
    Qcount=0
    Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
    for i in range(len(doc)):
        page = doc[i]
        blocks = page.get_text("dict", flags=11)["blocks"]
        for b in blocks:  # iterate through the text blocks
            for l in b["lines"]:  # iterate through the text lines
                for s in l["spans"]:  # iterate through the text spans
                    if (i== len(doc)-1 and blocks.index(b)==len(blocks)-1 and COptions!=[]) or (color(s['color']) not in ['Green','Red'] and COptions!=[]):
                        if Question_type in ['MSQ','MCQ']:
                            write.writerow([Question_id,Question_marks,Question_type,'$'.join(COptions),'$'.join(WOptions)])
                        elif Question_type in ['SA']:
                            write.writerow([Question_id,Question_marks,Question_type,':'.join(COptions[0].split(' to ')),'$'.join(WOptions)])
                        Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
                    if s['size']==18 and s['text'][:5]!='Group':
                        write.writerow([s['text']])
                    if ('Question Id' in s['text'] and 'COMPREHENSION' not in s['text']):
                        Qcount+=1
                        row = s['text'].split(' ')
                        Question_id = row[7];Question_marks=0;Question_type=row[11];COptions=[];WOptions=[]
                    # options appending
                    if Question_type=='SA' and color(s['color'])=='Green':
                        COptions.append(s['text'])
                    if s['text'][-2:]=='. ':
                        if color(s['color'])=='Green':
                            COptions.append(s['text'][:-2])
                        elif color(s['color'])=='Red':
                            WOptions.append(s['text'][:-2])
                    if 'Correct Marks' in s['text']:
                        Question_marks = s['text'].split()[3]
    # print(f'total questions (246): {Qcount}')
def Calculate(Course, Sub, Answ):
    if Sub[0][0] not in Answ:
        return None
    Tmarks=0;Smarks=0
    for ques in Sub:
        Tmarks+=float(ques[1])
        if ques[0] in Answ:
            if ques[2]=='SA':
                if len(ques[3].split(':'))==1:
                    if ques[3]==Answ[ques[0]]:
                        Smarks+=float(ques[1])
                else:
                    # print(float(ques[3].split(':')[0]),float(Answ[ques[0]]),float(ques[3].split(':')[1]))
                    if float(ques[3].split(':')[0]) <= float(Answ[ques[0]]) <= float(ques[3].split(':')[1]):
                        Smarks+=float(ques[1])
            else:
                count=0;total=len(ques[3].split('$'))
                for ans in Answ[ques[0]].split('$'):
                    if ans in ques[4].split('$'):
                        count=0; break
                    if ans in ques[3].split('$'):
                        count+=1
                Smarks+=(count/total)*float(ques[1])
    marks = (Smarks/Tmarks)*100
    print("{:<10}: {:>3}".format(Course, marks))
def evaluate(akey, trans):
    Trans = open(trans,'r')
    Akey  = open(akey, 'r')
    # getting necessary info from Answers
    Name  = Trans.readline().strip()
    print(f'Hey {Name}, Your scores in each course is:')
    tkey  = Trans.readline()
    akey  = Akey.readline()
    if tkey!=akey:
        print(f'Code of Answer key: {akey} and Transcript key: {tkey} Not matching. Please upload correct ones.')
        sys.exit()
    # evaluation
    Akey = Akey.readlines()
    Akey = [line.strip() for line in Akey]
    resp = {}
    for line in Trans:
        line = line.strip()
        resp[line.split(',')[0]]=line.split(',')[1]
    # evaluation
    Course=None;Answerkey=[]
    for line in Akey:
        line = line.strip()
        if len(line.split(','))==1 or Akey.index(line)==len(Akey)-1:
            if Akey.index(line)!=0:
                Calculate(Course, Answerkey, resp)
            Course = line; Answerkey=[]
        else:
            Answerkey.append(line.split(','))
        
        
