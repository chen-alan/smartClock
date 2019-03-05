import numpy as np, pandas as pd, json, os, re
from sklearn.ensemble import RandomForestClassifier

def makedf(data, act):
    xAccl, yAccl, zAccl, xGyro, yGyro, zGyro, xMag, yMag, zMag = ([] for _ in range(9))
    vals = [xAccl, yAccl, zAccl, xGyro, yGyro, zGyro, xMag, yMag, zMag]
    for x in range(len(arr)):
        xAccl.append(arr[x]['xAccl'])
        yAccl.append(arr[x]['yAccl'])
        zAccl.append(arr[x]['zAccl'])
        xGyro.append(arr[x]['xGyro'])
        yGyro.append(arr[x]['yGyro'])
        zGyro.append(arr[x]['zGyro'])
    #for xAccl
    tracedata = {'xAmean':np.mean(xAccl), 'xAstd': np.std(xAccl), 'xAmax': np.max(xAccl), 'xAmin': np.min(xAccl),
                'yAmean':np.mean(xAccl), 'yAstd': np.std(yAccl), 'yAmax': np.max(yAccl), 'yAmin': np.min(yAccl),
                'zAmean':np.mean(zAccl), 'zAstd': np.std(zAccl), 'zAmax':np.max(zAccl), 'zAmin': np.min(zAccl),
                'xGmean':np.mean(xGyro), 'xGstd': np.std(xGyro), 
                'yGmean':np.mean(yGyro), 'yGstd': np.std(yGyro), 
                'zGmean':np.mean(zGyro), 'zGstd': np.std(zGyro), 'class': [act for _ in range(len(arr))]}
    return tracedata

if __name__ == "__main__":
	rfc = RandomForestClassifier(warm_start = True)
	dat = {'xAmean':[], 'xAstd': [], 'xAmax': [], 'xAmin': [],
			'yAmean':[], 'yAstd': [], 'yAmax': [], 'yAmin': [],
            'zAmean':[], 'zAstd': [], 'zAmax':[], 'zAmin': [],
            'xGmean':[], 'xGstd': [], 
            'yGmean':[], 'yGstd': [], 
            'zGmean':[], 'zGstd': [], 'class': []}
	for file in re.match(r'dat.*\.json',' '.join(os.listdir())).group():
		act = re.search(r'-\w*-').group().strip('-')
		with f as open(file,'r'):
			rawdat = json.loads(f.read())
		dat1 = makedf(rawdat)
		for key in dat1.keys():
			dat[key].extend(dat1[key])
	df = pd.DataFrame(dat)
	y = df['class']
	X = df.iloc[:,:-1]
	rfc.fit(X,y)