import cachemodel, sys
from cachemodel import BlockMap, AssociativeCacheModel
def main(args):
	"""
	Simulates a read cache in memory. To execute, give it memory addresses to fetch in hex, simulation assumes a fully associative cache. Generates CSV output of cache slot count [1-128] vs hit ratio. 
	"""
	lines = []
#read from stdin until EOF.
	while (True):
		try:
			readln = raw_input()
			lines.append(readln)
		
		except EOFError:
			break
	#create a blockmap dictionary
	blockmap = BlockMap(d = {(0x0010,0x0013):'B4', (0x0014,0x0017):'B5', (0x0020,0x0023):'B6', (0x0024,0x0027):'B9', (0x0028,0x002B): 'B10', (0x002C,0x002F): 'B11', (0x0030,0x0033): 'B12', (0x34,0x37):'B13', (0x38,0x3B): 'B14', (0x3C,0x3F): 'B15', (0x40,0x43): 'B16', (0xFFFC, 0xFFFF): 'B(16K-1)'})
	
	#generate the data we want to plot. Generate a CSV file.
	for i in [1,2,4,8,16,32,64,128]:
		simmodel = AssociativeCacheModel(i,blockmap, access_delay=0.5, memory_latency=100)
		hitcount = 0
		for line in lines:
			hitcount +=(1 if simmodel.request(int(line.strip(),16)) else 0)
		print i, ",", (float(hitcount) / len(lines)) * 100, simmodel.getTotalLatency()







if __name__=="__main__":
	sys.exit(main(sys.argv))

