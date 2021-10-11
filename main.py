from __future__ import unicode_literals

from hazm import *

normalizer = Normalizer()
tokens = word_tokenize(normalizer.normalize('اصلاح نویسه ها و استفاده از نیم فاصله پردازش را آسان می کند'))
for token in tokens:
    print(token)
print(word_tokenize('اصلاح نویسه ها و استفاده از نیم فاصله پردازش را آسان می کند'))
