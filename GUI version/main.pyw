# importing stuff
import sys, subprocess, csv
from tkinter import *
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
####ScoreCalculatingFuctions################################################################################################################################################
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
    Key = [ques.strip() for ques in key]
    Resp = {}
    for line in trans:
        line = line.strip()
        Resp[line.split(',')[0]]=line.split(',')[1]
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
    return [Name]+result
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
#running main
def Play(filepaths):
    answerkey=filepaths['AnswerKey']
    transcript=filepaths['Transcript']
    if FileCheck(answerkey,'A') and FileCheck(transcript,'T'):
        TransCSV(transcript);AnswerCSV(answerkey)
        Akey, Tkey = CheckCode()
        if Akey == Tkey:
            result = Evaluate()
            if len(result)>5:
                return 'You marked yes for more corses in exam'
            return result
        else:
            return f'Answer Key code: {Akey}\nTranscript code: {Tkey}\nNot Matching!'
    else:
        return 'Not Correct Files, Check the files and submit again.'
######################################################################################
###Sample tkinter for reference to clear multipage app
# from tkinter import *
# window = Tk()
# window.geometry('600x300')
# window.title("QuizCal")
# window.resizable(False, False)
# def destroy_all_frames(window):
#     for widget in window.winfo_children():
#         if isinstance(widget, Frame):
#             widget.destroy()
# #Frames............................
# def Home():
#     destroy_all_frames(window)
#     home=Frame()
#     l1 = Label(home,text='Home').pack()
#     b1=Button(home,text='Error',command=lambda:Error()).pack()
#     b2=Button(home,text='Result',command=lambda:Result()).pack()
#     home.pack()
# def Error():
#     destroy_all_frames(window)
#     error=Frame()
#     l1 = Label(error,text='Error').pack()
#     b1=Button(error,text='Home',command=lambda:Home()).pack()
#     b2=Button(error,text='Result',command=lambda:Result()).pack()
#     error.pack()
# def Result():
#     destroy_all_frames(window)
#     result=Frame()
#     l1 = Label(result,text='Result').pack()
#     b1=Button(result,text='Error',command=lambda:Error()).pack()
#     b2=Button(result,text='Home',command=lambda:Home()).pack()
#     result.pack()
# Home()
# window.mainloop()
###########################################################################################################################################################

from tkinter import *
from tkinter import filedialog, ttk
import webbrowser

# files........................
filepaths={'AnswerKey':None,'Transcript':None}
# window.......................
window = Tk()
window.geometry('600x300')
window.title("QuizCal")
window.resizable(False, False)
# clearing frames...................
def destroy_all_frames(window):
    for widget in window.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()
# frames............................
def Home():
    destroy_all_frames(window)
    home = Frame()
    def SelectFile(K):
        global filepaths
        if K=='A':
            file = filedialog.askopenfilename(title="Select Answer Key. Name will be like 'IIT M FOUNDATION AN1 EXAM QPD2'",filetypes=[('Answer Key',"*.pdf")])
            if file: filepaths['AnswerKey']=file; akey_button.config(bg='green'); akey_value.config(text=file.split('/')[-1])
        elif K=='T':
            file = filedialog.askopenfilename(title="Select Transcript file. Name will be like 'POD12S3C4567890'",filetypes=[('Transcript','.pdf')])
            if file: filepaths['Transcript']=file; tkey_button.config(bg='green'); tkey_value.config(text=file.split('/')[-1])
    def Submit():
        if filepaths['AnswerKey'] and filepaths['Transcript']:
            response = Play(filepaths)
            if response == 'Not Correct Files, Check the files and submit again.':
                Error('Not Correct Files, Check the files and submit again.')
            elif isinstance(response, list):
                Result(response)
            elif response == 'You marked yes for more corses in exam':
                Error('You marked yes for more corses in exam')
            elif response.split(':')[0]=='Answer Key code':
                Error(response)
            else:
                Error('')
        else:
            slabel.config(text='Select files!')
    # Title label
    title_label = Label(home, text='Welcome to Quiz Score Calculator', font=('Arial', 18), bg='black', fg='white')
    title_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=10, padx=20)

    # Answer Key section
    akey_label = Label(home, text='Select Answer Key file', font=('Arial', 12))
    akey_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky='w')
    akey_button = Button(home, text='SELECT', command=lambda: SelectFile('A'), font=('Arial', 12))
    akey_button.grid(row=1, column=1, pady=(10, 0), padx=(0, 20), sticky='we',)  # Added padx and 'we'

    akey = Label(home, text='Selected :', font=('Arial', 12))
    akey.grid(row=2, column=0, padx=20, sticky='w')
    akey_value = Label(home, text='Not Selected', font=('Arial', 12))
    akey_value.grid(row=2, column=1, sticky='ew')

    # Transcript section
    tkey_label = Label(home, text='Select Transcript file', font=('Arial', 12))
    tkey_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky='w')
    tkey_button = Button(home, text='SELECT', command=lambda: SelectFile('T'), font=('Arial', 12))
    tkey_button.grid(row=3, column=1, pady=(10, 0), padx=(0, 20), sticky='we')  # Added padx and 'we'

    tkey = Label(home, text='Selected :', font=('Arial', 12))
    tkey.grid(row=4, column=0, padx=20, sticky='w')
    tkey_value = Label(home, text='Not Selected', font=('Arial', 12))
    tkey_value.grid(row=4, column=1, sticky='ew')

    # Submission status label
    slabel = Label(home, text='', fg='red', font=('Arial', 12))
    slabel.grid(row=5, column=0, columnspan=2, pady=5)

    # Adjust column weights to align labels and entries
    home.columnconfigure(0, weight=1)
    home.columnconfigure(1, weight=1)

    # Submit button
    submit_button = Button(home, text='SUBMIT', font=('Arial', 12), command=lambda: Submit())
    submit_button.grid(row=6, column=0, columnspan=2, pady=20, sticky='news')
    home.pack(fill='both',expand=True)

