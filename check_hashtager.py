import re
words = []
# corncob_lowercase.txt contains a list of dictionary words
with open('corncob_lowercase.txt', 'rb') as f:
    for read_word in f:
        words.append(read_word.strip())
def func_replace(each_func):
    i = 0
    wordsineach_func = []
    while len(each_func) > 0:
        i = i + 1
        word_found = longest_word(each_func)
        if len(word_found) > 0:
            wordsineach_func.append(word_found)
            each_func = each_func.replace(word_found, "")
    return ' '.join(wordsineach_func)


def longest_word(phrase):
    phrase_length = len(phrase)
    words_found = []
    index = 0
    outerstring = ""
    while index < phrase_length:
        outerstring = outerstring + phrase[index]
        index = index + 1
        if outerstring in words or outerstring.lower() in words:
            words_found.append(outerstring)
    if len(words_found) == 0:
        words_found.append(phrase)
    return max(words_found, key=len)

def check_hashtager(s):
	hashtags = re.findall(r"#(\w+)", s)
	return re.sub(r"#(\w+)", lambda m: func_replace(m.group(1)), s)

if __name__ == '__main__':
	print check_hashtager("#Whatthehello #goback")
