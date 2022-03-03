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
- get conllu ver. of file: python3 utils/get_conllu.py data/example.json
- get analysis: txtcomplexity --input-format conllu --all-measures output/example.json.conllu > "output/example_analysis.json"

## Run analysis code 
- set up your environmental variable 
    - on mac for example: export CORENLP_HOME='./corenlp'
- Install any python dependencies
  - pip3 install nltk
  - pip3 install textstat
- create separate terminal and run CoreNLP server
  - cd corenlp
  - java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9001 -timeout 15000
  - If you already have a process running on post 9001, you will need to stop it
    - on mac: lsof -t -i tcp:9001 | xargs kill
- run code, e.g. python3 analysis/analyze_data.py


## Useful Links
- Stanza
    - https://stanfordnlp.github.io/stanza/installation_usage
    - https://github.com/stanfordnlp/stanza/blob/main/doc/CoreNLP.proto 
    - https://stanfordnlp.github.io/stanza/client_usage.html 
    - https://stanfordnlp.github.io/stanza/tutorials.html 
    - https://stanfordnlp.github.io/stanza/neural_pipeline.html
- CoreNLP
    - https://stanfordnlp.github.io/CoreNLP/corenlp-server.html 
- textcomplexity
    - https://github.com/tsproisl/textcomplexity 