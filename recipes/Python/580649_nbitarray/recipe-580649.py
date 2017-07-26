class nBitArray() :
	
	m = 32
	f = 'I'
	
	_default_type = None
	
	def __init__(self, n_bit) :
		
		if not (isinstance(n_bit, int) and n_bit > 0) :
			raise ValueError
		
		self.n_bit = n_bit
		self.n_item = 0
		
		self.b_mask = (2 ** self.n_bit) - 1
		self.i_mask = ((0x1 << self.m) - 1)
		
	def _normalize_index(self, index) :
		if (-1 * self.n_item) <= index < 0 :
				index += self.n_item
		if 0 <= index < self.n_item :
			return index
		raise IndexError
			
	def __getitem__(self, index):
		if isinstance(index, int) :
			return self._get_at(self._normalize_index(index))
		elif isinstance(index, slice) :
			return (self._get_at(i) for i in range(* index.indices(self.n_item)))
		else:
			raise TypeError("index must be int or slice")
			
	def __str__(self) :
		u = io.StringIO()
		for n, i in enumerate(self._data) :
			u.write("{0:08X}".format(i))
			u.write('\n' if (n + 1) % 6 == 0 else ' ')
		return u.getvalue()
	
	def load_data(self, value_lst) :
		""" load a list of n_bit words """
		w_curs = 0 # position in the word
		word = 0
		stack = list()
		for n, value in enumerate(value_lst) :
			value = value & self.b_mask			
			v_curs = 0 # position in the value
			v_count = self.n_bit - v_curs # number of remaining bits to be written
			w_count = self.m - w_curs # number of bits available in the word			
			while v_count > 0 :
				if w_count <= v_count :
					p = value >> (v_count - w_count)
					word |= p & self.i_mask
					v_curs += w_count
					w_curs += w_count
				else :
					p = value << (w_count - v_count) 
					word |= p & self.i_mask
					v_curs += v_count
					w_curs += v_count
				if w_curs == self.m :
					stack.append(word)
					word = 0
					w_curs = 0 
				v_count = self.n_bit - v_curs
				w_count = self.m - w_curs
		if word :
			stack.append(word)			
		self.n_item = len(value_lst)
		self._data = array.array(self.f, stack)
		return self
		
	def _get_at(self, v_index) :
		if not 0 <= v_index < self.n_item :
			raise IndexError
			
		b = v_index * self.n_bit
		i_index = b // self.m # index of the word
		
		#print(v_index, b, i_index)
		
		v_curs = 0 # position in the value
		w_curs = b % self.m # position in the word
		
		v_count = self.n_bit - v_curs # number of remaining bits to append to the value
		w_count = self.m - w_curs # number of remaining bits to be read from the word
		
		value = 0
		while v_count > 0 :
			#print("v curs={0}, count={1}  -  w curs={2}, count={3}".format(v_curs, v_count, w_curs, w_count)) 
			if w_count <= v_count :
				value = (value << self.m) | self._data[i_index]
				#print("IF -> value = {0:05X}".format(value & self.b_mask))
				v_curs += w_count
				w_curs += w_count
			else :
				value = (value << v_count) | (self._data[i_index] >> (w_count - v_count))
				#print("ELSE -> value = {0:05X}".format(value & self.b_mask))
				v_curs += v_count
				w_curs += v_count
				
			if w_curs == self.m :
				i_index += 1
				w_curs = 0
				
			v_count = self.n_bit - v_curs
			w_count = self.m - w_curs
		
		return value & self.b_mask
			
if __name__ == '__main__' :

	high_res_sinus = [int(math.sin(i) * 0x3FFFFF) & 0x3FFFFF for i in range(10000)]
	low_res_sinus = [int(math.sin(i) * 0x3) & 0x3FFFFF for i in range(10000)]

	def do(array, name, size) :
		data = nBitArray(size).load_data(array)._data.tobytes()
		compressed = gzip.compress(data)
		print("{3}:{4} bits: {0} -> {1} ({2:0.1f} %)".format(
			len(data), len(compressed), 100 * len(compressed) / len(data), name, size)
		)

	do(high_res_sinus, "high_res_sinus", 22)
	do(high_res_sinus, "high_res_sinus", 24)
	do(low_res_sinus, "low_res_sinus", 22)
	do(low_res_sinus, "low_res_sinus", 24)
