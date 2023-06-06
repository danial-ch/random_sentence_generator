import re
import random
from decimal import Decimal

corpus = "The children were to be driven, as a special treat, to the sands at Jagborough. Nicholas was not to be of the party; he was in disgrace. Only that morning he had refused to eat his wholesome bread-and-milk on the seemingly frivolous ground that there was a frog in it. Older and wiser and better people had told him that there could not possibly be a frog in his bread-and-milk and that he was not to talk nonsense; he continued, nevertheless, to talk what seemed the veriest nonsense, and described with much detail the colouration and markings of the alleged frog. The dramatic part of the incident was that there really was a frog in Nicholas' basin of bread-and-milk; he had put it there himself, so he felt entitled to know something about it. The sin of taking a frog from the garden and putting it into a bowl of wholesome bread-and-milk was enlarged on at great length, but the fact that stood out clearest in the whole affair, as it presented itself to the mind of Nicholas, was that the older, wiser, and better people had been proved to be profoundly in error in matters about which they had expressed the utmost assurance."

def pre_process(text):
    """ INPUT : text to be processed
    OUTPUT processed text
    """

    # changing all characters to lower case
    lowered = text.lower()

    # adding starting and ending tags to all the sentences
    tagged = re.sub('\.', " </s> <s>", lowered)
    tagged = "<s> " + tagged[:-4]

    # removing punctuations from the sentences
    punctuations = [',', '!', '.', ';']
    removed_pun = tagged.translate({ord(x): '' for x in punctuations})

    return removed_pun

def ngrams(text, n):
    """ INPUT : text and number of n-grams
    OUTPUT N-Grams
    """
    output = []
    
    # splitting the text on space and trimming extra whitespaces
    splitted = [x.strip() for x in text.split(" ")]

    #creating ngrams based on the input
    for i in range(len(splitted)-n+1):
        output.append(' '.join(splitted[i:i+n]))

    return output

def random_sentence(tokens, size):
    """ INPUT : tokens is a list of word to be used as tokens
                size is size of the desired output
    OUTPUT a random sentence
    """

    # the sample function chooses n different samples from the set of unique words
    sentence_list = random.sample(tokens, size)

    # creating the sentence from the list and adding starting and finishing tags
    return "<s> " + " ".join(sentence_list) + " </s>"

# processing the text and creating unigrams and bigrams
processed_text = pre_process(corpus)
unigrams = ngrams(processed_text,1)
bigrams = ngrams(processed_text,2)

# adding all the unigrams to a set to have list of unique words and then counting the length of the set
tokens = set(unigrams) - {"<s>", "</s>"}
token_count = len(tokens)

# creating random sentence and it's corresponding bigrams and unigrams
sentence = random_sentence(tokens, random.randint(2,5))
sentence_unigrams = (ngrams(sentence,1))
sentence_bigrams = (ngrams(sentence,2))

total_chance = 1

# looping in the bigrams of the sentence
for i in range(len(sentence_bigrams)):

    # counting occurrences of the second word in each bigram in the corpus's unigrams
    u_count = unigrams.count(sentence_unigrams[i])

    # counting occurrences of the bigram in the corpus's bigrams
    bi_count = bigrams.count(sentence_bigrams[i])

    # calculating the chance and total chance using add-1-smoothing
    chance = (bi_count + 1) / (u_count + token_count)
    total_chance = total_chance * chance


# printing the sentence and it's chance
print("The sentence is : " + sentence)
print("The chance is " + f"{Decimal(total_chance * 100):.2E}" + "%")