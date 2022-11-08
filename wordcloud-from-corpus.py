import pyconll
import pdftotext
import pandas
import argparse
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def getPOS(conllu, posList):
    words = []
    for sentence in conllu:
        for token in sentence:
            if token.upos in posList:
                words.append(token.form.lower())
    return words

def diff(x, y):
    return list(set(x) - set(y))

def getWordsFromPDF(pdf_path):
    words = []
    with open(pdf_path, "rb") as f:
        pdf = pdftotext.PDF(f)
        for page in pdf:
            for word in page.split():
                words.append(word)
    return [word.lower() for word in words]

def countTokens(tokens, words):
    counts = []
    for token in tokens:
        counts.append(words.count(token))
    return pandas.DataFrame({'Token': [token.capitalize() for token in tokens], 'Count': counts}).drop(index=pandas.np.where(pandas.np.array(counts) == 0)[0])

def generateWordCloud(df, colormap = 'viridis'):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width = 1920, height = 1080, background_color='white', colormap=colormap, stopwords = stopwords, min_font_size = 10).generate_from_frequencies(df.set_index('Token')['Count'].to_dict())
    plt.figure(figsize = (16, 9), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()
    return plt
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='wordCloudFromCorpus')
    parser.add_argument('--conllu', 
        help='The path to conllu file', 
        required=True)
    parser.add_argument('--pdf', 
        help='The path to pdf file', 
        required=True)
    parser.add_argument('--posInclude', 
        help='The part of speech to be extracted from conllu file. For more than part of speech, wite as a delimited list', 
        required=True)
    parser.add_argument('--posExclude', 
        help='The part of speech to be extracted from conllu file. For more than part of speech, wite as a delimited list', 
        required=False)
    parser.add_argument('--colormap',
        help='The matplotlib colormap to be used for the word cloud',
        default='viridis',
        required=False)
    args = parser.parse_args()

    conllu = pyconll.load_from_file(args.conllu)
    list1 = getPOS(conllu, [element for element in args.posInclude.split(',')])
    list2 = getPOS(conllu, [element for element in args.posExclude.split(',')])
    list1_exclude_2 = diff(list1, list2)
    words = getWordsFromPDF(args.pdf)

    df = countTokens(list1_exclude_2, words)
    print(df.sort_values(by='Count', ascending=False))
    df.to_csv(f'./output-data/csv/{args.pdf.split("/")[-1].split(".")[0]}.csv', index=False)
    plt = generateWordCloud(df, colormap = args.colormap)