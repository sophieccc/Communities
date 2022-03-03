# Communities

## Setup CoreNLP
- download corenlp from this page: https://stanfordnlp.github.io/CoreNLP/download.html
- unzip corenlp into your Communities github directory
- rename unzipped corenlp directory to ‘corenlp’

## Setup Stanza
- Download stanza: pip3 install stanza -U
- Download english language: python3 -c 'import stanza; stanza.download("en")'
  
## Setup & Run textcomplexity
- pip3 install textcomplexity
- get conllu ver. of file: python3 utils/get_conllu.py data/example.txt
- get analysis: txtcomplexity --input-format conllu --all-measures output/example.txt.conllu > "output/example.json"

## Run example Stanza code
- set up your environmental variable 
    - on mac for example: export CORENLP_HOME='./corenlp'
- run code: python3 stanza_examply.py


## Useful Links
- Stanza
    - https://stanfordnlp.github.io/stanza/installation_usage
- CoreNLP
    - https://stanfordnlp.github.io/CoreNLP/corenlp-server.html 
- textcomplexity
    - https://github.com/tsproisl/textcomplexity 