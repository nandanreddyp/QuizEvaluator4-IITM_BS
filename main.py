from functions import *

def Play():
    paths = GetFiles()
    answerkey = filepaths['answerkey']
    AnswerCSV(answerkey)
    transcript = filepaths['transcript']
    TransCSV(transcript)
    Akey, Tkey = CheckCode()
    if Akey == Tkey:
        result = Evaluate()
        for sub in result:
            print("{:<10}: {:>3}".format(sub[0], sub[1]))
        print('\nThankyou for Using, Contact t.me/nandanreddyp to give feedback or report bugs.'); clear(); sys.exit()
    else: print('Answer key and Transcript\'s \'QuestionPaper Set code\' not matching!\nPlease Select correct files.'); clear(); sys.exit()

Play()
