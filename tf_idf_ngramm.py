#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import stdin
from os import linesep
from math import log
from collections import defaultdict
import argparse


def get_count(words):
    tfs = defaultdict(int)
    for w in words:
        tfs[w] += 1
    return tfs


def group_n_grams(words, n, stop_list):
    if n < 2:
        return [w for w in words if w not in stop_list]
    return [' '.join(w for w in words[i:i+n])
            for i in range(len(words)-n)
            if words[i+n-1] not in stop_list
               and words[i] not in stop_list]


def get_file_buffer(filename):
    with open(filename, 'r') as f:
        buff = f.read()
    return buff


def get_idf(tfs):
    idf = defaultdict(int)
    for tf in tfs:
        for word in tf:
            idf[word] += 1

    logN = log(len(tfs))
    for word in idf:
        idf[word] = logN - log(idf[word])
    return idf


def get_tf_idfs(text_buff, stop_list_file, chunk_size=200,
                n_grams_length=3, result_as_text=True):
    text = text_buff.split(' ')
    texts = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    names = list(range(1, len(texts) + 1))

    stop_list = get_file_buffer(filename=stop_list_file)
    texts = [group_n_grams(words=text[1:],
                           n=n_grams_length,
                           stop_list=stop_list)
             for text in texts]

    tfs = list(map(get_count, texts))
    idf = get_idf(tfs=tfs)

    tf_idfs = []
    for tf in tfs:
        tf_idfs_item = {}
        for word in tf.keys():
            tf_idfs_item[word] = tf[word] * idf[word] / len(tf)
        tf_idfs.append(tf_idfs_item)

    result = []
    for i, tf_idf in enumerate(tf_idfs):
        for word in tf_idf:
            result.append((names[i], word, tf_idf[word]))

    result = sorted(result, key=lambda x: x[2], reverse=True)
    if result_as_text:
        return linesep.join('%s,%s,%f' % r for r in result)
    else:
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ngram_len', type=int, required=True,
                        help='length of n-grams')
    parser.add_argument('--chunk_size', type=int, required=True,
                        help='size of a chunk')
    parser.add_argument('--stop_file', type=str, required=True,
                        help='a filename with a stop word list')
    args = parser.parse_args()

    text_buff = stdin.read()
    print(get_tf_idfs(text_buff=text_buff, stop_list_file=args.stop_file,
                      chunk_size=args.chunk_size, n_grams_length=args.ngram_len))
