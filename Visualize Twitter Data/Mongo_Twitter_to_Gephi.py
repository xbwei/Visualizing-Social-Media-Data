'''
Created on Feb 20, 2017

@author: Xuebin Wei
www.lbsocial.net
'''

from pymongo import MongoClient

import networkx as nx


client = MongoClient()

db = client.tweet_db

tweet_collection = db.tweet_collection

tweet_cursor = tweet_collection.find()

hashtag_graph = nx.Graph() 
# undirected network, hashtags in a single tweet form connections to others
# weight is the number of such connections being formed from the entire data

mentioned_user_graph =nx.Graph() 
# undirected network, users mentioned in a single tweet form connections to others
# weight is the number of such connections being formed from the entire data

user_to_mention_graph = nx.DiGraph()
# directed network, each connection is from author to  one of the mentioned users in a single tweet
# weight is the number of such connections being formed from the entire data


i = 0        
for document in tweet_cursor:

   
    try:
        '''
        create hashtag network
        '''
 
        if len(document["entities"]["hashtags"]) !=0:
            for hashtag1 in document["entities"]["hashtags"]:
                hashtag1_text = hashtag1["text"]
                for hashtag2 in document["entities"]["hashtags"]:
                    hashtag2_text = hashtag2["text"]
                    if hashtag1_text != hashtag2_text:
                        if hashtag_graph.has_edge(hashtag1_text, hashtag2_text):
                            hashtag_graph[hashtag1_text][hashtag2_text]['weight']= 0.5 + hashtag_graph[hashtag1_text][hashtag2_text]['weight']
                        else:
                            hashtag_graph.add_edge(hashtag1_text,hashtag2_text, weight = 0.5)
    except:
        print('wrong in adding hashtags')
        print (document["entities"]["hashtags"])
        continue
     
     
     
    try:
        '''
        create mentioned user network
        '''
 
        if len(document["entities"]["user_mentions"]) !=0:
            for mentioned_user1 in document["entities"]["user_mentions"]:
                mentioned_user1_name = mentioned_user1["screen_name"]
                for mentioned_user2 in document["entities"]["user_mentions"]:
                    mentioned_user2_name = mentioned_user2["screen_name"]
                    if mentioned_user1_name != mentioned_user2_name:
                        if mentioned_user_graph.has_edge(mentioned_user1_name, mentioned_user2_name):
                            mentioned_user_graph[mentioned_user1_name][mentioned_user2_name]['weight']= 0.5 + mentioned_user_graph[mentioned_user1_name][mentioned_user2_name]['weight']
                        else:
                            mentioned_user_graph.add_edge(mentioned_user1_name,mentioned_user2_name, weight = 0.5)
    except:
        print('wrong in adding mentioned users')
        print (document["entities"]["user_mentions"])
        continue

    try:
        '''
        create user to mentioned user network
        '''
        
        if len(document["entities"]["user_mentions"])!=0:
            ego_user = document["user"]["screen_name"]
            for mentioned_user in document["entities"]["user_mentions"]:
                actor_user = mentioned_user["screen_name"]
                if user_to_mention_graph.has_edge(ego_user, actor_user):
                    user_to_mention_graph[ego_user][actor_user]['weight']= 1.0 + user_to_mention_graph[ego_user][actor_user]['weight']
                else:
                    user_to_mention_graph.add_edge(ego_user,actor_user, weight = 1.0)


    except:
        print('wrong in adding users')
        print (ego_user)
        print (document["entities"]["user_mentions"])
        continue
    
    i = i+1
           

nx.write_gexf(hashtag_graph,"hashtag_graph.gexf")
nx.write_gexf(mentioned_user_graph,"meitoned_user_graph.gexf")
nx.write_gexf(user_to_mention_graph,"user_to_mention_graph.gexf")

print ('processed ',i,' tweets.')

print ('number of nodes in hashtag network:', hashtag_graph.number_of_nodes())
print ('number of edges in hashtag network:', hashtag_graph.number_of_edges())

print ('number of nodes in mentioned user network:', mentioned_user_graph.number_of_nodes())
print ('number of edges in mentioned user network:', mentioned_user_graph.number_of_edges())

print ('number of nodes in user to mention network:', user_to_mention_graph.number_of_nodes())
print ('number of edges in user to mention network:', user_to_mention_graph.number_of_edges())
