#analyze_tweets.py
import nltk
import nltk.data
import sqlite3

conn = sqlite3.connect('tweets.db')


print('***** MOST FREQUENTLY MENTIONED AUTHORS *****')
cur = conn.cursor()
q = 'SELECT * FROM Authors ORDER BY mention_count DESC LIMIT 10'
r = cur.execute(q)
# for row in r:
    # print(str(row[1]) + ' is mentioned ' + str(row[2]) + 'times')



# Print the 5 most frequently mentioned authors in the entire corpus

print('*' * 20, '\n\n') # dividing line for readable output



print('***** TWEETS MENTIONING AADL *****')
cur = conn.cursor()
q = 'SELECT tweet_text FROM Tweets JOIN Mentions ON Tweets.tweet_id = Mentions.tweet_id JOIN Authors ON Mentions.author_id = Authors.author_id WHERE username = "aadl"'
r = cur.execute(q)
# for row in r:
    # print(row[0])
# Print all tweets that mention the twitter user 'aadl' (the Ann Arbor District Library)

print('*' * 20, '\n\n')



print('***** MOST COMMON VERBS IN UMSI TWEETS *****')

q = 'SELECT * FROM Tweets WHERE Tweets.author_name = "umsi"'
r = cur.execute(q)
dic = {}
for row in r:
    tokens = nltk.word_tokenize(row[1])
    tagged_tokens = nltk.pos_tag(tokens)
    for i in tagged_tokens:
        if i[1] == 'VB':
            if i[0] not in dic:
                dic[i[0]] = 0
            dic[i[0]] += 1
dic_verb = sorted(dic, key = lambda x: dic[x], reverse = True)
for i in dic_verb[1:11]:
    print(str(i) + "(" + str(dic[i]) + "times )")

# Print the 10 most common verbs ('VB' in the default NLTK part of speech tagger)
# that appear in tweets from the umsi account

print('*' * 20, '\n\n')



print('***** MOST COMMON VERBS IN UMSI "NEIGHBOR" TWEETS *****')

# Print the 10 most common verbs ('VB' in the default NLTK part of speech tagger)
# that appear in tweets from umsi's "neighbors", giving preference to tweets from
# umsi's most "mentioned" accounts
q = 'SELECT * FROM Tweets WHERE Tweets.author_name != "umsi"'
r = cur.execute(q)
dic = {}
for row in r:
    tokens = nltk.word_tokenize(row[1])
    tagged_tokens = nltk.pos_tag(tokens)
    for i in tagged_tokens:
        if i[1] == 'VB':
            if i[0] not in dic:
                dic[i[0]] = 0
            dic[i[0]] += 1
dic_verb = sorted(dic, key = lambda x: dic[x], reverse = True)
for i in dic_verb[0:11]:
    if i != '@':
        print(str(i) + "(" + str(dic[i]) + "times )")
    else:
        continue
print('*' * 20, '\n\n')


conn.close()
