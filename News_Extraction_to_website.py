#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Imports
from newspaper import Article
from newspaper import fulltext
import os
from yake import KeywordExtractor
import re
from newsfetch.news import newspaper
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from langdetect import detect
import urllib.request
from deep_translator import GoogleTranslator
import nltk
import eel
from tkinter import *
from tkinter import filedialog


# In[2]:


eel.init('web')


# In[3]:


@eel.expose
def btn_ResimyoluClick():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    filepath = filedialog.askopenfilename() #TODO: Add file type restrcition
    return filepath


# In[4]:


@eel.expose
def btn_SavePathClick():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder = filedialog.askdirectory() #TODO: Add file type restrcition
    return folder


# In[5]:


def Uploading_picture_attachment(url, title, content, excerpt, keywords, p1,p2,p3, Wordpress_url, Wordpress_username, Wordpress_password):
    #prepare metadata
    data1 = {
        'name': p1,
        'type': 'image/jpeg',  # mimetype
}
    
    if p2:
        data2 = {
            'name': p2,
            'type': 'image/jpeg',  # mimetype
    }
    else:
        data2 = None
    
    if p3:
        data3 = {
            'name': p3,
            'type': 'image/jpeg',  # mimetype
    }
    else:
        data3 = None
    
    # read the binary file and let the XMLRPC library encode it into base64
    with open(p1, 'rb') as img:
        data1['bits'] = xmlrpc_client.Binary(img.read())
        
    if data2:
        with open(p2, 'rb') as img:
            data2['bits'] = xmlrpc_client.Binary(img.read())
            
    if data3:
        with open(p3, 'rb') as img:
            data3['bits'] = xmlrpc_client.Binary(img.read())
        
    isOS = False;
        
    Posting_post(url, title, content, excerpt, keywords, data1,data2,data3, isOS, Wordpress_url, Wordpress_username, Wordpress_password)


# In[6]:


def Upload_picture_url(url, title, content, excerpt, keywords, p1,p2,p3, Wordpress_url, Wordpress_username, Wordpress_password):
    #Downloading given media
    
    try:
        filename1 = p1.split("/")[-1]
        urllib.request.urlretrieve(p1, filename1)
    except:
        raise ValueError("First image address is wrong")
    
    if p2:
        try:
            filename2 = p2.split("/")[-1]
            urllib.request.urlretrieve(p2, filename2)
        except:
            raise ValueError("Second image address is wrong")
    if p3:
        try:
            filename3 = p3.split("/")[-1]
            urllib.request.urlretrieve(p3, filename3)
        except:
            raise ValueError("Third image address is wrong")
    
    
    #prepare metadata
    data1 = {
        'name': filename1,
        'type': 'image/jpeg',  # mimetype
}
    if p2:
        data2 = {
            'name': filename2,
            'type': 'image/jpeg',  # mimetype
    }
    else:
        data2 = None
    
    if p3:
        data3 = {
            'name': filename3,
            'type': 'image/jpeg',  # mimetype
    }
    else:
        data3 = None
    
    # read the binary file and let the XMLRPC library encode it into base64
    with open(filename1, 'rb') as img:
        data1['bits'] = xmlrpc_client.Binary(img.read())
    
    if data2:
        with open(filename2, 'rb') as img:
            data2['bits'] = xmlrpc_client.Binary(img.read())
    if data3:
        with open(filename3, 'rb') as img:
            data3['bits'] = xmlrpc_client.Binary(img.read())
        
    isOS = True;
        
    Posting_post(url, title, content, excerpt, keywords, data1,data2,data3, isOS, Wordpress_url, Wordpress_username, Wordpress_password)


# In[7]:


#Extracting content, title, excerpt and keywords from given url
@eel.expose
def Extract_News(url, lang, picture_id, p1,p2,p3, Wordpress_url, Wordpress_username, Wordpress_password):
    print("running export")
    print(url)
    #using news-fetch
    news = newspaper(url)
    
    #using newspaper extraction
    # download and parse article
    article_n = Article(url)
    article_n.download()
    article_n.parse()
    sum = article_n.summary
    
    len_g = len(news.article)
    len_n = len(article_n.text)
    
    if not news.article:
        print("news-fetch not working, checking newspaper")
        if not article_n:
            print("newspaper not working, URL cant be extracted")
            time.sleep(5)
            return
    
    if len_g > len_n:
        article_content = news.article
        article_title = news.headline
        article_excerpt = news.summary
        print("Using news-fetch extraction")
    else:
        article_content = article_n.text
        article_title = article_n.title
        article_excerpt = sum
        print("Using newspaper extraction")
        
    
    article_content_string = str(''.join(article_content))
    
    article_title_string = ''.join(article_title)
    
    article_excerpt_string = ''.join(article_excerpt)
    
    #Translating extracted texts
    Translating_post(url, article_content_string, article_title, article_excerpt_string, p1,p2,p3, lang, picture_id, Wordpress_url, Wordpress_username, Wordpress_password)
    
    return True;


# In[8]:


#Keywords Extraction
def Keywords(text):
    
    #detect language of given text from url to extract keywords from
    lang = detect(text)
    
    text = re.sub('"', '', text)
    
    kw_extractor = KeywordExtractor(lan=lang, n=2, top=20)
    keywords = kw_extractor.extract_keywords(text)
    keywords = [x for x, y in keywords]
    elements = ['https', 'content', 'uploads', 'wp-content', 'jpg', 'figure', 'class', 'url', 'image','img', 'linkdestination','size-large','src','alt','href','alignnone','width','heading','strong']
    for i in elements:
        if i in keywords:
            keywords.remove(i)
            
    more_keywords = ['latest news' , 'magazine' , 'familymag' , 'news' , 'online' , 'no ads' , 'Europe' , 'read magazine online' , 'Magazin about everything' , 'magazine of the world']
    m_k = " ".join(more_keywords)
    m_k2 = GoogleTranslator(source='auto', target=lang).translate(m_k)
    
    more_keywords = m_k2.split()
    keywords.extend(more_keywords)
    return keywords


