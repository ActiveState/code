def Plural(num=1, text=''):
	if num == 1:
		# singular -- easy
		result = '%d %s' % (num, text)
	else:
		aberrant = {	'knife' 	: 'knives',
				'self'		: 'selves',
				'elf'		: 'elves',
				'life'		: 'lives',
				'hoof'		: 'hooves',
				'leaf'		: 'leaves',
				'echo'		: 'echoes',
				'embargo'	: 'embargoes',
				'hero'		: 'heroes',
				'potato'	: 'potatoes',
				'tomato'	: 'tomatoes',
				'torpedo'	: 'torpedoes',
				'veto'		: 'vetoes',
				'child'		: 'children',
				'woman'		: 'women',
				'man'		: 'men',
				'person'	: 'people',
				'goose'		: 'geese',
				'mouse'		: 'mice',
				'barracks'	: 'barracks',
				'deer'		: 'deer',
				'nucleus'	: 'nuclei',
				'syllabus'	: 'syllabi',
				'focus'		: 'foci',
				'fungus'	: 'fungi',
				'cactus'	: 'cacti',
				'phenomenon'	: 'phenomena',
				'index'		: 'indices',
				'appendix'	: 'appendices',
				'criterion'	: 'criteria'
				}

		if aberrant.has_key(text):
			result = '%d %s' % (num, aberrant[text])
		else:
			postfix = 's'
			if len(text) > 2:
				vowels = 'aeiou'
				if text[-2:] in ('ch', 'sh'):
					postfix = 'es'
				elif text[-1:] == 'y':
					if (text[-2:-1] in vowels) or (text[0] in string.uppercase):
						postfix = 's'
					else:
						postfix = 'ies'
						text = text[:-1]
				elif text[-2:] == 'is':
					postfix = 'es'
					text = text[:-2]
				elif text[-1:] in ('s', 'z', 'x'):
					postfix = 'es'
				
			result = '%d %s%s' % (num, text, postfix)
