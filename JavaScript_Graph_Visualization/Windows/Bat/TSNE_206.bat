@echo off

set PATH = 'E:\Anaconda'

cd ..\Python

python generate_graph_from_datafile_version_0.9_iter_integre.py ^
--input_list "E:\206\list_small_icons.lst" ^
--directory "E:/206" ^
--root_path "DerivedObj/" ^
--input_path "E:\206\206_coordoonees\206_pixels_grey_scat32_100.tsv" ^
--output_path "E:\Dassault\4.14\4.14_Windows\Json\Json_206\206_Random_5_1000_3000_None_50_scat_100_32.json" ^
--perplexity 1 ^
--learning_rate 1000 ^
--init random ^
--n_iter 3000 ^
--step 50

pause

