# -*- coding: utf-8 -*-
import re
thestring = 'this is some text that will have one form or the other url embeded, most will have valid URLs while there are cases where they can be bad. for eg, http://www.google.com and http://www.google.co.uk and www.domain.co.uk and etc.'

URLless_string = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', thestring)

print URLless_string
