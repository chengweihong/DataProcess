import sys
import os
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import MiniBatchKMeans, KMeans
import numpy as np
import time
import cPickle
from sklearn.datasets.samples_generator import make_blobs
#test
#np.random.seed(0)
#batch_size = 45
#centers = [[1, 1], [-1, -1], [1, -1]]
#n_clusters = len(centers)
#X, labels_true = make_blobs(n_samples=3000, centers=centers, cluster_std=0.7)
#print X,labels_true,type(X)

#measurements = [{'city': 'Dubai', 'temperature': 33.},{'city':'London', 'temperature': 12.},{'city': 'San Fransisco', 'temperature': 18.}]
print "load sample"
t0 = time.time()
pagefile = file("../page/testpage","r")
pagedict = cPickle.load(pagefile)
t_batch = time.time() - t0
print "load success!time:",t_batch
count = 0
measurements = []
questionid = []
for id,question in pagedict.items():
    tmpdict = {}
    questionid.append(id)
    for word in question["titlevec"]:
        tmpdict[word] = tmpdict.get(word,0)+1
    for word in question["contentvec"]:
        tmpdict[word] = tmpdict.get(word,0)+1
    measurements.append(tmpdict)
print "initial sample set,size:",len(measurements)
#measurements = [{'city': 1.0, 'temperature': 33.},{'city':1.0, 'temperature': 12.},{'city': 2.0, 'temperature': 18.}]
vec = DictVectorizer()
matrix = vec.fit_transform(measurements)
#print type(matrix),vec.get_feature_names()
#print vec.get_params()

k_means = KMeans(init='k-means++', k=300, n_init=10)
t0 = time.time()
k_means.fit(matrix)
t_batch = time.time() - t0
k_means_labels = k_means.labels_
k_means_cluster_centers = k_means.cluster_centers_
k_means_labels_unique = np.unique(k_means_labels)
#print "distance:",k_means.transform(matrix)
#print "cluster info:",t_batch,k_means_labels,k_means_cluster_centers ,k_means_labels_unique
print "cluster cost time:",t_batch
problemdict = {}
for i in range(0,len(k_means_labels)):
    lable = k_means_labels[i]
    id = questionid[i]
    problemdict[lable] = problemdict.get(lable,"") + "\n" + str(lable) + "  : "+ pagedict[id]['title']
clusterfile = file("clusterres","w")
for lable,item in problemdict.items():
    clusterfile.write(item)
clusterfile.close()
    



