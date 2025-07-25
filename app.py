import streamlit as st
import pandas as pd
import preprocessor , helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff




df = pd.read_csv('C:/Users/HP/Desktop/olympic project/athlete_events.csv')
regions_df = pd.read_csv('C:/Users/HP/Desktop/olympic project/regions.csv')

df = preprocessor.preprocess(df,regions_df)
st.sidebar.title("Olympic analysis")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')

)



if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")


    years,country = helper.year_country_list(df)
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)


    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall Analysis' and selected_country == 'Overall Analysis':
        st.title("Overall Tally")
    if selected_year != 'Overall Analysis' and selected_country == 'Overall Analysis':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall Analysis' and selected_country != 'Overall Analysis':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall Analysis' and selected_country != 'Overall Analysis':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == "Overall Analysis":

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athletes)

    st.title("Participating Nations over the Years")
    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x='Edition', y='No of Countries')
    st.plotly_chart(fig)


    st.title("Events over the Years")
    events_over_time = helper.all_events_over_time(df)
    fig = px.line(events_over_time, x='Edition', y='No of Events')
    st.plotly_chart(fig)

    st.title("Athletes over the Years")
    athletes_over_time = helper.all_athletes_over_time(df)
    fig = px.line(athletes_over_time, x='Edition', y='No of Athletes')
    st.plotly_chart(fig)

    st.title("No of Events over time(Every Sport)")
    fig,axis = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport' , 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot = True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox("Select a Sport",sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_region = st.sidebar.selectbox("Select a Country",country_list)
    
    country_df = helper.country_wise_medals(df,selected_region)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_region + ' Medal Tally over the years')
    st.plotly_chart(fig)

    
    st.title(selected_region + ' excels in the following sports')
    fig,axis = plt.subplots(figsize=(20,20))
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == selected_region ]
    sns.heatmap(new_df.pivot_table(index = 'Sport', columns = 'Year', values = 'Medal', aggfunc = 'count').fillna(0), annot = True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_region)
    top10_df = helper.most_successful_countrywise(df, selected_region)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4], ['Overall Age' , 'Gold Medalist' , 'Silver Medalist' , 'Bronze Medalist'], show_hist=False , show_rug=False)
    fig.update_layout(autosize=False , width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)


    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)


    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],
                     y=temp_df['Height'],
                     hue=temp_df['Medal'],
                     style=temp_df['Sex'],
                     s=80)

    st.pyplot(fig)


    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)





    




    



    
    

    

    