#!/usr/bin/python
import os.path
import pw_anatomy, pw_brainfunction

class pw_critter:
	'''contains methods and data of polyworld critter anatomy and brainFunction files'''
	
	
	def __init__(self, filename1, filename2=None ):
		''' you may pass in filename1 and filename2 in any order'''

		self.func_filename, self.func = None, None
		self.anat_filename, self.anat = None, None

		assert os.path.isfile( filename1 ), "filename1 wasn't a file"
		assert filename2 is None or os.path.isfile( filename2), "filename2 was specified but wasn't a valid file"
		
		
		f1 = open(filename1)
		header1 = f1.readline()
		if header1.startswith('brainFunction'):
			self.func_filename = filename1
		elif header1.startswith('brain'):
			self.anat_filename = filename1
		else:
			raise ValueError, "filename1 was not a polyworld file"
		
		f1.close()
		
		if filename2 is not None:
			f2 = open(filename2)
			header2 = f2.readline()
			if header2.startswith('brainFunction'):
				assert self.func_filename is None, "func_filename already defined!"
				self.func_filename = filename2
			elif header2.startswith('brain'):
				assert self.anat_filename is None, "anat_filename already defined!"				
				self.anat_filename = filename2
			else:
				raise ValueError, "filename2 was not a polyworld file"

			f2.close()
		
		if self.anat_filename is not None:
#			print "anatfile=", anat_filename
			self.anat = pw_anatomy.pw_anatomy( self.anat_filename )
		
		if self.func_filename is not None:
#			print "funcfile=", func_filename
			self.func = pw_brainfunction.pw_brainfunction( self.func_filename )
			
		# sanity chceks to ensure the anatomy and function are about the same critter
		if self.anat and self.func:
			assert self.anat.critter_index == self.func.critter_index, "critter indices didn't match"
			assert self.anat.num_neurons == self.func.num_neurons, "number of neurons didn't match"
			
		
			

if __name__ == '__main__':
	c = pw_critter('brainAnatomy_62_incept.txt', 'brainFunction_84.txt' )
	
	