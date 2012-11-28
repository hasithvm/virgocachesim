from collections import deque

class AssociativeCacheModel():
	"""
	A CacheModel simulates a cache in memory and the various accesses it has to perform. In the future, this will be a base class, with various cache models as subclasses thereof.
	"""
	def __init__(self, cache_size,blockmap, **kwargs):
		self.cache_size = cache_size
		self.blockmap = blockmap
		self.sim_queue = deque(self.cache_size*[0], self.cache_size)
		self.cache_latency = kwargs.get('access_delay',0.5)
		self.memory_latency = kwargs.get('memory_latency',100)
		self.timer = 0.0
	
	def request(self,addr):
		"""
		Simulates a cache request at [addr]
		"""
		blockaddr = self.blockmap.get(addr)
		cache_hit = blockaddr in self.sim_queue
		if (not cache_hit):
			self.timer = self.timer + self.memory_latency
			self.sim_queue.appendleft(blockaddr)
		else:
			self.timer = self.timer + self.cache_latency
		return cache_hit

	def getTotalLatency(self):
		return self.timer

class BlockMap(dict):
	"""
	A BlockMap is an extended dict with the ability to check a range of values, as opposed to a single key. Any Iterable is a valid key range, but in this case, it's a hex integer.
	"""
	def __init__(self,d={}):
		for key,value in d.items():
			if len(key) !=2:
				raise Exception("Error! Key must have start and end ranges!")
			self[self.keyconvert(key)] = value

	def keyconvert(self,key):
		k = []
		for key_val in key:
			if type(key_val) == 'str':
				k.append(int(key_val,16))
			else:
				k.append(key_val)
		return k

	def __getitem__(self,key_search):

		for key, val in self.items():
			if key[0] <= key_search <=key[1]:
				return val
		raise KeyError("Key %s not in blockmap!" % key_search)

	def get(self, key, default=None):
		try:
			return self.__getitem__(key)
		except KeyError:
			return default

	def __setitem__(self, key_add, value_add):
		proper_key = self.keyconvert(key_add)
		try:
			if len(proper_key) == 2:
				if proper_key[0] < proper_key[1]:
					dict.__setitem__(self, (proper_key[0],proper_key[1]), value_add)
				else:
					raise RuntimeError('Start address must be less than the ending address!')
			else:
				raise ValueError('Start and end addresses must be a tuple (start, end)')
		except TypeError:
			raise TypeError('Invalid datatype for keys!')

	def __contains__(self, key):
		key = keyconvert(key)
		try:
			return bool(self[key]) or True
		except KeyError:
			return False
