#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import stdin
import argparse

from graph_tool.all import *
from tf_idf_ngramm import get_tf_idfs


def get_valuable(text_buff, n_grams_length, stop_list_file):
    words = get_tf_idfs(text_buff=text_buff,
                        stop_list_file=stop_list_file,
                        n_grams_length=n_grams_length,
                        result_as_text=False)

    return [word for word in words if word[0] == 1]


def get_valuable_words(text_buff, stop_list_file):
    return get_valuable(text_buff, 1, stop_list_file)


def get_bigram(text_buff, stop_list_file):
    return get_valuable(text_buff, 2, stop_list_file)


def get_threegram(text_buff, stop_list_file):
    return get_valuable(text_buff, 3, stop_list_file)


def get_connected(word, gram):
    return [g for g in gram if word[1] in g[1]]


def make_graph(text_buff, stop_list_file, output_file):
    words = get_valuable_words(text_buff, stop_list_file)
    bi = get_bigram(text_buff, stop_list_file)
    three = get_threegram(text_buff, stop_list_file)

    g = Graph()
    v_word = g.new_vertex_property("string")
    v_tfidf = g.new_vertex_property("int")
    for word in words:
        v = g.add_vertex()
        v_word[v] = word[1]
        v_tfidf[v] = int(word[2] * 10)
        for b_w in get_connected(word, bi):
            b = g.add_vertex()
            g.add_edge(v, b)
            v_word[b] = b_w[1]
            v_tfidf[b] = int(b_w[2] * 10)
        for t_w in get_connected(word, three):
            t = g.add_vertex()
            g.add_edge(v, t)
            v_word[b] = t_w[1]
            v_tfidf[b] = int(t_w[2] * 10)

    graph_draw(g, vertex_text=v_word, vertex_size=v_tfidf, vertex_font_size=10,
               output_size=(5000, 5000), output=output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stop_file', type=str, required=True,
                        help='a filename with a stop word list')
    parser.add_argument('--output_file', type=str, required=True,
                        help='output filename')
    args = parser.parse_args()

    text_buff = stdin.read()
    make_graph(text_buff=text_buff,
               stop_list_file=args.stop_file,
               output_file=args.output_file)
