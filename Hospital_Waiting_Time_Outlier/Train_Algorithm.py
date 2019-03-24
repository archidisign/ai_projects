import os
import BuildMatrices
from sklearn import cross_validation
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import pickle
import warnings
import copy
from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error

### This script is responsible for calling the data extraction script and matrix builder script in order to create the models for each stage.
### The models are then pickled so that they can easily be accessed later on

# load the dictionary of sparse matrices as well as the column dictionary
dat,col = BuildMatrices.build_matrices('devAEHRA')
print('\n')
print('***************************************************************')
print('*                   Creating and Saving Models                *')
print('***************************************************************\n')

#Loop through the dictionary of sparse matrices to create and save models so that they can be called when a prediction will be needed
for key in dat: 
    if key == 'RFT': #We are not interested in the Ready For Treatment Stage so we discard that
        continue
    print('Building Model for ' + key + '... ', end='')

    #Testing the algorithm with Cross Validation. Here we set the training and testing sets with a 9:1 ratio
    X = dat[key][:,0:-1]
    y = dat[key][:,-1]
    X = X.astype( np.float32 )
    #--offset = int( X.shape[0] * 0.8 )
    #--X_train, y_train = X[:offset], y[:offset]
    #--X_test, y_test = X[offset:], y[offset:]

    # Create model for each stage. I used the Gradient Bossting Regressor algorithm since it gave me the best results.
    temp = GradientBoostingRegressor(loss = 'lad',n_estimators=100)
    model = temp.fit(X, y)

    # save each model in a encoded pickle file named by the key
    file = open(os.path.abspath(key)+'.pkl','wb')
    pickle.dump(model,file)
    file.close()
    # save the column dictionary (dictionary that has all the features for each key)
    file = open(os.path.abspath("columndictionary.pkl"),'wb')
    pickle.dump(col,file)
    file.close()
    
    print('Done')

    # The following code is for observational purposes only. It gives a rough approximation of the performance for each model by returning
    # the absolute mean error. This is useful for research purposes and hence is disactivated for server training purposes.
    scores = cross_validation.cross_val_score(model, X, y, cv=50, scoring = 'mean_absolute_error')
    mean_abs_err = np.abs(np.mean(scores))
    #print('Mean absolute error: %.4f ' %(mean_abs_err))
    #The mean score and the 95% confidence interval of the score estimate
    #print("Standard Deviation: %0.4f" % (scores.std()))
    #--mse = mean_squared_error( y_test, temp.predict( X_test ))
    #--print( "MSE: %.4f\n" % mse )

print('\nThe algorithm has been successfully trained')
print('use the "predictor.py" script to make predictions')
    

# A little function forprinting purposes. Gives the console a better look.
def print_status(done,key):
    if done:
        print('Building Model for ' + key + '... Done')
    else:
        print('Building Model for ' + key + '...')       
