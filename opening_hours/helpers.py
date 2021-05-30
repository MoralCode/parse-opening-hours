
def normalize_string(string):
	string = unicodedata.normalize('NFC', string)
	string = string.strip()
	return string