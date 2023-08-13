# QuizEvaluator4-IITM_BS
A automated quiz evaluator for IITM BS students who are anxious to know their scores before IITM release that to their dashboard.
This program reads pdf files i.e, answer key and transcript given by student and then evaluates their score.

Note:
~ There are two versions of same program.
> One is with Graphical user interface, made with python. Located in GUI version
> The usual terminal running version is resided in root folder, main.py 

How to use:
> Run the main.py file.
> Follow instructions as program outputs.
> For testing program, pdf files are in 'pdf files for testing folder'.

How this program works:
1. functions.py contains main functions, when main.py is executed then it calls required functions from functions.py and get outputs.
2. At first main.py runs play function then it calls getfiles function in functions.py then it pops filemanaget to make user select files.
3. According to cases like wrong file selection, Question paper key not matching the program is designend to handle that.
4. If correct files uploaded then the program reads the pdfs and makes csv files in 'csv files' folder.
5. Then the evaluation starts and it calculates score for each subject and prints score.