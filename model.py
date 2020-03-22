import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import mean_absolute_error 
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm 

mae = mean_absolute_error

data = pd.read_csv('./games.csv')

x = data.drop(axis = 1 , columns = ['money'])
y = data['money']

model = SVC(random_state = 0)

print(y.head())

def convert(array):
    array = array.replace("'","")
    array = array.replace(" ", "")
    if(len(array) > 2):
        array = array[1:-1].split(',')
        array_size = len(array) 
    else:
        array_size = 0
    
    saida = []
    dic= {
        'H': 13,
        'DD': 14,
        'P': 15,
        'S': 16,
        'A': 1,
        'J': 10,
        'K': 11,
        'Q': 12
    }
    
    for i in range(11):
        if(i > array_size - 1 or array_size == 0):
            saida.append(0)    
        else:
            try:
                saida.append(dic[array[i]])
            except:
                saida.append(int(array[i]))
    return saida

def preprocess(x,index):
    
    data = []
    
    print('Preprocessing...')
    for i in tqdm(range(index,len(x) + index)):
        vect = []
        for column in x.loc[i]:
            #print(column)
            converted = convert(column)
            vect.append(converted)
            #print(converted)
            
        data.append(vect)
    return data

def accuracy(predicted , real_value,index):

    hits = 0
    i = index
    for prediction in predicted:
        if(prediction == real_value.loc[i]):
            hits += 1
        i+= 1
    return hits/len(real_value)                    

data_train = preprocess(x.loc[0:25000],0)
data_train  = np.array(data_train).reshape(len(data_train),-1)

data_val = preprocess(x.loc[25000:],25000)
data_val = np.array(data_val).reshape(len(data_val),-1)

train_y = y.loc[:25000]
val_y = y.loc[25000:]

model.fit(data_train, train_y)
predction =  model.predict(data_val)
print(mae(predction, val_y))
print(r2_score(predction, val_y))
print(accuracy(predction,val_y,25000))


