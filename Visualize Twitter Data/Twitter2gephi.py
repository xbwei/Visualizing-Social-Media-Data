'''
Created on Nov 11, 2015

@author: Xuebin Wei
@email: weixuebin@gmail.com
'''
import csv
import networkx as nx



csvfile = open('tweet.csv')
# data can be downloaded by using https://github.com/xbwei/GetTwitter/blob/master/Twitter/GetTwitter2CSV.py

reader = csv.DictReader(csvfile)

nxg = nx.Graph()
i = 0
for row in reader:

    people = []
    people.append(row['tweetuser'])
    if row['mention']!='':
#         print row['mention']
        i = i+1
        for mentioned_user in (row['mention'].split(",")[:-1]):
            
#             print '\t',mentioned_user
            people.append(mentioned_user)
    if row['replyuser'] !='':
        people.append(row['replyuser'])
    if row['retweetuser'] !='':
        people.append(row['retweetuser'])
    unique_people = list(set(people))
    if len(unique_people) > 1:
        for people1 in unique_people:
            for people2 in unique_people:
                if people1 != people2:
                    if nxg.has_edge(people1, people2):
                        nxg[people1][people2]['weight'] =0.5 + nxg[people1][people2]['weight']
        #                             print nxg.number_of_edges(people1, people2)
                    else:
                        nxg.add_edge(people1,people2,weight = 0.5)
    #                         print nxg[people1][people2]
nx.write_gexf(nxg, "tweet.gexf")
