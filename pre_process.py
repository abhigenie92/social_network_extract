# -*- coding: utf-8 -*-
from nltk.tokenize import TreebankWordTokenizer
import re,string
def tokenize_words(text):
	tokens = TreebankWordTokenizer().tokenize(text)
	contractions = ["n't", "'ll", "'m"]
	fix = []
	for i in range(len(tokens)):
		for c in contractions:
			if tokens[i] == c: fix.append(i)
	fix_offset = 0
	for fix_id in fix:
		idx = fix_id - 1 - fix_offset
		tokens[idx] = tokens[idx] + tokens[idx+1]
		del tokens[idx+1]
		fix_offset += 1
	return tokens
def process_text(text):
	# remove URLs, RTs, and twitter handles
	text=" ".join(text).lower()
	text_nourls=re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', text)
	text_nohandles=re.sub(r'@[A-Z,a-z,0-9,_]*[\s,\p]?','',text_nourls)
	text_noRTs=text_nohandles.replace('RT','')
	
	replace_list=['narcotics','anonymous','alcoholics']
	text_final=re.sub(r'|'.join(map(re.escape, replace_list)), '', text_noRTs)
	
	tokens=tokenize_words(text_final)
	remove_tokens=['na','aa','rt']

	tokens = [c for c in tokens if (c not in remove_tokens) and (len(c)> 1)]
	tokens2=[]
	for t in tokens:
		flag=False
		for x in t:
			if x not in string.punctuation:
				flag=True
		if flag:
			tokens2.append(t)

	return tokens2
