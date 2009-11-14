#!/usr/bin/python

from pprint import pprint
from scipy import *

"""------------------------------------------------	
	read_pwd_anatomy:

		args:
			PATH:							string path of desired anatomy file
			?include_vision:	include vision neurons in result?

		returns:
			numpy.array matrix representation of anatomy
			
------------------------------------------------"""
def read_pwd_anatomy(PATH, include_vision=False):
	INFILE = open(PATH, "r")
	lines = INFILE.readlines()
	INFILE.close()
	if not include_vision:
		lastVisionNeuron = int((lines[0])[-2:-1])
	else:
		lastVisionNeuron = 0
	lines = lines[(lastVisionNeuron+1):]
	for i in range(len(lines)):
		lines[i] = map(float, lines[i].split()[lastVisionNeuron:-1])
	return(array(lines))


"""------------------------------------------------	
	nodes_near:

		args:
			nodes:			list of indexes of nodes
			matrix:			numpy.array matrix representation of anatomy
			maxdist:		integer value. depth to search
			thresh:			

		returns:
			numpy.array matrix representation of anatomy

------------------------------------------------"""
def nodes_near_helper(d, node, dists, matrix):
	dists[node] = d
	#print(dists)
	if d-1 < 0:
		return
	i = 0
	for connection in matrix[node]:
		if connection != 0 and dists[i] < d-1:
				#print("Going to node "+str(i))
				nodes_near_helper(d-1, i, dists, matrix)
		i = i + 1
	return

def nodes_near(nodes, matrix, maxdist, thresh=0.5):
	matrix = matrix.tolist()
	dists = [-2]*len(matrix)
	for n in nodes:
		nodes_near_helper(maxdist, n, dists, matrix)
	ans=0
	for d in dists:
		if d > -2:
			ans = ans + 1
	ans = ans - len(nodes)
	return ans
	
	
	
	
	

if __name__ == '__main__':
	m = read_pwd_anatomy("brainAnatomy_62_incept.txt", include_vision=True)
#	print("\nTesting read_pwd_anatomy:\n\n"+str(m)+"\n\n")
	'''
	m = [[0, 0, 0.4, 0.4, 0, 0],
			 [1, 0, 0.6, 0.2, 1, 0],
			 [0, 2, 4, 0.1, 0.1, 0.5],
			 [0.1, 0.1, 0.1, 0.1, 0.5, 0.4],
			 [0, 0, 0, 0, 0, 0],
			 [1, 1, 0, 1, 0, 0]]
	'''

	#m = matrix(m)
	#n = nodes_near([0], m, 3 )
	#print("\nTesting nodes_near:\n\n"+str(n)+"\n")
			
	####################################################################################################	
	# MODIFIED VIRGIL ALGORITHM TO FIND ALL NODES WITHIN MAX_DISTANCE from START_NODES
	####################################################################################################
	START_NODES = [2,3]
	MAX_DISTANCE = 2
	THRESHOLD = 0.00


	# print the original matrix
	print m
	m = matrix( abs(m) > THRESHOLD, dtype=int )
	# print the matrix with the non-zeros set to 1
	print m
#	pprint( m )	



	v = zeros( (m.shape[0],1), dtype=int ); v[START_NODES] = 1
	connected = []

	for i in range(MAX_DISTANCE):
		print "depth %s START:\t %s" % (i+1, v.T )
		v = m*v
		indices = v.nonzero()[0].tolist()[0]

		print "depth %s END:  \t %s -- adding indices=%s" % (i+1, v.T, indices)

		# append to our list of connected_nodes, uniqueify
		connected = list(set( connected+indices ))
	
	print "nodes %(connected)s are connected within %(MAX_DISTANCE)s steps from nodes %(START_NODES)s" % locals()

	####### VIRGIL ALGORITHM ENDS HERE #####################################