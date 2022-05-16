import os


WORKING_DIR = '../databases/corpora/untarred'

[print(corpus) for corpus in os.listdir(WORKING_DIR) if corpus[0] != '.']
