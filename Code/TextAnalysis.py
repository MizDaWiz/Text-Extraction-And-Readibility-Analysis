# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 19:16:44 2024

@author: Fizza
# %%
"""
# %% Imports
import os 
import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize, SyllableTokenizer
# %%Complete Analysis

#Load Dictionaries
def load_words(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        return set(word.strip().lower() for word in f)

#Syllable Counter
def num_of_syll(tokens):
    ST = SyllableTokenizer()
    syllable_counts = [len(ST.tokenize(token)) for token in tokens]
    
    return syllable_counts

#Personal Pronouns
def pronouns(tokens):
    personal_pronouns = {
    'i', 'me', 'my', 'mine', 'myself',
    'you', 'your', 'yours', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself',
    'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself',
    'we', 'us', 'our', 'ours', 'ourselves',
    'they', 'them', 'their', 'theirs', 'themselves'
    }
    
    
    # Count personal pronouns, treating 'US' as not a pronoun
    pronoun_count = sum(
        1 for word in tokens if word.lower() in personal_pronouns and word!= 'us'
    )

    
    return pronoun_count 
    
#Calculate all outputs for a given article
def analyze_text(text, positive_words, negative_words):
    #Word Counts,CharCount and Sentiment Scores
    wtokens = word_tokenize(text.lower())
    
    ##Filter Punctuations from tokens
    wtokens = [token for token in wtokens if re.match(r'\w+', token)]
    
    ##Sentiment Scores and Word Count(4)
    p_score = sum(1 for word in wtokens if word in positive_words)
    n_score = sum(1 for word in wtokens if word in negative_words)
    pol_score = (p_score-n_score)/(p_score+n_score+0.000001)
    word_count = len(wtokens)
    char_count = len(text)
    s_score = (p_score+n_score)/(word_count+0.000001)
    
    #Sentence Count
    sen_count = len(sent_tokenize(text.lower()))
    
    #Readibility Analysis(2)
    avg_senlen = word_count/sen_count
    avg_wordlen = char_count/word_count
       
    
    #Num of Complex Words(3)
    syll_perword = num_of_syll(wtokens)
    c_word_count = sum(1 for num in syll_perword if num > 1)
    avg_syll_word = sum(syll_perword)/len(syll_perword)
    c_word_per = c_word_count/word_count
    fog_index = 0.4*(avg_senlen+c_word_per)
    
    #Pronouns
    pron_count = pronouns(wtokens)
    
    return p_score, n_score, pol_score, s_score, avg_senlen, c_word_per, fog_index, c_word_count, word_count, avg_syll_word, pron_count, avg_wordlen

#Iterate through all articles and store the result
def analyze_all_articles(articles_folder, master_dictionary_folder):
    
    #Get Positive and Negative Words
    positive_words = load_words(os.path.join(master_dictionary_folder, 'positive-words.txt'))
    negative_words = load_words(os.path.join(master_dictionary_folder, 'negative-words.txt'))
    
    results = [] 
    #Iterate
    for filename in os.listdir(articles_folder):
        
        if filename.endswith('.txt'):
            file_path = os.path.join(articles_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            positive_score, negative_score, polarity_score, subjectivity_score, avg_senlen, c_word_per, fog_index, c_word_count, word_count, avg_syll_word, pron_count, avg_wordlen, = analyze_text(text, positive_words, negative_words)
            results.append({
            'URL_ID': filename,
            'positive_score': positive_score,
            'negative_score': negative_score,
            'polarity_score': polarity_score,
            'subjectivity_score':subjectivity_score, 
            'avg_sentence_length':avg_senlen,
            'Percentage Of Complex Words':c_word_per,
            'Fog Index':fog_index,
            'Complex Word Count': c_word_count,
            'word_count': word_count,
            'Syllable Per Word': avg_syll_word,
            'Personal Pronouns': pron_count,
            'Average Word Length': avg_wordlen
            
        })
        print(f"Analyzed: {filename}")

    return results

def save_results_to_csv(results, output_path):
     df = pd.DataFrame(results)
     df.to_csv(output_path, index = False)


# %%Execute(Change Forlder Paths)

master_dictionary_folder = 'C:/Users/Fizza/Desktop/20211030 Test Assignment/MasterDictionary'
resultpath = 'C:/Users/Fizza/Desktop/20211030 Test Assignment/output_final.csv'
articles_folder = 'C:/Users/Fizza/Desktop/20211030 Test Assignment/articles'
results = analyze_all_articles(articles_folder, master_dictionary_folder)
save_results_to_csv(results, resultpath)
print("Text analysis complete. Results saved to output_final.csv")

#Understand why word length is coming larger, test at base level
#Find other things as specified 