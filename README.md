### Description:
This is a CLI for a localisation-oriented word cloud generator. It takes a conllu file and one of {.txt, .pdf} as input. With a list of words belonging to specific parts of speech (--posInclude), extracted from the conllu file, it counts the number of times each occurs in the text input. A parameter (--posExclude) can be used to exclude overlapping parts of speech: for example, you may want a word cloud of all of the adjectives in a PDF, excluding those adjectives that also function as adpositions. The output is a word cloud with the words that appear in the pdf file and belong to (--posInclude) - (--posExclude), saved as a .png file and its data as a .csv. To download corpuses, see [Universal Dependencies](https://universaldependencies.org/).

### Usage:
```
python wordcloud-from-corpus.py --conllu <path to conllu file> --pdf <path to pdf file> --posInclude <part of speech to be included> --posExclude <part of speech to be excluded> --colormap <matplotlib colormap>
```
