import torch
import torch.nn as nn
from collections import Counter

# Could be speed up with similarity search, or by learning just the Top highest probability/confidence keys/values(or both).
# We could track which key-value pairs have been learned(with a list of counters or the Counter object) and use that to tell how surprised the network is to see a particular query.
#   That could be very useful in Reinforcement Learning(as curiosity value) or Classification to detect which class has not been learned.
# In Reinforcemenet learning the count of 0 would represent the highest/maximum curiosity value. That would represent a state(or location) that has not been visited.

class NeuralDictionary(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 500 keys each of size 100
        self.keys = nn.Parameter(torch.randn(500, 100, dtype=torch.double))
        
        # 500 values each of size 4
        self.values = nn.Parameter(torch.randn(500, 4, dtype=torch.double))

        # to track and later see how many times a key has been chosen as the most important one(the key with the highest confidence)
        self.meta = Counter()

    def forward(self, query):
        attention = torch.matmul(self.keys, query)
        attention = torch.softmax(attention, 0)
        out = torch.matmul(attention, self.values)
        out = torch.sigmoid(out)
        
        amax = torch.argmax(attention)
        self.meta.update(f'{amax}')
        #print(self.meta.most_common(10))
      
        # output is size 4
        return out
    
