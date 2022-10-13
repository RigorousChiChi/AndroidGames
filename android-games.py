# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

games = pd.read_csv('android-games.csv')

clean_games = games.copy()
clean_games['rating_sum'] = clean_games['5 star ratings'] + clean_games['4 star ratings'] + clean_games['3 star ratings'] + clean_games['2 star ratings'] + clean_games['1 star ratings']
clean_games = clean_games.loc[np.abs(clean_games['total ratings'] - clean_games['rating_sum']) < 10]
clean_games['installs_int'] = np.where(clean_games['installs'].str.contains('M'),1000000,1000)
clean_games['installs_30'] = clean_games.apply(lambda x: x['installs_int']/(x['growth (30 days)']/100+1),axis = 1)
clean_games['installs_60'] = clean_games.apply(lambda x: x['installs_30']/(x['growth (60 days)']/100+1),axis = 1)
clean_games['5_1-star-ratio'] = clean_games['5 star ratings']/clean_games['1 star ratings']
clean_games['5-star-ratio'] = clean_games['5 star ratings']/clean_games['total ratings']
cat_installs = clean_games.groupby('category')['installs_int'].sum().reset_index()
Most_Ratings = clean_games.sort_values('total ratings',ascending = False).iloc[0]
word_ranks = games.loc[games['category'] == 'GAME WORD'].loc[games.duplicated('rank')]

