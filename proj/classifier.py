import numpy as np, pandas as pd, json, os, re, argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from flask import Flask, render_template, redirect, url_for, request, \
    make_response

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main(new=0, filedir=None, data=None):
    print("in main")
    filedir = "dat-jjack5.json"
    print("filedir: ", filedir)
    # fitting new model/predicting using existing one
    flstb = re.search(r'dat-\w*\.json', filedir).group() if filedir else None
    rfc = rforestfit(new, flstb)
    if rfc[1] == True and filedir == None:
        print("Model ready")
        return
    if filedir != None:
        act = re.search(r'-\w*\.', filedir).group()[1:-1]
        with open('data/' + filedir, 'r+') as f:
            dat = json.loads(f.read())
        df = pd.DataFrame(makedat(dat, act))
    else:
        df = pd.DataFrame(data)
    trueclass = df['class']
    df.drop(columns=['class'], inplace=True)
    df['class'] = rfc[0].predict(df)
    df['accurate'] = df['class'] == trueclass
    print(df[df['accurate'] == True]['accurate'].count() / df[
        'accurate'].count())
    return str(df['class'].mode().values[0])


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


def rforestfit(new, flstb):
    print("in rforestfit")
    newModel = True
    if new == 0 and 'moveclass.pkl' in os.listdir():
        rfc = joblib.load('moveclass.pkl')
        newModel = False
    else:
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
        for file in re.findall(r'dat-[\w\d]*\.json',
                               ' '.join(os.listdir('data'))):
            if flstb and file == flstb:
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