# In[9]:


@eel.expose
def Translating_post(url, content, title, excerpt, p1,p2,p3, lang, picture_id, Wordpress_url, Wordpress_username, Wordpress_password):
    
    print("running translate")
    keywords = Keywords(content)
    
    keywordsstring = " ".join(keywords)
    
    print("translating to " + lang) 
    
    #returns a corpus with batches of max_character=5000
    batch_corpus = prepare_batch_corpus(content)

    #returns complete translated corpus (one stirng of the whole translate content)
    content_translate = translate_batch_deepl(batch_corpus, lang)
    
    title_translate = GoogleTranslator(source='auto', target=lang).translate(title)
    
    lenght = len(excerpt)
    if lenght > 0:
        excerpt_translate = GoogleTranslator(source='auto', target=lang).translate(excerpt)
    else:
        excerpt_translate = GoogleTranslator(source='auto', target=lang).translate(title)
        
    keywordsstring_translate = GoogleTranslator(source='auto', target=lang).translate(keywordsstring)
    
    splitted_keywords = keywordsstring_translate.split()
    
    if picture_id == 1:
        Uploading_picture_attachment(url, title_translate, content_translate, excerpt_translate, splitted_keywords, p1,p2,p3, Wordpress_url, Wordpress_username, Wordpress_password)
    elif picture_id == 2:
        Upload_picture_url(url, title_translate, content_translate, excerpt_translate, splitted_keywords, p1,p2,p3, Wordpress_url, Wordpress_username, Wordpress_password)
    elif picture_id == 0:
        Posting_post(url, title_translate, content_translate, excerpt_translate, splitted_keywords, None,None, None, False, Wordpress_url, Wordpress_username, Wordpress_password)
        
    return True; 


# In[10]:


def prepare_batch_corpus(input_text, max_caracter=4500):
    # "input_text" is a list with one entry which is a long string of the text to be translated
    corpus = nltk.sent_tokenize(input_text)
    
    # Size information
    nb_sentence = len(corpus)

    # Batch information (reset these values after each batch finalization)
    batch = []
    batch_length = 0
    

    # All batches are stored in that list, which will bbe the output of the function
    batch_corpus = []
    
    # Going throug each sentence of the initial corpus to create the batches
    for idx, sentence in enumerate(corpus):
        
        # Are we dealing with the last sentence ?
        last_sentence = idx + 1 == nb_sentence

        # Checking the batch size before adding a new sentence in it
        hypothetical_length = batch_length + len(sentence)
        if hypothetical_length < max_caracter:
            batch.append(sentence)
            batch_length += len(sentence) # + len(joiner)
            
            # If sentence can be added to the corpus wa add it and don't save the corpus yet
            # Except if this is the last sentence
            if not last_sentence:
                continue
        
        # Finalizing batch beforee storing
        joined_batch = "".join(batch)
    
        # Save batch in the corpus
        batch_corpus.append(joined_batch)
        
        # Reseting batch parameters
        batch = []
        batch_length = 0
                    
    return batch_corpus


# In[11]:


def translate_batch_deepl(batch_corpus, lang):

    translated_text = []
    i= 0

    for text_to_translate in batch_corpus:
        #print(batch_corpus[i])
        text = GoogleTranslator(source='auto', target=lang).translate(text_to_translate)
        translated_text.append(text)
        i += 1
        

    content = "".join(translated_text)

    # return content
    return content


# In[12]:


@eel.expose
def Posting_post(url, title, content, excerpt, keywords, data1,data2,data3, isOs, Wordpress_url, Wordpress_username, Wordpress_password):
    
    #detect where you want to post this article
    client = Client(Wordpress_url, Wordpress_username, Wordpress_password)
    
    print("posting to " + Wordpress_url)
    
    
    #uploading pictures into the library   
    if data1:
        response1 = client.call(media.UploadFile(data1))
        attachment_id1 = response1['id']
        content = content + " "
    if data2:
        response2 = client.call(media.UploadFile(data2))
        attachment_url2 = response2['url']
        content = content + " " + attachment_url2 + " "
    if data3:
        response3 = client.call(media.UploadFile(data3))
        attachment_url3 = response3['url']
        content = content + " " + attachment_url3

    content = content + "Source: " + url
    
    
    #posting the post
    post = WordPressPost()
    post.title = title
    post.content = content
    post.excerpt = excerpt
    #first picture is thumbnail
    if data1:
        post.thumbnail = attachment_id1
    post.terms_names = {
    'post_tag': keywords,
    'category':['Uncategorized']
    }
    client.call(posts.NewPost(post))
    
    if isOs == True:
        #delete photos
        os.remove(data1['name'])
        try:
            os.remove(data2['name'])
        except:
            print("duplicated picture")
        try:
            os.remove(data3['name'])
        except:
            print("duplicated picture")
    
    
    print("posted!")
    return True


# In[13]:


@eel.expose
def dummy(param):
    head, tail = os.path.split(param)
    song_name = tail
    # song_name = os.path.splitext(tail)[0]
    return song_name


# In[14]:


eel.start('index.html', size = (1000, 600), port = 8080)

