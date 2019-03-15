import numpy as np, pandas as pd, json, os, re, argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from flask import Flask, render_template, redirect, url_for, request, \
    make_response
import time

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main(new=0, filedir=None, data=None):
    start = time.time()
    print("in main")

    #receiving data from mobile
    data = ""
    if request.method == 'POST':
        d = request.form.to_dict()
        for i in d:
            data += i
    data = json.loads(data)

    #if filedir specified:
    #filedir = 'dat-act18.json'
    print("filedir: ", filedir)
    # fitting new model/predicting using existing one
    flstb = re.search(r'dat-\w*\.json', filedir).group() if filedir else None

    #calling for model. switch to rforestfit(1, flstb) if want to train, filedir must be provided so flstb = None
    rfc = rforestfit(0, flstb)

    #training mode: model fit, no prediction needed
    if rfc[1] == True and filedir == None:
        print("Model ready")
        return

    #file of training data given
    if filedir != None:
        act = re.search(r'-\w*\.', filedir).group()[1:-1]
        with open('data/' + filedir, 'r+') as f:
            dat = json.loads(f.read())
        df = pd.DataFrame(makedat(dat, act))
    #when data is received over network from mobile and not from file
    else:
        df = pd.DataFrame(makedat(data))

    #prediction, and accuracy reading in training mode
    #trueclass = df['class']
    #df.drop(columns=['class'], inplace=True)
    df['class'] = rfc[0].predict(df)
    #df['accurate'] = df['class'] == trueclass
    #print(df[df['accurate'] == True]['accurate'].count() / df[
       # 'accurate'].count())
    end = time.time()
    print('time taken:')
    print(end - start)

    #returning mode (majority classification) of classifications for all datapoints given
    return str(df['class'].mode().values[0])

#data formatting helper
def makedat(data, act=None):
    print("in makedat")
    xAccl, yAccl, zAccl, xRot, yRot, zRot, xRotVel, yRotVel, zRotVel = ([] for
                                                                        _ in
                                                                        range(
                                                                            9))
    vals = [xAccl, yAccl, zAccl, xRot, yRot, zRot, xRotVel, yRotVel, zRotVel]
    for x in range(len(data)):
        xAccl.append(data[x]['acceleration']['x'])
        yAccl.append(data[x]['acceleration']['y'])
        zAccl.append(data[x]['acceleration']['z'])
        xRot.append(data[x]['rotation']['beta'])
        yRot.append(data[x]['rotation']['gamma'])
        zRot.append(data[x]['rotation']['alpha'])
        xRotVel.append(data[x]['rotationRate']['beta'])
        yRotVel.append(data[x]['rotationRate']['gamma'])
        zRotVel.append(data[x]['rotationRate']['alpha'])
    # for xAccl
    """tracedata = {'xAmean':np.mean(xAccl), 'xAstd': np.std(xAccl), 'xAmax': np.max(xAccl), 'xAmin': np.min(xAccl),
                'yAmean':np.mean(xAccl), 'yAstd': np.std(yAccl), 'yAmax': np.max(yAccl), 'yAmin': np.min(yAccl),
                'zAmean':np.mean(zAccl), 'zAstd': np.std(zAccl), 'zAmax':np.max(zAccl), 'zAmin': np.min(zAccl),
                'xRmean':np.mean(xRot), 'xRstd': np.std(xRot),
                'yRmean':np.mean(yRot), 'yRstd': np.std(yRot),
                'zRmean':np.mean(zRot), 'zRstd': np.std(zRot),
                'xRVmean':np.mean(xRotVel), 'xRVstd': np.std(xRotVel),
                'yRVmean':np.mean(yRotVel), 'yRVstd': np.std(yRotVel),
                'zRVmean':np.mean(zRotVel), 'zRVstd': np.std(zRotVel)}"""
    tracedata = {'xAccl': xAccl, 'yAccl': yAccl, 'zAccl': zAccl, 'xRot': xRot,
                 'yRot': yRot, 'zRot': zRot, 'xRotVel': xRotVel,
                 'yRotVel': yRotVel, 'zRotVel': zRotVel}
    if act != None:
        tracedata['class'] = [1 for _ in
                              range(len(data))] if 'jjack' in act else [0 for _
                                                                        in
                                                                        range(
                                                                            len(
                                                                                data))]
    # for key in tracedata.keys():
    #	tracedata[key] = [tracedata[key]]
    return tracedata

#model creation and fitting
def rforestfit(new, flstb):
    print("in rforestfit")
    newModel = True
    #if new model not needed, load previously trained model from pickle file
    if new == 0 and 'moveclass.pkl' in os.listdir():
        rfc = joblib.load('moveclass.pkl')
        newModel = False

    else: #new model needed
        rfc = RandomForestClassifier()
        """dat = {'xAmean':[], 'xAstd': [], 'xAmax': [], 'xAmin': [],
                'yAmean':[], 'yAstd': [], 'yAmax': [], 'yAmin': [],
                'zAmean':[], 'zAstd': [], 'zAmax':[], 'zAmin': [],
                'xRmean':[], 'xRstd': [],
                'yRmean':[], 'yRstd': [],
                'zRmean':[], 'zRstd': [],
                'xRVmean':[], 'xRVstd': [],
                'yRVmean':[], 'yRVstd': [],
                'zRVmean':[], 'zRVstd': [], 'class': []}"""
        dat = {'xAccl': [], 'yAccl': [], 'zAccl': [], 'xRot': [], 'yRot': [],
               'zRot': [], 'xRotVel': [], 'yRotVel': [], 'zRotVel': [],
               'class': []}

        #reading all training files, must be provided in directory "./data"
        for file in re.findall(r'dat-[\w\d]*\.json',
                               ' '.join(os.listdir('data'))):
            if flstb and flstb == file:
                continue
            act = re.search(r'-[\w\d]*\.', file).group()[1:-1]
            with open('data/' + file, 'r') as f:
                rawdat = json.loads(f.read())
            dat1 = makedat(rawdat, act=act)
            for key in dat1.keys():
                dat[key].extend(dat1[key])
        df = pd.DataFrame(dat)
        y = df['class']
        X = df.iloc[:, :-1]
        rfc.fit(X, y)
        joblib.dump(rfc, 'moveclass.pkl')
    return (rfc, newModel)


#for command line running outside of flask
if __name__ == "__main__":
    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datadir', type=str)
    parser.add_argument('-n', '--newtree', type=int, choices=[0, 1], default=0)
    args = vars(parser.parse_args())
    if not args['datadir'] and not args['newtree']:
        raise Exception('Need file for prediction if not making new tree')
    filedir = args['datadir']
    new = args['newtree']
    # print(main(new, filedir))
    print("start here")
    print(main(new=0, filedir="dat-jjack5.json"))
    app.run(debug=True)
