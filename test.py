import fitz, os
def color(num):
    return 'Green' if num == 32512 else 'Red' if num == 16711680 else 'Other'

folder_path = "./pdf files"
items = os.listdir(folder_path)
for item in items:
    if item[:5]=='IIT M':
        Answers= './pdf files/'+item

doc = fitz.open(Answers)
f = open('temp.txt','w')
qcount=0;Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
for i in range(224,len(doc)):
#for i in range(len(doc)):
    page = doc[i]
    blocks = page.get_text("dict", flags=11)["blocks"]
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans
                # print(s['text'])
                # print(s["text"], color(s['color']),blocks.index(b), sep=' ') # color converter, main color code in binary
                if 'Question Id' in s['text'] and 'COMPREHENSION' not in s['text']:
                    print(Question_id,Question_type,COptions,WOptions)
                    qcount+=1
                    row = s['text'].split(' ')
                    Question_id = row[7];Question_marks=0;Question_type = row[11];COptions = [];WOptions = []
                if 'Correct Marks' in s['text']:
                    Question_marks = s['text'][16]
                if Question_type in ['MCQ','MSQ']:
                    if s['text'][-2:]=='. ':
                        if color(s['color'])=='Green':
                            COptions.append(s['text'][:-2])
                        elif color(s['color'])=='Red':
                            WOptions.append(s['text'][:-2])
                elif Question_type == 'SA':
                    if color(s['color'])=='Green':
                        COptions.append(s['text'])
print(f'total questions 246: {qcount}')
                #     Question_type = a[11]
                #     c_options = []
                #     w_options = []
                #     # print(Question_id,Question_type)
                # if 'Correct Marks' in s['text']:
                #         b = s['text'].split(' ')
                #         marks = b[3]
                #         # print(marks)
                # if len(str(s['text'])) == 15 :
                #     if color(s['color']) == 'Green' :
                #           c_options.append(s['text'][0:13])
                #     elif color(s['color']) == 'Red' :
                #          w_options.append(s['text'][0:13])
                #         #  print(c_options,w_options)
                #          print(Question_id,Question_type,marks,c_options,w_options)
                # if color(s['color']) =='Green' and Question_type =='SA':
                #      print(Question_id,Question_type,marks,s['text'])

                