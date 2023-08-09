import fitz
def color(num):
    return 'Green' if num == 32512 else 'Red' if num == 16711680 else 'Other'

doc = fitz.open('./pdf files/qp.pdf')
for i in range(0,4):
    page = doc[i]
    blocks = page.get_text("dict", flags=11)["blocks"]
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans
                if s['text'][0:5] == 'IIT M':
                    print(s['text'])