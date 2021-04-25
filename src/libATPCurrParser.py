#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  libATPCurrParser.py
#  
#  Copyright 2016 Leonardo M. N. de Mattos <l@mattos.eng.br>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 3 of the License.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

def parseATPCurr(inputLis):
	
	import mmap
	
	# Data format
	dataSet = {
		'Node-K': 'Node-K',
		'Node-M': 'Node-M',
		'Ire': 0.0,
		'Iim': 0.0,
		'Imod': 0.0,
		'Iang': 0.0,
		'P': 0.0,
		'Q': 0.0
	}
	
	# Opening lis-file 
	try:
		fpLis = open(inputLis, 'r')
	except IOError:
		return(None)
	
	# Map file into memory
	mpLis = mmap.mmap(fpLis.fileno(), 0, access=mmap.ACCESS_READ)
	
	# Search in lis-file for the steady-state 
	switchCurKey = "Output for steady-state phasor switch currents."
	switchCurKeyEnd = "Solution at nodes with known voltage."
	try: 
		pos_switchCurKeyEnd = mpLis.find(switchCurKeyEnd) - 4
		pos_switchCurKey = mpLis.find(switchCurKey,0,pos_switchCurKeyEnd)
	except ValueError:
		print "Not valid lis-file"
		return(None)
	
	# Set pointer position
	p = pos_switchCurKey + len(switchCurKey) + 126 + 2
	
	# Actually parse the file
	dataList = []
	while(p < pos_switchCurKeyEnd):

		# New data dict
		data = dataSet.copy()
		
		# Check for open switch
		if mpLis.find("Open",p,p+131) == -1:
			
			# Treat lis-file switch line
			line = mpLis[p:p+131].strip().split()			
			
			# check for grounded switches, Node-K
			if mpLis[p+6:p+12] == '      ':
				data['Node-K'] = 'TERRA'
				line.insert(0,'TERRA')
			else:
				data['Node-K'] = line[0]
			
			# check for grounded switches. Node-M
			if mpLis[p+16:p+22] == '      ':
				data['Node-M'] = 'TERRA'
				line.insert(1,'TERRA')
			else:
				data['Node-M'] = line[1]

			# Read data and save
			data['Ire'] = float(line[2])
			data['Iim'] = float(line[3])
			data['Imod'] = float(line[4])
			data['Iang'] = float(line[5])
			data['P'] = float(line[6])
			data['Q'] = float(line[7])
			
			p += 131

		else:
			
			# Treat lis-file switch line
			line = mpLis[p:p+125].strip().split()			

			# Read data and save
			data['Node-K'] = line[0]
			data['Node-M'] = line[1]		
		
			p += 125
			
		dataList.append(data)
		
	# Close lis-file
	fpLis.close

	return(dataList)
	
# Segunda opção de leitura utilizando StringIO
def parseATPCurr2(inputLis):
	
	import mmap
	import StringIO
	
	# Data format
	dataSet = {
		'Node-K': 'Node-K',
		'Node-M': 'Node-M',
		'Ire': 0.0,
		'Iim': 0.0,
		'Imod': 0.0,
		'Iang': 0.0,
		'P': 0.0,
		'Q': 0.0
	}
	
	# Opening lis-file 
	try:
		fpLis = open(inputLis, 'r')
	except IOError:
		return(None)
	
	# Map file into memory
	mpLis = mmap.mmap(fpLis.fileno(), 0, access=mmap.ACCESS_READ)
	
	# Search in lis-file for the steady-state 
	switchCurKey = "Output for steady-state phasor switch currents."
	switchCurKeyEnd = "Solution at nodes with known voltage."
	try: 
		pos_switchCurKeyEnd = mpLis.find(switchCurKeyEnd) - 4
		pos_switchCurKey = mpLis.find(switchCurKey,0,pos_switchCurKeyEnd)
	except ValueError:
		print "Not valid lis-file"
		return(None)
	
	# Set pointer position
	buffer = StringIO.StringIO(mpLis[pos_switchCurKey+len(switchCurKey)+127+1:pos_switchCurKeyEnd])	
	dataList = []
	for line_raw in buffer.readlines():		

		# New data dict
		data = dataSet.copy()
		
		# Check for open switch
		if line_raw.find("Open") == -1:
			
			# Treat lis-file switch line
			line = line_raw.strip().split()			
			
			# check for grounded switches, Node-K
			if line_raw[6:12] == '      ':
				data['Node-K'] = 'TERRA'
				line.insert(0,'TERRA')
			else:
				data['Node-K'] = line[0]
			
			# check for grounded switches. Node-M
			if line_raw[16:22] == '      ':
				data['Node-M'] = 'TERRA'
				line.insert(1,'TERRA')
			else:
				data['Node-M'] = line[1]

			# Read data and save
			data['Ire'] = float(line[2])
			data['Iim'] = float(line[3])
			data['Imod'] = float(line[4])
			data['Iang'] = float(line[5])
			data['P'] = float(line[6])
			data['Q'] = float(line[7])			

		else:
			
			# Treat lis-file switch line
			line = line_raw.strip().split()			

			# Read data and save
			data['Node-K'] = line[0]
			data['Node-M'] = line[1]								
		
		dataList.append(data)
		
	# Close lis-file
	fpLis.close	

	return(dataList)
