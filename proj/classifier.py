import numpy as np, pandas as pd, json, os, re, argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

def makedat(data, act):
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

def rforestfit(new):
	newModel = True
	if new==0 and 'moveclass.pkl' in os.listdir():
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
		print(' '.join(os.listdir()))
		for file in re.search(r'dat-\w*\.json',' '.join(os.listdir())).group():
			act = re.search(r'-\w*\.',file).group()[1:-1]
			with open(file,'r') as f:
				rawdat = json.loads(f.read())
			dat1 = makedat(rawdat,act)
			for key in dat1.keys():
				dat[key].extend(dat1[key])
		df = pd.DataFrame(dat)
		y = df['class']
		X = df.iloc[:,:-1]
		rfc.fit(X,y)
		joblib.dump(rfc, 'moveclass.pkl')
	return (rfc, newModel)

def main():
	#parsing arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-d','--datadir', type=str)
	parser.add_argument('-n','--newtree', type=int, choices=[0,1])
	args = vars(parser.parse_args())
	if not args['datadir'] and not args['newtree']:
		raise Exception('Need file for prediction if not making new tree')
	filedir = args['datadir']
	new = args['newtree']

	#fitting new model/predicting using existing one
	rfc = rforestfit(new)
	if rfc[1]==True and filedir==None:
		return "Model ready"
	act = re.search(r'-\w*\.',filedir).group()[1:-1]
	with open(filedir,'r+') as f:
		dat = json.loads(f.read())
	df = pd.DataFrame(makedat(dat, act))
	df['class'] = rfc[0].predict(df)
	return df

if __name__ == "__main__":
	main()
