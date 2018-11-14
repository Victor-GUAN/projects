@echo off

set PATH = 'E:\Anaconda'

cd ..\Python

python generate_graph_from_datafile_version_0.9_iter_integre.py ^
--input_list E:/Buggy/buggy_small_icons.lst ^
--directory "E:/Graph Visualization Tool/data" ^
--root_path Buggy/ ^
--input_path \\LW5-MBS3-DSY\apprentissage\Victor\experiments\embedding-projector-standalone-master\oss_data\DerivedObjects_pixels_grey_scat_100_32.tsv ^
--output_path "E:\Dassault\4.14\4.14_Windows\Json\Json_Buggy\Buggy_PCA_1_1000_3000_None_50_scat_100_32.json" ^
--perplexity 1 ^
--learning_rate 1000 ^
--init pca ^
--n_iter 3000 ^
--step 50

pause