def Result(response):
    destroy_all_frames(window)
    result = Frame(window)
    greet_label = Label(result, text='Hey ' + response[0] + '!\nYour Scores:', font=("Helvetica", 16))
    greet_label.pack(pady=20)
    s1 = Label(result,text='',anchor='w')
    s2 = Label(result,text='',anchor='w')
    s3 = Label(result,text='',anchor='w')
    s4 = Label(result,text='',anchor='w')
    for i in range(len(response)):
        if i==1: s1.config(text=f"{response[i][0]:<20}: {int(round(response[i][1],0))}",font=('Roboto',18))
        elif i==2: s2.config(text=f"{response[i][0]:<20}: {int(round(response[i][1],0))}",font=('Roboto',18))
        elif i==3: s3.config(text=f"{response[i][0]:<20}: {int(round(response[i][1],0))}",font=('Roboto',18))
        elif i==4: s4.config(text=f"{response[i][0]:<20}: {int(round(response[i][1],0))}",font=('Roboto',18))
    s1.pack();s2.pack();s3.pack();s4.pack()
    # reseting paths
    global filepaths
    filepaths={'AnswerKey':None,'Transcript':None}
    b1 = Button(result, text='Calculate for another files', command=lambda: Home(), bg="white", fg="black", font=("Helvetica", 12))
    b1.pack(pady=20, side='bottom')

    result.pack(fill='both', expand=True)

def Error(string):
    destroy_all_frames(window)
    def open_link(event):
        webbrowser.open("https://t.me/nandanreddyp")
    # Create a fullscreen window
    error = Frame(window)
    # Load background image
    background_img = PhotoImage(file="BackgroundIMG.png")
    
    # Create a label for the background image
    background_label = Label(error, image=background_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Label for error message
    e1 = Label(error, text=string, font=("Helvetica", 16), fg="red")
    e1.pack(pady=20)
    
    # Label for contact information
    contact = Label(error, text='If you encounter any bugs, please contact me at', font=("Helvetica", 12))
    contact.pack()
    
    # Link to t.me/nandanreddyp
    link_text = "t.me/nandanreddyp"
    link_label = Label(error, text=link_text, font=("Helvetica", 12, "bold"), fg="blue", cursor="hand2")
    link_label.pack()
    link_label.bind("<Button-1>", open_link)
    
    # Resetting paths
    global filepaths
    filepaths = {'AnswerKey': None, 'Transcript': None}
    
    # Button to go back to home
    b1 = Button(error, text='Submit Files Again', command=lambda: Home(), bg="white", fg="black", font=("Helvetica", 12))
    b1.pack(side='bottom', pady=20)
    error.pack(fill='both', expand=True)

Home()
window.mainloop()
################################################################################################################################################