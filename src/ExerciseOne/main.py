from hazm import *


def clean(text):
    normalizer = Normalizer()
    text = normalizer.affix_spacing(text)
    text = normalizer.character_refinement(text)
    text = normalizer.punctuation_spacing(text)
    return text


def sentences(text):
    tokenizer = SentenceTokenizer()
    return tokenizer.tokenize(text)


if __name__ == '__main__':
    sample = "بنابرایـن ایـن مسـئله فرصـت خوبـی بـرای اسـتفاده از ایـن فضـای پویـا جهـت رونق بخشــیدن بــه کســب " \
             "وکارتان اســت ، به ویــژه ازاین جهــت کــه ایــن شــبکه امــکان تبلیغــات را از طریــق پســتها و " \
             "اســتوریها بــرای مــردم بســیار راحتتــر نمــوده اســت. عــلاوه بــر ایــن افــراد جوانتــر همیشــه " \
             "علاقــه ی بیشــتری بــه شــبکه های اجتماعـی ماننـد اینسـتاگرام، یوتیـوب، توییتـر، فیـس بـوک و ایـن دسـت " \
             "برنامه هـا داشـته اند و ایـن گـروه سـنی همیشـه خریـد اینترنتـی را بـه خریـد حضـوری ترجیـح میدهنـد، " \
             "زیـرا عـاوه بـر راحتـی ایـن نـوع از خریـد ، وقتـی ایـن دسـته از کاربـران از طریــق فروشــگاه های " \
             "اینترنتــی معتبــر خریــد خــود را انجــام میدهنــد به نوعــی از اصالــت کالا ی خــود اطمینــان دارنــد " \
             "و میداننــد کــه کالا یــی کــه قــرار اســت بــه دستشـان برسـد از کیفیـت بالا یـی برخـوردار اسـت . "
    sample = clean(sample)
    sample = sentences(sample)
    tagger = POSTagger(model=r"")
    tokens_list = []
    tags_list = []
    for sen in sample:
        tokens_list.append(word_tokenize(sen))
        tags_list.extend(tagger.tag(sen))

    lemmatizer = Lemmatizer()
    lemmatized_words = []
    for tag in tags_list:
        lemmatized_words.append(lemmatizer.lemmatize(tag[0], pos=tag[1]))

