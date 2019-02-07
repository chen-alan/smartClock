
# coding: utf-8

# # Lab 1: Classification of Car Acitivity via scikit-learn

# ### by Michael Tang, Woorin Jang, Alan Chen

# This is Team 2 (WAM)'s implementation of Lab 1, predicting the type of activity of a car given its trace data. This was implemented by organizing the training set - trace data gathered by the class during lab sessions - into dataframes and creating features to be fed into a K Nearest Neighbors classifier. This classifier was imported from the scikit-learn package, and predicts classification of trace data based on the classifications of its "nearest neighbors". The number of neighbors has been tuned to 5 after testing of what gives the highest accuracy. The features as well have been engineered based on what promotes the most accurate classification. At the end, our predicted classifications for the files we were given are outputted after training the model over all class-given data in the activitydataset folder.

# In[1]:


import numpy as np, pandas as pd, json
from sklearn.neighbors import KNeighborsClassifier


# ## 1. Function to make a dictionary with mean and std for each trace

# In[2]:


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
    


# ## 2. Testing to see how well k-neighbors works

# First, we gather classifications off of a subset of the already labeled datasets provided in /activitydataset. We then test the k-neighbors classifier for accuracy on the cross-validation set, the portion of the dataset not used for training.

# ### Driving

# In[3]:


with open('activity-dataset-team2/activity-team2-Driving-0.txt', 'r') as f:
    dr = json.loads(f.read().replace('\'','\"'))['seq']
with open('activity-dataset-team2/activity-team2-Driving-1.txt', 'r') as f:
    dr.extend(json.loads(f.read().replace('\'','\"'))['seq'])
dr = makedic(dr)
drdf = pd.DataFrame(dr, index=[0])
drdf


# ### Jumping

# In[4]:


with open('activity-dataset-team2/activity-team2-Jumping-0.txt', 'r') as f:
    jp = json.loads(f.read().replace('\'','\"'))['seq']
with open('activity-dataset-team2/activity-team2-Jumping-1.txt', 'r') as f:
    jp.extend(json.loads(f.read().replace('\'','\"'))['seq'])
jp = makedic(jp)
jpdf = pd.DataFrame(jp, index=[0])
jpdf


# ### Standing

# In[5]:


with open('activity-dataset-team2/activity-team2-Standing-0.txt', 'r') as f:
    st = json.loads(f.read().replace('\'','\"'))['seq']
with open('activity-dataset-team2/activity-team2-Standing-1.txt', 'r') as f:
    st.extend(json.loads(f.read().replace('\'','\"'))['seq'])
st = makedic(st)
stdf = pd.DataFrame(st, index=[0])
stdf


# ### Walking

# In[6]:


with open('activity-dataset-team2/activity-team2-Walking-0.txt', 'r') as f:
    wk = json.loads(f.read().replace('\'','\"'))['seq']
with open('activity-dataset-team2/activity-team2-Walking-1.txt', 'r') as f:
    wk.extend(json.loads(f.read().replace('\'','\"'))['seq'])
wk = makedic(wk)
wkdf = pd.DataFrame(wk, index=[0])
wkdf


# ### Adding cumulative data (16-28) to training

# #### Loading cumulative datasets

# In[7]:


with open('activitydataset/activity-dataset-Driving.txt', 'r') as f:
    dr = json.loads(f.read().replace('\'','\"'))
drcum = [] #an array of dictionaries, each dic containing info for one trace
for x in range(20, len(dr)):
    trace = dr[x]['seq']
    drdic = makedic(trace)
    drdic['class'] = 0
    drcum.append(drdic) 
drcumdf = pd.DataFrame(drcum)


# In[8]:


with open('activitydataset/activity-dataset-Jumping.txt', 'r') as f:
    jp = json.loads(f.read().replace('\'','\"'))
jpcum = [] #an array of dictionaries, each dic containing info for one trace
for x in range(20, len(jp)):
    trace = jp[x]['seq']
    jpdic = makedic(trace)
    jpdic['class'] = 1
    jpcum.append(jpdic) 
jpcumdf = pd.DataFrame(jpcum)


# In[9]:


with open('activitydataset/activity-dataset-Standing.txt', 'r') as f:
    st = json.loads(f.read().replace('\'','\"'))
stcum = [] #an array of dictionaries, each dic containing info for one trace
for x in range(20, len(st)):
    trace = st[x]['seq']
    stdic = makedic(trace)
    stdic['class'] = 2
    stcum.append(stdic) 
stcumdf = pd.DataFrame.from_dict(stcum)


# In[10]:


with open('activitydataset/activity-dataset-Walking.txt', 'r') as f:
    wk = json.loads(f.read().replace('\'','\"'))
wkcum = [] #an array of dictionaries, each dic containing info for one trace
for x in range(20, len(wk)):
    trace = wk[x]['seq']
    wkdic = makedic(trace)
    wkdic['class'] = 3
    wkcum.append(wkdic) 
wkcumdf = pd.DataFrame.from_dict(wkcum)


# In[11]:


#attach labels
drdf['class'] = 0
jpdf['class'] = 1
stdf['class'] = 2
wkdf['class'] = 3
#create a super-chungus
df = pd.concat([drcumdf, jpcumdf, stcumdf,wkcumdf],sort=False)
X = df.iloc[:,:-1]
y = df['class']
kn = KNeighborsClassifier(n_neighbors=5).fit(X,y)


# ### Testing k-neighbors with class data (1-14)

# #### Loading cumulative datasets

# In[12]:


drtest = [] #an array of dictionaries, each dic containing info for one trace
for x in range(0, 20):
    trace = dr[x]['seq']
    drdic = makedic(trace)
    drdic['class'] = 0
    drtest.append(drdic) 
drtestdata = pd.DataFrame(drtest)


