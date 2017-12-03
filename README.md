Mambo: Multimodal Biomedical Networks
=====================================

This repository contains a tutorial for [Mambo](http://snap.stanford.edu/mambo) in the form of iPython notebooks. The tutorial shows how to use Mambo to synthesize data from various data sources in order to construct and represent multimodal networks. The repository also contains data, code and other resources necessary to run the tutorial.

![alt text](http://snap.stanford.edu/mambo/mambo-multimodal.png)

Download Materials for This Tutorial
------------------------------------

The Mambo tools and tutorial materials are available in this repository. 

All necessary data for the *multimodal cancer network* example is included in this repository. Data for the *giga-scale multimodal network* example is very large and must be downloaded from external databases. See [Mambo website](http://snap.stanford.edu/mambo) for information on how to access those databases. 

Installation Notes
------------------

This tutorial requires the following installations:

- [IPython](http://ipython.readthedocs.org/en/stable/)
- [Jupyter Notebook](http://jupyter.org)
- [Snap.py](https://snap.stanford.edu/snappy/)


Outline
=======

We start by providing background on multimodal networks, their representations, Mambo system and its workflow:

- [01 Introduction to Multimodal Networks](01%20Introduction%20to%20Multimodal%20Networks.ipynb)
- [02 Data Representation in Mambo](02%20Data%20Representation%20in%20Mambo.ipynb)

We then provide a detailed overview of each step in Mambo workflow. As an example, we construct a multimodal cancer network centered around genes that are frequently mutated in cancer patients:

- [03 Workflow for Constructing a Multimodal Network](03%20Workflow%20for%20Constructing%20a%20Multimodal%20Network.ipynb)
- [04 Creating Mode Tables](04%20Creating%20Mode%20Tables.ipynb)
- [05 Creating Link Tables](05%20Creating%20Link%20Tables.ipynb)
- [06 Constructing a Multimodal Network from Mode and Link Tables](06%20Constructing%20a%20Multimodal%20Network%20from%20Mode%20and%20Link%20Tables.ipynb)
- [07 Loading a Multimodal Network](07%20Loading%20a%20Multimodal%20Network.ipynb)
- [08 Performing Analytics on a Multimodal Network](08%20Performing%20Analytics%20on%20a%20Multimodal%20Network.ipynb)

Finally, we provide a case study that constructs a giga-scale multimodal biological network that has more than two thousand modes, twenty thousand link types, and a total of 3.5 billion edges:

- [09 Giga-Scale Multimodal Biological Network](09%20Giga-Scale%20Multimodal%20Biological%20Network.ipynb)
- [10 Supplementary: Filtering a Giga-Scale Multimodal Biological Network](10%20Supplementary%20-%20Filtering%20a%20Giga-Scale%20Multimodal%20Biological%20Network.ipynb)