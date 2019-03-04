import numpy as np, pandas as pd, json
from sklearn.neighbors import KNeighborsClassifier

def makedic(arr):
    xAccl, yAccl, zAccl, xGyro, yGyro, zGyro, xMag, yMag, zMag = ([] for i in range(9))
    vals = [xAccl, yAccl, zAccl, xGyro, yGyro, zGyro, xMag, yMag, zMag]
    for x in range(0, len(arr)):
        xAccl.append(arr[x]['data']['xAccl'])
        yAccl.append(arr[x]['data']['yAccl'])
        zAccl.append(arr[x]['data']['zAccl'])
        xGyro.append(arr[x]['data']['xGyro'])
        yGyro.append(arr[x]['data']['yGyro'])
        zGyro.append(arr[x]['data']['zGyro'])
        xMag.append(arr[x]['data']['xMag'])
        yMag.append(arr[x]['data']['yMag'])
        zMag.append(arr[x]['data']['zMag'])
    #for xAccl
    tracedata = {'xAmean':np.mean(xAccl), 'xAstd': np.std(xAccl), 'xAmax': np.max(xAccl), 'xAmin': np.min(xAccl),
                'yAmean':np.mean(xAccl), 'yAstd': np.std(yAccl), 'yAmax': np.max(yAccl), 'yAmin': np.min(yAccl),
                'zAmean':np.mean(zAccl), 'zAstd': np.std(zAccl), 'zAmax':np.max(zAccl), 'zAmin': np.min(zAccl),
                'xGmean':np.mean(xGyro), 'xGstd': np.std(xGyro), 
                'yGmean':np.mean(yGyro), 'yGstd': np.std(yGyro), 
                'zGmean':np.mean(zGyro), 'zGstd': np.std(zGyro),
                'xMmean':np.mean(xMag), 'xMstd': np.std(xMag),
                'yMmean':np.mean(yMag), 'yMstd': np.std(yMag), 
                'zMmean':np.mean(zMag), 'zMstd': np.std(zMag)} 
    return tracedata