# In[13]:


jptest = [] #an array of dictionaries, each dic containing info for one trace
for x in range(0,20):
    trace = jp[x]['seq']
    jpdic = makedic(trace)
    jpdic['class'] = 1
    jptest.append(jpdic) 
jptestdata = pd.DataFrame(jptest)


# In[14]:


sttest = [] #an array of dictionaries, each dic containing info for one trace
for x in range(0,20):
    trace = st[x]['seq']
    stdic = makedic(trace)
    stdic['class'] = 2
    sttest.append(stdic) 
sttestdata = pd.DataFrame.from_dict(sttest)


# In[15]:


wktest = [] #an array of dictionaries, each dic containing info for one trace
for x in range(0,20):
    trace = wk[x]['seq']
    wkdic = makedic(trace)
    wkdic['class'] = 3
    wktest.append(wkdic) 
wktestdata = pd.DataFrame.from_dict(wktest)


# In[16]:


test = pd.concat([drtestdata,jptestdata,sttestdata,wktestdata])


# #### Testing on cumulative dataset

# In[17]:


#output: accuracy
print("Cross-validation accuracy: ",len(np.where(test['class']==kn.predict(test.iloc[:,:-1]))[0])/len(test['class']))


# ### Predicting Unknown Traces

# #### First, we re-train our model with the enire class data set.

# In[18]:


with open('activitydataset/activity-dataset-Driving.txt', 'r') as f:
    dr = json.loads(f.read().replace('\'','\"'))
drcum = [] #an array of dictionaries, each dic containing info for one trace
for x in range(0, len(dr)):
    trace = dr[x]['seq']
    drdic = makedic(trace)
    drdic['class'] = 0
    drcum.append(drdic) 
drcumdf = pd.DataFrame(drcum)


# In[19]:


with open('activitydataset/activity-dataset-Jumping.txt', 'r') as f:
    jp = json.loads(f.read().replace('\'','\"'))
jpcum = [] #an array of dictionaries, each dic containing info for one trace
for x in range(0, len(jp)):
    trace = jp[x]['seq']
    jpdic = makedic(trace)
    jpdic['class'] = 1
    jpcum.append(jpdic) 
jpcumdf = pd.DataFrame(jpcum)


# In[20]:


with open('activitydataset/activity-dataset-Standing.txt', 'r') as f:
    st = json.loads(f.read().replace('\'','\"'))
stcum = [] #an array of dictionaries, each dic containing info for one trace
for x in range(0, len(st)):
    trace = st[x]['seq']
    stdic = makedic(trace)
    stdic['class'] = 2
    stcum.append(stdic) 
stcumdf = pd.DataFrame.from_dict(stcum)


# In[21]:


with open('activitydataset/activity-dataset-Walking.txt', 'r') as f:
    wk = json.loads(f.read().replace('\'','\"'))
wkcum = [] #an array of dictionaries, each dic containing info for one trace
for x in range(0, len(wk)):
    trace = wk[x]['seq']
    #print(trace)
    wkdic = makedic(trace)
    wkdic['class'] = 3
    wkcum.append(wkdic) 
wkcumdf = pd.DataFrame.from_dict(wkcum)


# In[22]:


#attach labels
drdf['class'] = 0
jpdf['class'] = 1
stdf['class'] = 2
wkdf['class'] = 3
#create a super-chungus
df = pd.concat([drcumdf, jpcumdf, stcumdf,wkcumdf],sort=False)
X = df.iloc[:,:-1]
y = df['class']
kn = KNeighborsClassifier(n_neighbors=5).fit(X,y)


# #### Next, we attempt to predict activity for each unknown trace:

# In[23]:


print("Classifications for test files:")
clkey = {0:'driving',1:'jumping',2:'standing',3:'walking'}


# ##### Unknown #1

# In[24]:


with open('activity-test-dataset/team2_1.txt', 'r') as f:
    unknown_trace = json.loads(f.read().replace('\'','\"'))
    
unknwn= []
unknwn_dic = makedic(unknown_trace['seq'])
unknwn_dic['class']=-1
unknwn.append(unknwn_dic)
unk = pd.DataFrame.from_dict(unknwn)
print("team2_1.txt: ",clkey[kn.predict(unk.iloc[:,:-1])[0]])


# #### Unknown #2

# In[25]:


with open('activity-test-dataset/team2_2.txt', 'r') as f:
    unknown_trace = json.loads(f.read().replace('\'','\"'))
    
unknwn= []
unknwn_dic = makedic(unknown_trace['seq'])
unknwn_dic['class']=-1
unknwn.append(unknwn_dic)
unk = pd.DataFrame.from_dict(unknwn)
print("team2_2.txt: ",clkey[kn.predict(unk.iloc[:,:-1])[0]])


# #### Unknown #3

# In[26]:


with open('activity-test-dataset/team2_3.txt', 'r') as f:
    unknown_trace = json.loads(f.read().replace('\'','\"'))
    
unknwn= []
unknwn_dic = makedic(unknown_trace['seq'])
unknwn_dic['class']=-1
unknwn.append(unknwn_dic)
unk = pd.DataFrame.from_dict(unknwn)
print("team2_3.txt: ",clkey[kn.predict(unk.iloc[:,:-1])[0]])


# #### Unknown #4

# In[27]:


with open('activity-test-dataset/team2_4.txt', 'r') as f:
    unknown_trace = json.loads(f.read().replace('\'','\"'))
    
unknwn= []
unknwn_dic = makedic(unknown_trace['seq'])
unknwn_dic['class']=-1
unknwn.append(unknwn_dic)
unk = pd.DataFrame.from_dict(unknwn)
print("team2_4.txt: ",clkey[kn.predict(unk.iloc[:,:-1])[0]])

