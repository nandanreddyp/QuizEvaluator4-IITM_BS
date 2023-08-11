import sys, subprocess, csv
try:
    import fitz
except ImportError: 
    print("PyMuPDF is not installed. Installing now...")
    try: subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"]); print("PyMuPDF installed successfully."); import fitz
    except subprocess.CalledProcessError: print("Failed to install PyMuPDF.\nPlease use internet to install 'PyMuPDF' package."); sys.exit()
try:
    from tkinter import filedialog
except ImportError:
    print('tkinter is not installed. Installing now...')
    try: subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinter"]); print('tkinker intalled successfully.'); from tkinter import filedialog
    except subprocess.CalledProcessError: print('Failed to install tkinter.\nPlease use internet to install \'Tkinter\' package.'); sys.exit()
#################################################################################################################################################################
def GetFiles():
    print('Select Answer Key pdf file')
    AnswerKey = filedialog.askopenfilename(title='Answer Key',filetypes=[('Answer Key', '*.pdf')])
    print('Select Transcript pdf file')
    Transcript = filedialog.askopenfilename(title='Transcript',filetypes=[('Transcript', '*.pdf')])
    if FileCheck(AnswerKey,'A') and FileCheck(Transcript,'T'): 
        return (AnswerKey,Transcript)
    else: print('Please select CORRECT Answer Key and Transcript!'); GetFiles()
def FileCheck(file, K):
    try:
        doc = fitz.open(file)
        text = doc[0].get_text().split('\n')
        if K=='A':
            if text[0] == 'Indian Institute of Technology, Madras - BS in Data Science and Applications': return True; return False
        elif K=='T':
            if text[0] == 'Name' and text[2] == 'QP Set': return True; return False
    except:
        return False
def TransCSV(file):
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
    trans.close()
def AnswerCSV(file):
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
    answer.close()
def CheckCode():
    key = open('./csv files/key.txt')
    trans = open('./csv files/trans.txt')
    Name = trans.readline() # to remove first line
    Akey = key.readline().strip(); Tkey = trans.readline().strip() #selecting QP set codes
    return (Akey, Tkey)
def Evaluate():
    key = open('./csv files/key.txt')
    trans = open('./csv files/trans.txt')
    Name = trans.readline().strip()
    Akey = key.readline().strip(); Tkey = trans.readline().strip()
    if Akey!=Tkey:
        return 'keys not matching'
    Key = [ques.strip() for ques in key]
    Resp = {}
    for line in trans:
        line = line.strip()
        Resp[line.split(',')[0]]=line.split(',')[1]
    print(f'Hey, {Name}. Your scores in each subject are: ')
    #Grouping courses and evaluating
    Course=None;Answerkey=[];result=[]
    for line in Key:
        if len(line.split(','))==1 or Key.index(line)==len(Key)-1:
            if Course!=None:
                res=(Calculate(Course, Answerkey, Resp))
                if res!=None:
                    result.append(res)
            Course=line;Answerkey=[]
        else:
            Answerkey.append(line.split(','))
    return result
def Calculate(Course, SecQs, Resp):
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
    return (Course, marks)
#################################################################################################################################################################
def Play():
    answerkey, transcript = GetFiles()
    TransCSV(transcript)
    AnswerCSV(answerkey)
    Akey, Tkey = CheckCode()
    if Akey == Tkey: 
        result = Evaluate(); 
        for sub in result: print("{:<10}: {:>3}".format(sub[0], sub[1]))
        print('\nThankyou for Using, Contact t.me/nandanreddyp to give feedback or report bugs.')
    else: print('Answer key and Transcript\'s \'QuestionPaper Set code\' not matching!\nSelect correct files.')
    # deleting saved information about student
    akey=open('./csv files/key.txt','w');akey.write('');akey.close()
    tkey=open('./csv files/trans.txt','w');tkey.write('');tkey.close()
Play()