import bz2
import pickle

data = bz2.BZ2File("nlp_preprocessing_toolbox/data/freq_dict.pbz2", "rb")
data = pickle.load(data)
freq_dict = data

print(freq_dict)