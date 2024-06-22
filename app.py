import streamlit as st
import matplotlib.pyplot as plt


import helper
import preprocessor
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a text file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    #this file is a stream of bytedata for now
    #we'll convert it to string
    data=bytes_data.decode("utf-8")
    #st.text(data)-to show file data on screen
    df=preprocessor.preprocess(data)
    #displaying datatframe
    # st.dataframe(df)
    #dropdown to select user-we'll need unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')#inserting overall at 0th pos
    selected_user=st.sidebar.selectbox('Show analysis wrt',user_list)
    # if this btn is clicked
    if st.sidebar.button('Show Analysis'):
        st.title('Top Statistics')
        num_messages,words,media_messages,total_links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(len(words))
        with col3:
            st.header("Media shared")
            st.title(media_messages)
        with col4:
            st.header("Total links shared")
            st.title(total_links)
    #monthly timeline
    st.title('Monthly Timeline')
    timeline=helper.monthly_timeline(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(timeline['time'], timeline['message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    #daily timeline
    daily_timeline=helper.daily_timeline(selected_user,df)
    st.title('Daily Timeline')
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    #activity map
    st.title('Activity Map')
    col1,col2=st.columns(2)
    with col1:
        st.header('Most Busy Day')
        busy_day= helper.week_activity_map(selected_user, df)
        fig,ax=plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header('Most Busy Month')
        busy_month= helper.month_activity_map(selected_user, df)
        fig,ax=plt.subplots()
        ax.bar(busy_month.index,busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    #activity heatmap
    st.title('Weekly Activity Heatmap')
    activity_heatmap=helper.heatmap(selected_user,df)
    fig,ax=plt.subplots()
    ax=sns.heatmap(activity_heatmap)
    st.pyplot(fig)
    #finding the busiest users in the group(grp level)
    if selected_user=='Overall':
        st.title('Most Busy Users')
        x,percentage_df=helper.most_busy_users(df)
        fig,ax=plt.subplots()
        col5,col6=st.columns(2)
        with col5:
            ax.bar(x.index, x.values,color='green')
            # to make names on xaxis vertical for better visibility
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col6:
            st.dataframe(percentage_df)
    #wordcloud
    st.title('Wordcloud')
    df_wc=helper.create_wordCloud(selected_user,df)
    #df_wc is an image , hence use matplotlib to show
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    #most common words
    st.title('Most common words')
    common_word_df=helper.most_common_words(selected_user,df)
    # st.dataframe(common_word_df)
    fig,ax=plt.subplots()
    ax.barh(common_word_df[0],common_word_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    #emoji analysis
    st.title('Emoji  Analysis')
    col1,col2=st.columns(2)
    emoji_df=helper.emoji_helper(selected_user,df)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax=plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        st.pyplot(fig)

