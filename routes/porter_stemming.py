from nltk.tokenize import sent_tokenize, word_tokenize 
import warnings 
  
warnings.filterwarnings(action = 'ignore') 
  
import gensim 
from gensim.models import Word2Vec 
  
#  Reads ‘alice.txt’ file 
sample = "google facebook google facebook apple linear come store net"

  
# Replaces escape character with space 

data = sample.split(' ')
  
print(data[vocabulary])

  
# Create CBOW model 
model1 = gensim.models.Word2Vec(data, min_count = 1, size = 9, window = 5) 
print(model1.__dict__)

model1.similarity('google', 'facebook')
      
# print("Cosine similarity between 'alice' " +
#                  "and 'machines' - CBOW : ", 
#       model1.similarity('alice', 'machines')) 
  
# # Create Skip Gram model 
# model2 = gensim.models.Word2Vec(data, min_count = 1, size = 100, 
#                                              window = 5, sg = 1) 
  
# # Print results 
# print("Cosine similarity between 'alice' " +
#           "and 'wonderland' - Skip Gram : ", 
#     model2.similarity('alice', 'wonderland')) 
      
# print("Cosine similarity between 'alice' " +
#             "and 'machines' - Skip Gram : ", 
#       model2.similarity('alice', 'machines')) 