st.sidebar.subheader('Table of contents')
st.sidebar.write('1. ','<a href=#case-study-on-top-android-games>Introduction</a>', unsafe_allow_html=True)
st.sidebar.write('2. ','<a href=#data-cleaning>Data cleaning</a>', unsafe_allow_html=True)
st.sidebar.write('3. ','<a href=#exploratory-data-analysis>Exploratory data analysis</a>', unsafe_allow_html=True)
st.sidebar.write('4. ','<a href=#conclusion>Conclusion</a>', unsafe_allow_html=True)
st.title('Case Study on Top Android Games')
st.markdown('<p style="font-size:30px">Goal of this case study</p>',unsafe_allow_html=True)
#st.markdown('<p style="color:blue;font-size:24px">This is demoss text</p>',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">There are millions of people who play Android Games. And there are thousands of games out there for players to download and play. What kind of games do people like to play, and what types of games should developers continue to create?',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">The goal of this case study is to find out what types and category of Android games create the most profits, analyzing the total amount of installs, average ratings, and growth. This dataframe contains a total of 15 columns: title, average ratings, 1 start to 5 star ratings, growth in the past 30-60 days, installs, and category. The category has a subset of 17 game categories, and this is an important feature because it could help us group games by categories, which is extrememly helpful for our research question since our goal is to know which category is the most popular and understand what type of game developers should develop.',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">',unsafe_allow_html=True)
st.dataframe(games.head(10))
st.markdown('<p style="font-size:18px">Before we actually get into the dataset, we should first define and understand what does some of the columns represent and how was they calculated.',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">The first important column is the rank column. It is justified by considering all columns related to how popular the game is, including the growth, total amount of installs, total amount of ratings, and its average rating. The second column is the growth in the past 30 and 60 days. It is mainly calculated with the percentage of growth from the total installs in the past certain amount of time, while also considering the growth in ratings. But since it mainly focuses on the growth in installs we could understand it as the growth in total amount of installs calculated in percentage. The last column is the total ratings. By looking at it we briefly know how popular the game currently is or in the past.',unsafe_allow_html=True)
###############################################Data Cleaning##################################
st.header('Data Cleaning')
st.markdown('<p style="font-size:18px">The description in the original dataset says that there are 100 games in each cateogry, but I found out for some categories there are more than 100 games. The following line of code demonstrates it:<p>',unsafe_allow_html=True)
st.code("games['category'].value_counts()")
st.dataframe(games['category'].value_counts())
st.markdown('<p style="font-size:18px">My hypothesis on why are there more games in some categories is that there are duplicates. In GAMES CARD, GAME WORD and GAME CASUAL there are obviously more games than 100. Duplicate is very likely because the original data only had 100 games, and it is not possible to have games randomly appear.<p>',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">The potential problems that couuld be caused by this flaw are massive. The first issue we might run into in the future is that when calculating the average the number the result is very likely to be wrong. That could easily make us get the wrong conclusion and make the entire study worthless. The second problem is that if we want to select a specific game to compare it with the average, we might get its duplicate with the wrong data. That would also affect our conclusion.<p>',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">After going more specific into the code, I found out the .values code could see all of the ranks in the rank column, thus easily identifing all of the duplicates. So I decided to find the duplicates for the "GAME WORD" category first.',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">To begin with, I needed to assign the ranks in GAME WORD to a variable that makes it easier to calculate. So I used the .loc code as shown below. I started with finding the GAME WORD category and then went in details with the ranks.',unsafe_allow_html=True)
st.code("word_ranks = games.loc[games['category'] == 'GAME WORD'].loc[games.duplicated('rank')]")
st.markdown('<p style="font-size:18px">Next, we should find the specific ranking of each game in GAME WORD. Using the .value code would show a list of all the raking in GAME WORD category, and then we could read through it and find all the duplicates.',unsafe_allow_html=True)
st.code("word_ranks['rank'].values")
word_ranks[["title","rank"]]
st.markdown('<p style="font-size:18px">After looking at the list, we find out that the duplicates are ranked 21 and 33, each having three games that are ranked as the same number, and now we should select them out of the dataframe specifically.',unsafe_allow_html=True)
games[['title','rank','total ratings','5 star ratings','4 star ratings','3 star ratings','2 star ratings','1 star ratings']].loc[1644:1646]
games[['title','rank','total ratings','5 star ratings','4 star ratings','3 star ratings','2 star ratings','1 star ratings']].loc[1660:1662]
st.markdown('<p style="font-size:18px">If we look at the information of these columns, we will soon realize although the total ratings are the same for all three duplicates, the amount of five star to one star ratings does not match with each other. That shows that only one among the three is the correct data.',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">To locate the correct row, we need to add all of the ratings from 1 star to 5 star, and see if it matches with the total rating. Adding each of the rows together is very complicated and will take a lot of time, so I defined a new column called "ratings sum", which is the sum of 1 star to 5 star ratings and will be used to compare with the "total rating" column.',unsafe_allow_html=True)
st.code("games['rating_sum'] = games['5 star ratings'] + games['4 star ratings'] + games['3 star ratings'] + games['2 star ratings'] + games['1 star ratings']")
st.markdown('<p style="font-size:18px">After defining this new columnm, all we need to do is locate and select all the rows that "rating_sum" matches with "total ratings". To accomplish that goal, we need to use the .loc code to find all the rows that has no difference between the two columns and account it as a new dataframe called clean games (since it deleted all of the duplicates) as the following:',unsafe_allow_html=True)
st.code("clean_games = games.loc[np.abs(games['total ratings'] - games['rating_sum']) < 10]")
st.markdown('<p style="font-size:18px">This line of code locates all of the rows that the absolute value of "total ratings" - "rating_sum" is less than 10. Subtracting these two columns would show how much difference they have, and I decided to count all +-10 rows since there might be slight difference in between. The ablsolute value is because I am not sure if the "total ratings" column is always greater than the "rating_sum".',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">The dataframe below is the final "clean_games" dataframe that deleted all duplicated in the original dataframe.',unsafe_allow_html=True)
clean_games
cat_mean =games.groupby('category').mean()
st.dataframe(cat_mean)

st.header('Exploratory data analysis')
#############################################5 Star Ratings###################################
st.markdown('<p style="font-size:18px">After making sure the dataset is clean, we should move back to the original goal of this case study, which is to find which category or type of games are the most popular, and makes the most amount of money. I think to approach this question, we should begin with the amount of 5 star ratings, since the amount of people that give 5 star ratings (thinks the game is good) is directly linked to how popular it is.<p>',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">The code below would generate a bar graph that shows the difference with the amount of 5 star ratings, and you can hover your mouse to get more detail about each bar.<p>',unsafe_allow_html=True)
st.code("px.bar(clean_games,x = 'category',y = '5 star ratings',color = 'category,hover_name = 'title'',color_discrete_sequence = px.colors.qualitative.Antique,title = '',width = 800, height = 800)")
st.markdown('<p style="color:blue; font-size:19px">Number of 5 Star Rating Per Category for each game<p>',unsafe_allow_html=True)
fig1 = px.bar(clean_games,x = "category",y = "5 star ratings",color = "category",hover_name = "title",color_discrete_sequence = px.colors.qualitative.Antique,title = '',width = 800, height = 800)
st.plotly_chart(fig1)
st.markdown('<p style="font-size:18px">Looking at the chart, we can see that the categories with the most 5 star ratings are GAMES ACTION, GAMES CASUAL, and GAMES SRATEGY. They have a clear difference among the other categories for 5 star ratings. Among these three categries, GAMES ACTION has the most 5 star ratings.In this case, according to how many people like and gives a good rating of the game, GAMES ACTION will be the best category to develop games.<p>',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">Note: the amount of 5 star rating could only be  part of your consideration of which game to develop, since if there are a lot of 1 star ratings as well it might not be as popular or good as the category of game for you to develop.<p>',unsafe_allow_html=True)
#################################################Growth#######################################
st.subheader('Growth')
st.markdown('<p style="font-size:18px">Next, besides considering the amount of 5 star ratings each category has, we need to look at their growth as well. If we do not look at the growth and only consider the  amount of 5 star rating when deciding what games we should develop, there might be the possibility where a category gained a lot of 5 star ratings a long time before, when it was extremely popular, but now being outmoded and nobody cares about it. That would result in no one installing the game.<p>',unsafe_allow_html=True)
st.markdown('<p style="color:blue; font-size:19px">Growth in the past 60 days in each category<p>',unsafe_allow_html=True)
growth_60_top50 = clean_games.sort_values(['growth (60 days)','average rating'],ascending = False).reset_index(drop = True).head(50)
fig2 = px.sunburst(growth_60_top50,names = 'category',values = 'growth (60 days)',path = ['category','title'],width = 800, height = 800)
st.plotly_chart(fig2)
st.markdown('<p style="font-size:18px">This graph shows the amount of growth that each category and their top games had gained in the past 60 days. In this graph, we can see that GAME MUSIC, GAME TIVIA and GAME EDUCATIONAL had gained the most growth in the past two months. But does that mean they are the most popular games currently? The growth in calculated in percentage, and a high percentage of growth does not directly result in a high growth in the direct number of installs. That is because the caltulation of the actual number of growth (60 days or 30 days) is total installs * percentage in growth. If the total amount of installs is very low, then it is much easier to get a high percentage for growth.From that we can conclude that if you want your game to develp quicker in the beginning stage, then you should consider categories such as GAME MUSIC, GAME TRIVIA, and GAME EDUCATIONAL. If you want a more continuous development or ready to put in a lot of resource to make the game to into a very popular game in the future, then it would better to choose the more popular categories.<p>',unsafe_allow_html=True)
st.markdown('<p style="font-size:18px">This tells us that if we directly look at the growth we would conclude that these less popular categories grows quicker, however the total amount of installs grows quicker in the more popular categories. So if you want to make a small game that grows quickly you should consider the less popular categories.<p>',unsafe_allow_html=True)
################################################Installs######################################
st.subheader('Installs')
st.markdown('<p style="font-size:18px">Last but not least, we should look directly at the amount of installs that each category have in total to see clearly which is the most popular and how many people actually installed the game. Below is a bar graph of the total amount of installs in each category.<p>',unsafe_allow_html=True)
st.markdown('<p style="color:blue; font-size:19px">The total amount of installs in each category<p>',unsafe_allow_html=True)
games['installs_int'] = np.where(games['installs'].str.contains('M'),1000000,1000)
games['installs_int'] = games['installs'].str.replace('M|k','',regex = True).str.strip().astype(float)*games['installs_int']
st.markdown('<p style="font-size:18px">The first step that we need to do in order to display the data in a graph is get the information that we need. In this case we need the total installs in each category. To get it, we need to use the "groupby" function to groud all of the games that has the same category and then sum the installs together, so we add a sum function at the last part to sum all of the installs for each game."<p>',unsafe_allow_html=True)
st.code("cat_installs = games.groupby('category')['installs_int'].sum().reset_index()")
cat_installs = games.groupby('category')['installs_int'].sum().reset_index()
st.markdown('<p style="font-size:18px">After we gave the data we need stored in category-installs (cat-installs), we should use the bar function in plotlyx to generate the bar graph. To do that, we use the code below.<p>',unsafe_allow_html=True)
st.code("px.bar(cat_installs,x = 'category',y = 'installs_int')")
fig3 = px.bar(cat_installs,x = 'category',y = 'installs_int')
st.plotly_chart(fig3)
st.markdown('<p style="font-size:18px">In this bar graph, we can directly see that the categories with the most amount of installs are actually the ones with the most amount of 5 star ratings. That makes the 5 star rating graph look very similiar ratio-wise to the installs graph. We easily could find out that same as the 5 star rating graph GAMES ARCADE, GAME CASUAL, and GAME ACTION. However, there is a clear difference between the installs graph and the 5-star rating graph, and the difference in GAME STRATEGY. GAME STRATEGY have a lot of 5-star ratings compared to the amount of installs that it has, and I believe that means although not as many people downloads this\'s category\'s game as the other extremely popular categories do, more people that actually downloaded likes this category. I think that means GAME STRATEGY would be another great category to deveop games in.<p>',unsafe_allow_html=True)
############################################Conclusion########################################
st.header('Conclusion')
st.markdown('<p style="font-size:18px">From the results we got in the exploratory analysis, we can start making conclusions to answer our question of which type of games are the best to develop. If we want to develop a game that grows quickly at the early stages and maybe consider selling it soon, GAME MUSIC, GAME EDUCATIONAL, GAME TRIVIA and other categories that aren\'t as popular would be the best choice, since their installs and ratings grows the quickest. If you would like to make your game big with some ambition, you should consider developing your game in the top categories such as GAME STRATEGY, GAME ARCADE, GAME CASUAL, and GAME ACTION. Note that GAME STRATEGY has the highest ratio of five star ratings among these give categories, GAME ACTION has the highest total amount of 5 star ratings,  and GAME CASUAL has the most amount of installs. You can make adjustments according to your game and what game do you want to make.<p>',unsafe_allow_html=True)































