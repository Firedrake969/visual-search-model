import traceback
import sys
import cPickle
import Model1
import scipy.misc
from scipy.ndimage.filters import gaussian_filter
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import ModelOptions1 as opt


reload(opt)
reload(Model1)

# Build filters
s1filters = Model1.buildS1filters()
print 'Loaded s1 filters'
protsfile = open('imgprots.dat', 'rb')
imgprots = cPickle.load(protsfile)
print 'Loading objprots filters'
protsfile = open('gdrivesets/prots/objprots_25.dat', 'rb')
objprots = cPickle.load(protsfile)
for idx, _ in enumerate(objprots):
    objprots[idx] = objprots[idx]
print 'Objprots shape:', len(objprots), objprots[0].shape
protsfile = open('naturalImgC2b.dat', 'rb') # todo ???
imgC2b = cPickle.load(protsfile)
print 'imgC2b: ', len(imgC2b)
imgC2b = imgC2b[0:-1]

# predicted x and y, real x and y
box_radius = 12.0
targetIndex = 0
def check_bounds(px, py, rx, ry):
    bounds = [
        rx - box_radius,
        rx + box_radius,
        ry - box_radius,
        ry + box_radius
    ]
    print x, y, bounds
    return px >= bounds[0] and px <= bounds[1] and py >= bounds[2] and py <= bounds[3]

img = scipy.misc.imread('gdrivesets/scenes/5and2/setsize{}_{}.png'.format(12, 2), mode='I')

S1outputs = Model1.runS1layer(img, s1filters)
C1outputs = Model1.runC1layer(S1outputs)
S2boutputs = Model1.runS2blayer(C1outputs, imgprots)
feedback = Model1.feedbackSignal(objprots, targetIndex, imgC2b)
print 'feedback info: ', feedback.shape
lipmap = Model1.topdownModulation(S2boutputs,feedback)
protID = np.argmax(feedback)
print feedback[protID], np.mean(feedback)
print 'lipmap shape: ', len(lipmap), lipmap[0].shape

priorityMap = Model1.priorityMap(lipmap,[256,256])

# i = 0
# found = False
# while i < 5 and not found:
#     priorityMap, fx, fy = Model1.inhibitionOfReturn(priorityMap)
#     found = check_bounds(fx, fy)
#     i += 1

# print i, found

numCols = 5
numRows = 12

whichgraph = 'ab'


if 'a' in whichgraph:
    fig,ax = plt.subplots(nrows = numRows, ncols = numCols)
    plt.gray()  # show the filtered result in grayscale


    for i in xrange(numRows):
        ax[i,0].imshow(img)

    i = 0
    for scale in S1outputs:
        sif, minV, maxV = Model1.imgDynamicRange(np.mean(scale, axis = 2))
        ax[i,1].imshow(sif)
        i += 1

    i = 0
    for scale in C1outputs:
        cif, minV, maxV = Model1.imgDynamicRange(np.mean(scale, axis = 2))
        ax[i,2].imshow(cif)
        i += 1

    i = 0
    for scale in S2boutputs:
        #s2b, minV, maxV = Model1.imgDynamicRange(np.mean(scale, axis = 2))
        s2b, minV, maxV = Model1.imgDynamicRange(scale[:,:,protID])
        ax[i,3].imshow(s2b)
        i += 1

    i = 0
    for scale in lipmap:
        #lm, minV, maxV = Model1.imgDynamicRange(np.mean(scale, axis = 2))
        lm, minV, maxV = Model1.imgDynamicRange(scale[:,:,protID])  
        ax[i,4].imshow(lm)
        i += 1

    ax[0,0].set_title('Original')
    ax[0,1].set_title('S1')
    ax[0,2].set_title('C1')
    ax[0,3].set_title('S2b')
    ax[0,4].set_title('LIP')

if 'b' in whichgraph:

    fig,ax = plt.subplots(nrows = 1, ncols = 2)
    plt.gray()
    pmap, minV, maxV = Model1.imgDynamicRange(priorityMap)
    dims = pmap.shape
    pmap = Model1.scale(priorityMap)
    for i in xrange(dims[0]):
        for j in xrange(dims[0]):
            tmp = pmap[i,j]
            pmap[i,j]= np.exp(np.exp(tmp))
            # pmap[i,j]= np.exp(np.exp(np.exp(tmp)))
    ax[0].imshow(gaussian_filter(pmap, sigma=3))

    for i in xrange(dims[0]):
        for j in xrange(dims[0]):
            tmp = pmap[i,j]
            pmap[i,j]= np.exp(tmp)
            # pmap[i,j]= np.exp(np.exp(np.exp(tmp)))
    ax[1].imshow(gaussian_filter(pmap, sigma=3))

if 'c' in whichgraph:

    fig,ax = plt.subplots(nrows = numRows, ncols = change)
    plt.gray()  # show the filtered result in grayscale

    for i in xrange(change):
        for j, scale in enumerate(S2boutputs):
            s2b, minV, maxV = Model1.imgDynamicRange(scale[:,:,i])
            ax[j,i].imshow(s2b)


if 'd' in whichgraph:

    fig,ax = plt.subplots(nrows = numRows, ncols = change)
    plt.gray()  # show the filtered result in grayscale
    plt.axis('off')

    for i in xrange(change):
        for j, scale in enumerate(lipmap):
            s2b, minV, maxV = Model1.imgDynamicRange(scale[:,:,i])
            ax[j,i].imshow(s2b)

if 'e' in whichgraph:
    fig,ax = plt.subplots(nrows = numRows, ncols = 3)
    plt.gray()  # show the filtered result in grayscale
    i = 0
    for scale in S2boutputs:
        #s2b, minV, maxV = Model1.imgDynamicRange(np.mean(scale, axis = 2))
        s2b, minV, maxV = Model1.imgDynamicRange(scale[:,:,protID])
        ax[i,0].imshow(np.exp(np.exp(s2b)))
        i += 1
    i = 0
    for scale in modulated_s2boutputs:
        #s2b, minV, maxV = Model1.imgDynamicRange(np.mean(scale, axis = 2))
        s2b, minV, maxV = Model1.imgDynamicRange(scale[:,:,protID])
        ax[i,1].imshow(np.exp(np.exp(s2b)))
        i += 1
    i = 0
    for scale in cropped_s2boutputs :
        #s2b, minV, maxV = Model1.imgDynamicRange(np.mean(scale, axis = 2))
        s2b, minV, maxV = Model1.imgDynamicRange(scale[:,:,protID])
        ax[i,2].imshow(np.exp(np.exp(s2b)))
        i += 1


plt.show()
