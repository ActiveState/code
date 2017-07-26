## Artificial Neuroglial Network (ANGN)   
Originally published: 2012-08-16 17:21:51  
Last updated: 2012-10-02 16:18:36  
Author: David Adler  
  
This is an attempt at emulating the algorithm from these scientific articles:
1. [2011 - Artificial Astrocytes Improve Neural Network Performance](http://www.hindawi.com/journals/cmmm/2012/476324/ )
2. [2012 - Computational Models of Neuron-Astrocyte Interactions Lead to Improved Efficacy in the Performance of Neural Networks](http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0019109)


The objective of the program is to train a neural network to classify the four inputs (the dimensions of a flower) into one of three categories (three species of flower),  (taken from the [Iris Data Set](http://archive.ics.uci.edu/ml/datasets/Iris) from the UCI Machine Learning Repository). This program has two learning phases: the first is a genetic algorithm (supervised), the second is a neuroglial algorithm (unsupervised). This ANGN is a development of a previous program only consisting of a genetic algorithm which can be found [here](http://code.activestate.com/recipes/578241-genetic-algorithm-neural-network-in-python-source-/).

The second phase aims to emulate astrocytic interaction with neurons in the brain. The algorithm is based on two axioms: a) astrocytes are activated by persistent neuronal activity b) astrocytic effects occur over a longer time-scale than neurons. Each neuron has an associated astrocyte which counts the number of times its associated neuron fires (+1 for active -1 for inactive). If the counter reaches its threshold (defined as `Athresh`) the astrocyte is activated and for the next x iterations (defined as `Adur`) the astrocyte modifies the incoming weights to that particular neuron. If the counter reached a maximum due to persistent firing the incoming weights are increase by 25% for the proceeding `Adur` iterations; conversely if the counter reached a minimum due to persistent lack of firing the weights are decreased by 50% for the following `Adur` iterations). For a detailed description of the algorithm see the linked articles. For a general understanding of how this program was coded look at the pseudo-code/schematic [here](http://commons.wikimedia.org/wiki/File:ANGN_schematic.png).

Any comments for improvements are welcome. There are several issues in this program which require addressing, please scroll down below code to read about these issues.