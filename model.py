import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error 
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm 

mae = mean_absolute_error

data = pd.read_csv('./games.csv')

x = data.drop(axis = 1 , columns = ['money'])
y = data['money']

def preprocess(x):
    
    print('Preprocessing...')
    for i in tqdm(range(len(x))):
        vect = []
        for column in x.loc[i]:
            vect.append(hash(column))
            
        x.loc[i] = vect
preprocess(x)

print(x.head())

model = DecisionTreeRegressor(random_state = 0, max_leaf_nodes = 30)

train_x , val_x , train_y, val_y = train_test_split(x, y, test_size= 0.15)
model.fit(train_x, train_y)
predction =  model.predict(val_x)
print(mae(predction, val_y))
print(r2_score(predction, val_y))


