import numpy as np, pandas as pd, json, os, re, argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

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

def rforestfit():
	newModel = True
	if 'moveclass.pkl' in os.listdir():
		rfc = joblib.load('moveclass.pkl')
		newModel = False
	else:
		rfc = RandomForestClassifier()
		dat = {'xAmean':[], 'xAstd': [], 'xAmax': [], 'xAmin': [],
				'yAmean':[], 'yAstd': [], 'yAmax': [], 'yAmin': [],
            	'zAmean':[], 'zAstd': [], 'zAmax':[], 'zAmin': [],
            	'xGmean':[], 'xGstd': [], 
            	'yGmean':[], 'yGstd': [], 
            	'zGmean':[], 'zGstd': [], 'class': []}
		for file in re.match(r'dat.*\.json',' '.join(os.listdir())).group():
			act = re.search(r'-\w*-').group().strip('-')
			with open(file,'r') as f:
				rawdat = json.loads(f.read())
			dat1 = makedf(rawdat,act)
			for key in dat1.keys():
				dat[key].extend(dat1[key])
		df = pd.DataFrame(dat)
		y = df['class']
		X = df.iloc[:,:-1]
		rfc.fit(X,y)
		joblib.dump(rfc, 'moveclass.pkl')
	return (rfc, newModel)

def main(filedir):
	rfc = rforestfit()
	if rfc[1]==True:
		return "Model ready"
	with open(filedir,'r+') as f:
		dat = json.loads(f.read())
		df = pd.DataFrame(dat)
	df['class'] = rfc[0].predict(df)
	return df

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.addArgument('datadir', type=str)
	args = parser.parse_args()
	filedir = vars(args)['datadir']
	return main(filedir)
