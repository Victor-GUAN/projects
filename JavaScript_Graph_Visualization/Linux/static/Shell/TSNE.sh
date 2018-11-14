#! /bin/bash
cd ../Python

sudo python "generate_graph_from_datafile_version_0.9_iter_integre.py" \
--input_list "/home/share/Graph Visualization Tool/data/Buggy/buggy_small_icons.lst" \
--directory "/home/share/Graph Visualization Tool/data" \
--root_path "Buggy/" \
--input_path "/home/share/Graph Visualization Tool/DerivedObjects_pixels_grey_scat_100_32.tsv" \
--output_path "/home/share/4.11/templates/Json/Buggy_PCA_10_150_3000_None_50_scat_100_32.json" \
--perplexity 10 \
--learning_rate 150 \
--init "pca" \
--n_iter 3000 \
--step 50

