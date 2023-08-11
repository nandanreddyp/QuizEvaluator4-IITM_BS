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
    trans = open('./csv files/trans.txt','w',newline='')
    write = csv.writer(trans)
    #reading transcript pdf
    doc = fitz.open(file)
    text = ''.join([page.get_text() for page in doc])
    text = [line.strip() for line in text.split('\n')][:-1]
    # writing information
    write.writerow([text[1]])
    write.writerow([' '.join(text[3].split()[4:8])])
    for i in range(11,len(text)):
        if i%2!=0 and i!=len(text)-1 and text[i+1]!='Unanswered':
            if text[i][:4]==text[i+1][:4]:
                write.writerow([text[i],'$'.join(text[i+1].split(','))])
            else:
                write.writerow([text[i],text[i+1]])

def answerCSV(file):
    def color(num):
        return 'Green' if num==32512 else 'Red' if num==16711680 else 'Other'
    doc = fitz.open(file)
    answer = open('./csv files/key.txt','w',newline='')
    write = csv.writer(answer)
    #writing question paper id in key
    text=doc[0].get_text().strip().split('\n')
    write.writerow([' '.join(text[7].split()[2:6])])
    #questions data saving
    def add(Question_id,Question_marks,Question_type,COptions,WOptions):
        if Question_id==None: return 
        if Question_type in ['MSQ','MCQ']:
            write.writerow([Question_id,Question_marks,Question_type,'$'.join(COptions),'$'.join(WOptions)])
        elif Question_type in ['SA']:
            write.writerow([Question_id,Question_marks,Question_type,':'.join(COptions[0].split(' to ')),'$'.join(WOptions)])
        Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
    Qcount=0;Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
    for i in range(len(doc)):
        page = doc[i]
        blocks = page.get_text("dict", flags=11)["blocks"]
        for b in blocks:  # iterate through the text blocks
            for l in b["lines"]:  # iterate through the text lines
                for s in l["spans"]:  # iterate through the text spans
                    if s['size']==18 and s['text'][:5]!='Group':
                        if Question_id!=None: 
                            add(Question_id,Question_marks,Question_type,COptions,WOptions)
                        Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
                        write.writerow([s['text']])
                    elif ('Question Id' in s['text'] and 'COMPREHENSION' not in s['text']):
                        if Question_id!=None: add(Question_id,Question_marks,Question_type,COptions,WOptions)
                        Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
                        Qcount+=1
                        row = s['text'].split(' ')
                        Question_id = row[7];Question_marks=0;Question_type=row[11];COptions=[];WOptions=[]
                    elif 'Correct Marks' in s['text']:
                        Question_marks = s['text'].split()[3]
                    elif color(s['color']) in ['Green','Red']:
                        if len(s['text'])==len('6406531931004. ') and str(s['text'][:4])=='6406531931004. '[:4]:
                            if color(s['color'])=='Green':
                                COptions.append(s['text'][:-2])
                            elif color(s['color'])=='Red':
                                WOptions.append(s['text'][:-2])
                        elif Question_type=='SA' and color(s['color'])=='Green':
                            COptions.append(s['text'])
                            add(Question_id,Question_marks,Question_type,COptions,WOptions)
                            Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
                    if (i== len(doc)-1 and blocks.index(b)==len(blocks)-1):
                        add(Question_id,Question_marks,Question_type,COptions,WOptions)
                        Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
    # print(f'Total no of questions ():{Qcount}')

def calculate(Course, SecQs, Resp):
    if SecQs[0][0] not in Resp:
        return None
    Tmarks=0;Smarks=0
    for ques in SecQs:
        Tmarks+=float(ques[1])
        if ques[0] in Resp:
            if ques[2]=='SA':
                if len(ques[3].split(':'))==1:
                    if ques[3]==Resp[ques[0]]:
                        Smarks+=float(ques[1])
                else:
                    # print(float(ques[3].split(':')[0]),float(Answ[ques[0]]),float(ques[3].split(':')[1]))
                    if float(ques[3].split(':')[0]) <= float(Resp[ques[0]]) <= float(ques[3].split(':')[1]):
                        Smarks+=float(ques[1])
            else:
                count=0;total=len(ques[3].split('$'))
                for ans in Resp[ques[0]].split('$'):
                    if ans in ques[4].split('$'):
                        count=0; break
                    if ans in ques[3].split('$'):
                        count+=1
                Smarks+=(count/total)*float(ques[1])
    marks = (Smarks/Tmarks)*100
    print("{:<10}: {:>3}".format(Course, marks))

def evaluate():
    key = open('./csv files/key.txt')
    trans = open('./csv files/trans.txt')
    Name = trans.readline().strip()
    print(f'Hey, {Name}. Your scores in each subject are: ')
    Akey = key.readline().strip(); Tkey = trans.readline().strip()
    if Akey!=Tkey:
        print(f'Answer key: {Akey} not matching with {Tkey}')
        sys.exit()
    Key = [ques.strip() for ques in key]
    Resp = {}
    for line in trans:
        line = line.strip()
        Resp[line.split(',')[0]]=line.split(',')[1]
    #Grouping courses
    Course=None;Answerkey=[]
    for line in Key:
        if len(line.split(','))==1:
            if Course!=None:
                calculate(Course, Answerkey, Resp)
            Course=line;Answerkey=[]
        elif Key.index(line)==len(Key)-1:
            calculate(Course, Answerkey, Resp)
        else:
            Answerkey.append(line.split(','))
        
        
