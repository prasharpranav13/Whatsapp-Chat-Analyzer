import pandas as pd
from urlextract import URLExtract
extractor=URLExtract()
from wordcloud import WordCloud
from collections import Counter
import emoji


def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    # total words
    words = []
    for message in df['message']:
        words.extend(message.split())  # will split all the messages
    media_df=df[df['message']=='<Media omitted>\n']
    media_messages=media_df.shape[0]
    #total links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    total_links=len(links)
    return num_messages, words,media_messages,total_links
    #df[df['user']==selected_user] will give all the rows where user is selected user
    #shape gives (row,col) hence 0th gives no of messages

def most_busy_users(df):
    x = df['user'].value_counts().head()  # ->top 5 users
    df=round((df['user'].value_counts() / df['user'].shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percentage'})
    return x,df


def create_wordCloud(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    # all rows without group notification
    df[df['user'] != 'group_notification']
    # new df
    tmp = df[df['user'] != 'group_notification']

    # removing media omitted
    tmp = tmp[tmp['message'] != '<Media omitted>\n']

    # removing stoppers
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return  " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    tmp['message'].apply(remove_stop_words)
    #generating wordcloud
    df_wc=wc.generate(tmp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]


    # all rows without group notification
    df[df['user'] != 'group_notification']
    # new df
    tmp = df[df['user'] != 'group_notification']

    # removing media omitted
    tmp = tmp[tmp['message'] != '<Media omitted>\n']

    # removing stoppers
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []
    for message in tmp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        words.extend(message.split())

    # counting freq of words
    # 20 most frequent words
    Counter(words).most_common(20)
    # converting to dataframe
    common_word_df=pd.DataFrame(Counter(words).most_common(20))
    return common_word_df

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    daily_timeline=df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def heatmap(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    activity_heatmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_heatmap
