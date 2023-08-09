import csv

scores = open('./csv files/qp.txt','w',newline='')
write = csv.writer(scores)
fields = ['Qid','Type','marks','Cans','Wans']

write.writerow(fields)
write.writerow(['asdf',3,['a','b','c','d']])
scores.close


scores = open('./csv files/qp.txt','r')
for line in scores:
    print(line.split(','))


#for multiple options: Qid, Mult, marks, 'Cans', 'Wans'
#for text type       : Qid, Str,  marks, 'Ans',  None
#for range type      : Qid, Ran,  marks, 'range', None