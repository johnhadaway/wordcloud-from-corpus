import pyconll
import pdftotext
import pandas
import argparse
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def getPOS(conllu, posList):
    print(posList)
    words = []
    for sentence in conllu:
        for token in sentence:
            if token.upos in posList and token.form != None:
                words.append(token.form.lower())
    return list(set(words))


def combineLists(lists):
    return list(set([item for sublist in lists for item in sublist]))


def diff(x, y):
    return list(set([item for item in x if item not in y]))


def getWordsFromPDF(pdf_path):
    words = []
    with open(pdf_path, "rb") as f:
        pdf = pdftotext.PDF(f)
        for page in pdf:
            for word in page.split():
                words.append(word)
    return [word.lower() for word in words]


def getWordsFromText(text_path):
    words = []
    with open(text_path, "r") as f:
        for line in f:
            for word in line.split():
                words.append(word)
    return [word.lower() for word in words]


def countTokens(tokens, words):
    counts = []
    for token in tokens:
        counts.append(words.count(token))
    return pandas.DataFrame({'Token': [token.capitalize() for token in tokens], 'Count': counts})[lambda x: x['Count'] != 0]


def generateWordCloud(df, colormap='viridis'):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width=1920, height=1080, background_color='white', colormap=colormap, stopwords=stopwords,
                          min_font_size=10).generate_from_frequencies(df.set_index('Token')['Count'].to_dict())
    plt.figure(figsize=(16, 9), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='wordCloudFromCorpus')
    parser.add_argument('--conllu',
                        help='The path to conllu file.',
                        required=True)
    parser.add_argument('--file',
                        help='The path to either the .pdf or .txt file',
                        required=True)
    parser.add_argument('--posInclude',
                        help='The part of speech to be extracted from conllu file. For more than part of speech, wite as a comma-delimited list',
                        required=True)
    parser.add_argument('--posExclude',
                        help='The part of speech to be extracted from conllu file. For more than part of speech, wite as a comma-delimited list',
                        required=False)
    parser.add_argument('--colormap',
                        help='The matplotlib colormap to be used for the word cloud',
                        default='viridis',
                        required=False)
    args = parser.parse_args()

    if args.file.endswith('.pdf'):
        words = getWordsFromPDF(args.file)
    elif args.file.endswith('.txt'):
        words = getWordsFromText(args.file)
    else:
        print('This currently must be either .pdf or .txt')
        exit()

    conllu = pyconll.load_from_file(args.conllu)
    list1 = getPOS(conllu, [element for element in args.posInclude.split(',')])
    if args.posExclude:
        exclude_list = []
        list2 = getPOS(
            conllu, [element for element in args.posExclude.split(',')])
        list1_exclude_2 = diff(list1, list2)
        print(len(list1_exclude_2))
        df = countTokens(list1_exclude_2, words)
    else:
        df = countTokens(list1, words)

    generateWordCloud(df, args.colormap)

    df = countTokens(list1_exclude_2, words)
    print(df.sort_values(by='Count', ascending=False))
    df.to_csv(
        f'./output-data/csv/{args.file.split("/")[-1].split(".")[0]}.csv', index=False)
