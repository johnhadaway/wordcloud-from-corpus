### Description:
This is a CLI for a localisation-oriented word cloud generator. It takes a conllu file and a pdf file as input. It then extracts the words from the pdf file and counts the number of times they appear in a list of words belonging to specific parts of speech, --posInclude, extracted from the conllu file. A parameter, --posExclude, can be used to exclude overlapping part(s) of speech: for example, you may want a word cloud of all of the adjectives, excluding those adjectives that also function as adpositions. The output is a word cloud with the words that appear in the pdf file and belong to (--posInclude) - (--posExclude). The word cloud is saved as a .png file, and its data as a .csv. To download corpuses, see [Universal Dependencies](https://universaldependencies.org/).

### Usage:
```
python wordcloud-from-corpus.py --conllu <path to conllu file> --pdf <path to pdf file> --posInclude <part of speech to be included> --posExclude <part of speech to be excluded> --colormap <matplotlib colormap>
```
