from scipy import stats
import numpy as np
import json

datatypes = ['5and2', 'conjunction', 'blackandwhite']

statsdata = {}

def zscore(x, mu, sigma):
    return (x - mu)/float(sigma)

def twoz(d1, d2):
    num = (np.mean(d1) - np.mean(d2))
    denom = np.sqrt((np.var(d1)/len(d1)) + (np.var(d2)/len(d2)))
    print num, denom
    return num/denom

for datatype in datatypes:
    with open('fixationjson/{}_final.json'.format(datatype), 'rb') as f:
        model_data = json.load(f)

    with open('humandata/{}.json'.format(datatype), 'rb') as f:
        human_data = json.load(f)

    sizes = [('3'), ('6'), ('12'), ('18')]

    statsdata[datatype] = {}

    for size in sizes:
        if datatype == datatypes[0]:
            print datatype, size
            print stats.norm.interval(0.95, loc=np.mean(np.array(human_data[size])), scale=np.std(human_data[size]))
            # print np.mean(np.array(model_data[size])*250.0)
            print np.mean(human_data[size])
            # print np.std(np.array(model_data[size])*250.0)
            # print np.std(human_data[size])
            z = zscore(np.mean(np.array(model_data[size])*250.0), np.mean(human_data[size]), np.std(human_data[size]))
            if z > 0:
                z = -z
            print stats.norm.cdf(z)*2.0
            z = twoz(np.array(model_data[size])*250.0, human_data[size])
            if z > 0:
                z = -z
            print stats.norm.cdf(z)*2.0
            print len(np.array(model_data[size])*250.0)
            print len(human_data[size])
            print ''
        statsdata[datatype][size] = stats.ttest_ind(np.array(model_data[size])*250.0, human_data[size], equal_var=False)[1]
        # statsdata[datatype][size] = stats.ttest_1samp(np.array(model_data[size])*250.0, np.mean(human_data[size]))[1]

with open('stats.json', 'wb') as f:
    json.dump(statsdata, f, indent=4)