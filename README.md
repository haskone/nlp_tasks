##Usage:

./filter.pl data/texts/some_text.txt | ./tf_idf_ngramm.py --ngram_len 2 --chunk_size 200 --stop_file data/stop_list/stop_list.txt > res.csv

./filter.pl data/texts/some_text.txt | ./tf_idf_visualizator.py --stop_file data/stop_list/stop_list.txt --output_file output.png