#!/usr/bin/python
from pw_critter import pw_critter
import os

DIR = '/gcausality/sample_data'

filenames = [ DIR + '/' + x for x in os.listdir( DIR ) if not x.startswith('.') ]

#print filenames
indices = sorted(list(set([ part for fname in filenames for part in fname.split('_') if part.isdigit() ])))

# for each index...
for index in indices:
    fnames = [ fname for fname in filenames if '_'+index in fname ]
    
    assert len(fnames) == 2, "matched more than two!)"

    c = pw_critter( fnames[0], fnames[1] )

    print "fnames=%s  -- successfully evaluated critter #%s" % (fnames, index)
    
#    c = pw_critter( fnames[0] )
    
    dist = 1
    test_neuron = c.func.neurons['behavior'][-1]
#    print "bias_node=%s" % c.func.neurons['bias']
#    print "num_neurons=%s" % c.anat.num_neurons
    
#    c.func.print_statistics()

#    print c.anat.cxnmatrix[:,bias_node].T
    
#    print "trace(bias,1)=", c.anat.trace( bias_node, 1 )
    backconnected = c.anat.trace_back( test_neuron, dist )
    assert c.func.neurons['bias'] in backconnected or test_neuron in c.func.neurons['input'], "Had error!  Bias node didn't connect to test_node"

    print "trace_back(behav,1)=", backconnected
#    raw_input('...')


print "#samples=%s" %  len(indices)
#indices = [ x[:-4].split('_')[-1] for x in filenames if x.endswith('.txt') ]

#print indices

