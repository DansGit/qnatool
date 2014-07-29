import os


# Pipeline settings
# ==================

# Whether or not to do the processing phase, which
# includes parsing the text with StanfordCoreNLP,
# extracting triplets and filtering out unreliable
# triplets.
do_process = True

# Whether or not to generate network files.
# This is required for making charts.
do_network = True

# Whether or not to generate charts that describe the
# network's properties.
do_charts = True

# How much memory to allow StanfordCoreNLP to use
memory = "3g"


# Filtering Settings
# ==================

# How often a whole triplet needs to be repeated in order to
# considered reliable.
frequency_threshold = 2

# How much more often should an entity (subject or object)
# appear in given data compared to background data AKA
# the 'weight' of the entity.
weight_threshold = 2

# Some words are not found by NER detection but still
# relevant to the narrative. This parameter represents
# how often these unnamed words need to appear in
# the data set to be considered reliable. Usually these
# words are more concepts than actors and are thus
# defined as 'key concepts' later in the pipeline.
# This threshold should be rather large to filter out
# garbage words.
unnamed_threshold = 20


# Network Settings
# ================

# If true, resulting network graph will be largest connected
# component of the graph generated. Setting this to false
# usually results in a graph with one giant cluster and dozens
# of tiny clusters with only 2 or three nodes.
giant = True


# Input/Output Settings.
# Can be set automatically at runtime or here.
# ============================================

source_dir = ''
output_dir = ''
chart_dir = ''
project_name = ''


# Data Settings. Change to overide defaults.
# ==========================================

# Path to the data and temp folders.
# I reccomend you don't change these.
DATA = os.path.abspath('data')
TEMP = os.path.join(DATA, 'temp')

# You may want to have multiple QNATool processes write to a single
# database. In that case, simply provide that database's path
# here and the new data will be appended to it.
DB = ''

# The background database is used to filter out junk words
# and promote words relevant to your research by comparing
# your corpus with a non-relevant corpus.
# For that reason, this database should be generated from
# a set of articles that aren't relevant to your
# work.
BGDB = os.path.join(DATA, 'background.db')
