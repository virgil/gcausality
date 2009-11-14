#!/usr/bin/python
from pprint import pprint
from numpy import array, matrix, exp, pi, sqrt, mean, round, random
import rpy2
from copy import copy
from pw_critter import pw_critter

#####################################################
#INPUT_FILENAME = 'brainFunction_157.txt'
INPUT_FILENAME = 'brainAnatomy_62_incept.txt'
INPUT_FILENAME2 = None
NUM_STEPS_TO_BACKTRACE = 3

# Apply gaussian blur to the neurons to make them model'able by linear regression
# See wikipedia for the equation
APPLY_GAUSSIAN_NOISE_TO_ALL_NEURONS = False

# don't change this unless you know what you're doing
GAUSSIAN_NOISE_SIGMA = 0.1

###############################################################
# handy functions
###############################################################
def gaussian_noise( sigma, the_shape=None ):
	'''applies random (gaussian) noise to x to make it model'able by linear regression
	(linear regression assumes linearity of the signal)
	there are better ways to do this, see references in Anil Seth's causality density paper
	but this will work for now.'''
	
	assert sigma > 0.0, "gaussian: sigma must be positive"
	
	if the_shape is None:
		return random.normal( 0, sigma )
	else:
		return random.normal( 0, sigma, the_shape )
###############################################################

if __name__ == '__main__':
		
#	input_filename = 'brainFunction_157.txt'
	input_filename = 'brainAnatomy_62_incept.txt'
	c = pw_critter( INPUT_FILENAME, INPUT_FILENAME2 )
	a, f = c.anat, c.func
	
	if a:
		start_nodes = [12]
		connected = a.trace( start_nodes, NUM_STEPS_TO_BACKTRACE )
		connected_back = a.trace_back( start_nodes, NUM_STEPS_TO_BACKTRACE )	

		print "nodes %(connected)s are connected within %(NUM_STEPS_TO_BACKTRACE)s steps from nodes %(start_nodes)s" % locals()
		print "nodes %(connected_back)s are BACKconnected within %(NUM_STEPS_TO_BACKTRACE)s steps from nodes %(start_nodes)s" % locals()

	if f:

		########################################################
		# Apply Gaussian noise?
		########################################################
		if APPLY_GAUSSIAN_NOISE_TO_ALL_NEURONS:
			print '- APPLYING GAUSSIAN NOISE WITH sigma=%s to all %s neurons' % ( GAUSSIAN_NOISE_SIGMA, f.num_neurons )
			f.acts += gaussian_noise( GAUSSIAN_NOISE_SIGMA, f.acts.shape )


		########################################################
		# Print handy statistics
		########################################################
		f.print_statistics()
		f.write_to_Rfile( input_filename + '.R', range(f.num_neurons) )
