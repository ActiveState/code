import ctypes

class C_struct:
	"""Decorator to convert the given class into a C struct."""

	# contains a dict of all known translatable types
	types = ctypes.__dict__

	@classmethod
	def register_type(cls, typename, obj):
		"""Adds the new class to the dict of understood types."""
		cls.types[typename] = obj

	def __call__(self, cls):
		"""Converts the given class into a C struct.
		
		Usage:
			>>> @C_struct()
			... class Account:
			... 	first_name = "c_char_p"
			...	last_name = "c_char_p"
			... 	balance = "c_float"
			...
			>>> a = Account()
			>>> a
			<cstruct.Account object at 0xb7c0ee84>

		A very important note: while it *is* possible to
		instantiate these classes as follows:

			>>> a = Account("Geremy", "Condra", 0.42)

		This is strongly discouraged, because there is at
		present no way to ensure what order the field names
		will be read in.
		"""
		
		# build the field mapping (names -> types)
		fields = []
		for k, v in vars(cls).items():
			# don't wrap private variables
			if not k.startswith("_"):
				# if its a pointer
				if v.startswith("*"):
					field_type = ctypes.POINTER(self.types[v[1:]])
				else:
					field_type = self.types[v]
				new_field = (k, field_type)
				fields.append(new_field)

		# make our bases tuple
		bases = (ctypes.Structure,) + tuple((base for base in cls.__bases__)) 
		# finish up our wrapping dict
		class_attrs = {"_fields_": fields, "__doc__": cls.__doc__}

		# now create our class
		return type(cls.__name__, bases, class_attrs)	
