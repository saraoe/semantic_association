from huggingface_hub import hf_hub_download

hf_hub_download(
    repo_id="Word2vec/wikipedia2vec_enwiki_20180420_100d",
    filename="enwiki_20180420_100d.txt",
    local_dir="models",
)

import gensim.downloader

model = gensim.downloader.load("word2vec-google-news-300")
model.save_word2vec_format("models/word2vec-google-news-300.txt")
