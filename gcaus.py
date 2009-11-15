#!/usr/bin/python
from pprint import pprint
#from numpy import array, matrix, exp, pi, sqrt, mean, round, random
#from copy import copy
from pw_critter import pw_critter
import os
#import rpy2.robjects as robjects
from scipy import stats

#####################################################
INPUT_DIRECTORY = '/gcausality/sample_data'
NUM_STEPS_TO_BACKTRACE = 3
NUM_TIMESTEPS_TO_CHOOSE_REFERENCE_BEHAVIOR = 5

MIN_NUM_TIMESTEPS_TO_CALC_GC_OVER = 30

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
	

	filenames = [ INPUT_DIRECTORY + '/' + x for x in os.listdir(  INPUT_DIRECTORY ) if not x.startswith('.') ]
	
	#print filenames
	indices = sorted(list(set([ part for fname in filenames for part in fname.split('_') if part.isdigit() ])))
	
	# for each index...
	for index in indices:
		fnames = [ fname for fname in filenames if '_'+index in fname ]
		assert len(fnames) == 2, "matched more than two!"
	
		c = pw_critter( fnames[0], fnames[1] )
	
		print "- Evaluated critter #%s" % (index)
		a, f = c.anat, c.func
		
		########################################################
		# Apply Gaussian noise?
		#######################################################
		if APPLY_GAUSSIAN_NOISE_TO_ALL_NEURONS:
			print '- APPLYING GAUSSIAN NOISE WITH sigma=%s to all %s neurons' % ( GAUSSIAN_NOISE_SIGMA, f.num_neurons )
			f.acts += gaussian_noise( GAUSSIAN_NOISE_SIGMA, f.acts.shape )

		behav = f.neurons['behavior'][-1]
		print "behav=%s" % behav

		reference_time = c.reference_time( behav, NUM_TIMESTEPS_TO_CHOOSE_REFERENCE_BEHAVIOR, MIN_NUM_TIMESTEPS_TO_CALC_GC_OVER )
		if reference_time is None:
			print "- critter %s did not live long enough to determine causality (min=%s)" % (index, MIN_NUM_TIMESTEPS_TO_CALC_GC_OVER+NUM_TIMESTEPS_TO_CHOOSE_REFERENCE_BEHAVIOR)
			continue
		
		CN = c.context_network( behav, NUM_STEPS_TO_BACKTRACE )

		print "entire CN=%s" % CN
		print "reference_time=%s" % reference_time

		##########################################################################################
		# now to make the GRANGER NETWORK (GN) from the CONTEXT NETWORK (CN)
		# GRANGER NETWORK (GN) is an (improper) subset of the CN
		##########################################################################################
		
		# 1. Write the Rfilename
		Rfilename = "func_%s.R" % index
		f.write_to_Rfile( Rfilename, labels=range(f.num_neurons) )
		
		# 2. Open it in R
		print "pi=%s" % robjects.r['pi']
		
		# Foreach context pair, see if the ANOVA of a future time-series does significantly better using the past 
		# of the 1st node to predict the 2nd.
		
		raw_input('...')

		########################################################
		# Print handy statistics
		########################################################
#		f.print_statistics()
