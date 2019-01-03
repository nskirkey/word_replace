import string, re, os
from sys import argv, exit
from wordnik import swagger, WordApi
from queue import Queue

# Credentials to create client from wordnik API.
wordnikUrl = 'http://api.wordnik.com/v4'
wordnikKey = 'your-api-key'

# Credentials for dictionaryapi.com. (Not used, but maybe can be expanded with).
dictionaryUrl = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/voluminous?key=your-api-key'
dictionaryKey = 'your-api-key'

# Fuction to replace word with American Heritage Dictionary format pronunciation.
def ahdReplace(w):
	pronunciation_temp = my_dict.getTextPronunciations(w, limit=1)

	# Don't replace if NoneType.
	if pronunciation_temp == None:
		pronunciation = w
		pronunciationType = 'none'

	else:
		pronunciation = pronunciation_temp[0].raw
		pronunciationType = pronunciation_temp[0].rawType

	return pronunciation, pronunciationType

# Fuction to replace word with IPA format pronunciation.
def ipaReplace(w):
	if cleaned_word in ipa:
		pronunciation = ipa[cleaned_word]
		pronunciationType = "ipa"

	else:
		pronunciation = w
		pronunciationType = 'none'

	return pronunciation, pronunciationType

# Funcation to remove punctuation from string.
def removePunctuation(s):
	# Remove apostrophies from set of punctuation to be removed (affects the look-up of contractions).
	sp = string.punctuation.replace('\'', '')

	return s.translate(str.maketrans('', '', sp))

# Create client and WordApi objects.
client = swagger.ApiClient(wordnikKey, wordnikUrl)
my_dict = WordApi.WordApi(client)

# Input and output filenames.
text_filename = './input.txt'
output_filename = './output.txt'
look_up_filename = './CMU.in.IPA.txt'

# Open files for reading and writing.
text = open(text_filename, 'r')
output_text = open(output_filename, 'wb')
look_up_text = open(look_up_filename, 'r')

# Pronunciation formats supported 
acceptable_formats = ['ahd', 'ipa']

# Check command line arguments. If incorrect exit proram.
if len(argv) !=  2 or argv[1] not in acceptable_formats:
	print('Incorrect arguments.')
	exit(0)

# Load dict with IPA prononciations if format selection is IPA.
if argv[1] == 'ipa':
	ipa = {}	
	for line in look_up_text:
		entry = line.split()
		entry[0] = entry[0].translate(str.maketrans('', '', ','))
		if len(entry) < 2:
			ipa[entry[0]] = entry[0]
		else:
			ipa[entry[0]] = entry[1]

# Compile regular expression to detect punctuation.
punc_pat = re.compile('!|"|#|\$|%|&|\(|\)|\+|,|-|\*|\.|\'|\/|:|;|<|=|>|\?|@|\[|\\|\]|\^|_|`|{|\||}|~')

# Create queues to hold punctuation.
q =  Queue(100)

# Work.
for line in text:
	for word in line.split():
		# Handle punctuation in sentences using regex.
		# Enqueue punctuation to be put in correct place in output.
		for letter in word:
			if punc_pat.match(letter):
				q.put(letter)
			
		# Clean word from input.
		cleaned_word = removePunctuation(word).lower()
		
		# Traslate using IPA dict loaded (much faster).
		if argv[1] == 'ipa':
			pronunciation, pronunciationType = ipaReplace(cleaned_word)

		# Otherwise get AHD pronunciation of word from Wordnik.
		else:
			pronunciation, pronunciationType = ahdReplace(cleaned_word)

		# Need to find way to handle pronunciations in arpabet format.
		# Replace with english word until handled.
		if pronunciationType == 'arpabet':
			output_text.write(word.encode('utf-8') + ' '.encode('utf-8'))
			continue

		# Get rid of unneseccary information from API return.
		if ',' in pronunciation:
			pronunciation = pronunciation[0:pronunciation.find(',')] 

		if ';' in pronunciation:
			pronunciation = pronunciation[0:pronunciation.find(';')] 

		if '<' in pronunciation:
			pronunciation = pronunciation[0:pronunciation.find('<')] 

		# Remove bad chars from function return.
		bad_chars = '()'
		pronunciation = pronunciation.translate(str.maketrans('', '', bad_chars))

		# Write word to output file.
		output_text.write(pronunciation.encode('utf-8') + ' '.encode('utf-8'))
		
		# Write punctuation to output file.
		while q.qsize() > 0:
			# Get rid of spaces after word before period that would cause problem (maybe can be improved to not add space at end of sentences?). 
			output_text.seek(-1, os.SEEK_END)
			output_text.truncate()

			#  Write punctuation.
			output_text.write(q.get()[0].encode('utf-8') + ' '.encode('utf-8'))

# Close input/output files.
text.close()
output_text.close()