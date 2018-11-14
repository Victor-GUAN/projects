# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 17:24:00 2017

@author: MGN11
"""

#import t_sne
#
#from t_sne import *
from optparse import OptionParser
from optparse import OptionGroup



def main():

    #   save and input the parameters in terminal
    
    usage = "usage: %prog [option] arg"
    
    parser = OptionParser(usage)
    
    parser.add_option("--input_list", dest="input_list", help="the initial image id data file", default="E:/206/list_small_icons.lst", metavar="FILE")
    parser.add_option("--directory", dest="directory", help="the directory path for the document of images (without '/' at the end)", default="E:/206", metavar="FILE")
    parser.add_option("--root_path", dest="root_path", help="the parent folder for the images (with a '/' at the end)", default="DerivedObj/", metavar="FILE")
    parser.add_option("--input_path", dest="input_path", help="the initial tsv data file", default="E:/206/206_coordoonees/206_pixels_grey_scat32_100.tsv", metavar="FILE")
    parser.add_option("--output_path", dest="output_path", help="the output path for the final json file", default="E:/Dassault/json/206_PCA_graph.json_version_0.9_iter.json", metavar="FILE")
    
    group = OptionGroup(parser, "Parameters Options",  
                    "Caution: these are the input parameters for TSNE function")  
    
    group.add_option("--perplexity", type="int", dest="perplexity", help="perplexity for TSNE - int", default=30, metavar="INT")
    group.add_option("--learning_rate", type="int", dest="learning_rate", help="learning rate for TSNE which should be between 100 and 1000 - int", default=1000, metavar="INT")
    group.add_option("--init", dest="init", help="Initialization of embedding, possible options are 'random', 'pca', and a numpy array of shape (n_samples, n_components) - string", default="random", metavar="STRING")
    group.add_option("--n_iter", type="int", dest="n_iter", help="Maximum number of iterations for the optimization. Should be at least 200 - int", default=1000, metavar="INT")
    group.add_option("--random_state", type="int", dest="random_state", help=" int or RandomState instance or None, default = 0 - int", default=0, metavar="INT OR NONE")
    group.add_option("--step", type="int", dest="step", help=" the step between the iterations we want to extract - int", default=50, metavar="INT")

    parser.add_option_group(group)
    
    (options, args) = parser.parse_args()
    
    
    """if len(args) == 0:  
        parser.error("incorrect arguments")"""
        
if __name__ == "__main__":
    main()