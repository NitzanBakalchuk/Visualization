import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Specify the backend explicitly, e.g., 'Agg'
import plotly.express as px

import matplotlib.pyplot as plt


df15 = pd.read_csv("2015.csv")
df16 = pd.read_csv("2016.csv")
df17 = pd.read_csv("2017.csv")
df18 = pd.read_csv("2018.csv")
df19 = pd.read_csv("2019.csv")
df = pd.read_csv("df.csv")

# Define UI
def app():
################################## world map #########################################################
    st.title("World Happiness Visualization")
    st.header("World Map -Happiness Rank by Country")
    st.write("The word map below shows the happiness ranking around the globe,")
    st.write("please choose the year you want to present at the bar below and start to explore!")
    date = st.slider("Year:", min_value=2015, max_value=2019, value=2015)
    df5 = df15
    
    if date == 2015:
        df5 = df15
    elif date == 2016:
        df5 = df16
    elif date == 2017:
        df5 = df17
    elif date == 2018:
        df5 = df18
    elif date == 2019:
        df5 = df19

    # Create the choropleth map
    fig = px.choropleth(df5, locations='Country', locationmode='country names',
                        color='Rank',
                        labels={'Value': 'Score', 'Country': 'Country'},
                        hover_name='Country',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        hover_data={'Rank': True, 'Country': True, 'Score': True},
                        projection='natural earth')

    # Display the map
    st.plotly_chart(fig, use_container_width=True)
########################  Happiness ranking  ################################################################

    st.header("Rank changes by years")
    st.write('Explore the difference in Happiness ranking of countries between the selected years')
    st.write('note: you can also select none option at the country selection and sort the values by pressing the top of each column.')
    years = ['2015', '2016', '2017', '2018', '2019']
    all_country = df15['Country'].unique().tolist()
    selected_country = st.selectbox("Select a country", [None] + all_country)
    col1, col2 = st.columns([1, 1])
    selected_year_1 = col1.selectbox("Select Year 1", [None] + years)
    selected_year_2 = col2.selectbox("Select Year 2", [None] + years)
    df1 = df15
    df2 = df19

    if selected_year_1 == '2015':
        df1 = df15
    elif selected_year_1 == '2016':
        df1 = df16
    elif selected_year_1 == '2017':
        df1 = df17
    elif selected_year_1 == '2018':
        df1 = df18
    elif selected_year_1 == '2019':
        df1 = df19

    if selected_year_2 == '2015':
        df2 = df15
    elif selected_year_2 == '2016':
        df2 = df16
    elif selected_year_2 == '2017':
        df2 = df17
    elif selected_year_2 == '2018':
        df2 = df18
    elif selected_year_2 == '2019':
        df2 = df19

    dfall = pd.merge(df1[['Country', 'Rank']], df2[['Country', 'Rank']], on='Country')
    dfall.columns = ['Country', 'Rank Year 1', 'Rank Year 2']
    dfall['Rank Change'] =   dfall['Rank Year 1'] -dfall['Rank Year 2']

        
    def color_survived(val):
        if val == 0:
             color = 'white'
        elif val > 0 :
            color = '#99ff99'
        else:
            color = '#ffcc99'
    
        return f'background-color: {color}'
    #
    # st.dataframe(dfall.style.apply(highlight_survived, axis=1))
    if selected_country is None:
        st.dataframe(dfall.style.applymap(color_survived, subset=['Rank Change']))
    
    else:
        st.subheader("Rank Table")
        filtered_df = dfall[dfall['Country'] == selected_country]
        filtered_df = filtered_df[['Country', 'Rank Year 1', 'Rank Year 2', 'Rank Change']]
        st.dataframe(filtered_df.style.applymap(color_survived, subset=['Rank Change']))
   
############################# Feature Correlation With Happiness Score ##########################################
    st.header("Features importance by Happiness Score")
    st.write("Choose a year and watch the features importance to the happiness score")
    selected_year_3 = st.selectbox("Select Year",  years)
    st.write("Choose different countries and watch how they correlates to the pie chart")
    years = ['2015', '2016', '2017', '2018', '2019']
    
    # col1, col2 = st.columns([2, 1])
    selected_country_3 = st.selectbox("Select country to explore",  all_country)
    
    df3 = df15
    if selected_year_3 == '2015':
        df3 = df15
    elif selected_year_3 == '2016':
        df3 = df16
    elif selected_year_3 == '2017':
        df3 = df17
    elif selected_year_3 == '2018':
        df3 = df18
    elif selected_year_3 == '2019':
        df3 = df19
    
    if selected_year_3 == '2015':
        custom_colors = ['#ff9999','#66b3ff', '#99ff99',  '#ffcc99', '#c2c2f0', '#ffb3e6']
    else:
        custom_colors = ['#ff9999','#99ff99', '#66b3ff',  '#ffcc99', '#c2c2f0', '#ffb3e6']
    
    s = df3[df3['Country'] == selected_country_3].drop(['Country','Rank', 'Score'], axis=1)
    fig = px.bar(s.transpose())
    fig.update_traces(marker_color=custom_colors)
    
    features = ['Economy', 'Generosity', 'Freedom', 'Family', 'Trust', 'Health']
    
    # Filter the correlation table based on selected features
    df3 = df3.drop('Country', axis=1)
    correlation_table = df3.corr()[['Score']]
    correlation_table = correlation_table.loc[features].sort_values(by='Score', ascending=False)
    
    # Taking the absolute values of the correlation values
    correlation_table['Score'] = correlation_table['Score'].abs()
    correlation_table['Score'] = pd.to_numeric(correlation_table['Score'])
    # Create a pie chart using Plotly Express
    fig4 = px.pie(correlation_table, values='Score', names=correlation_table.index)
    # Customize the chart colors
    custom_colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']
    fig4.update_traces(marker=dict(colors=custom_colors))
    
    
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig, use_container_width=True)
    col2.plotly_chart(fig4, use_container_width=True)
    # # Display the chart
    # st.plotly_chart(fig4)

################################ 3 most influential features #######################################################
    st.header('Feature trend by top/bottom countries Rank')
    st.write('The graph below presents the top 5 ranked countries in the green lines and the bottom 5 ranked countries in purple.')
    st.write('Choose a feature and countries and compare their trend to the top/bottom ranked countries trend by the selected feature.')
    st.write('Here you can understand why countries changed their rank by the years and dive into the countries comparison.')
    features = ['Economy', 'Family','Health','Freedom', 'Trust', 'Generosity' ]
    ii = ['Switzerland', 'Iceland', 'Denmark', 'Norway', 'Finland', 'Togo', 'Burundi', 'Syria', 'Burkina Faso', 'Afghanistan']
    
    dfs = {'2015': df15[['Country'] + features],
           '2016': df16[['Country'] + features],
           '2017': df17[['Country'] + features],
           '2018': df18[['Country'] + features],
           '2019': df19[['Country'] + features]}
    
    dict_economy = {}
    dict_family = {}
    dict_health = {}
    dict_trust = {}
    dict_Generosity = {}
    dict_Freedom = {}
    for values in dfs.values():
        for _, row in values.iterrows():
            country = row['Country']
            if country in dict_economy:
                dict_economy[country].append(row.tolist()[1])
                dict_family[country].append(row.tolist()[2])
                dict_health[country].append(row.tolist()[3])
                dict_trust[country].append(row.tolist()[4])
                dict_Generosity[country].append(row.tolist()[5])
                dict_Freedom[country].append(row.tolist()[6])
            else:
                dict_economy[country] = [row.tolist()[1]]
                dict_family[country] = [row.tolist()[2]]
                dict_health[country] = [row.tolist()[3]]
                dict_trust[country] = [row.tolist()[4]]
                dict_Generosity[country] = [row.tolist()[5]]
                dict_Freedom[country] = [row.tolist()[6]]
    
    fig5 = go.Figure()
    
    years = ['2015', '2016', '2017', '2018', '2019']
    colors = ['green', 'green', 'green', 'green', 'green','rgb(171, 50, 96)','rgb(171, 50, 96)','rgb(171, 50, 96)','rgb(171, 50, 96)','rgb(171, 50, 96)']
    high_countries1 = ['Switzerland', 'Iceland', 'Denmark', 'Norway', 'Finland', 'Togo', 'Burundi', 'Syria', 'Burkina Faso', 'Afghanistan']
    
    categories = ['Economy', 'Family','Health','Freedom', 'Trust', 'Generosity' ]

    col1, col2 = st.columns([1, 3])
    selected_features = col1.selectbox('Select features to display:', categories)
    selected_country2 = col2.multiselect("Select country", [None] + all_country)
    dict_feature = dict_economy
    if selected_features == 'Economy':
        dict_feature = dict_economy
    elif selected_features == 'Family':
        dict_feature = dict_family
    elif selected_features == 'Health':
        dict_feature = dict_health
    elif selected_features == 'Generosity':
        dict_feature = dict_Generosity
    elif selected_features == 'Freedom':
        dict_feature = dict_Freedom
    elif selected_features == 'Trust':
        dict_feature = dict_trust

    for i, country in enumerate(high_countries1):
        fig5.add_trace(go.Scatter(x=years, y=dict_feature[country], name=high_countries1[i], line_width=2.0, line=dict(color=colors[i])))
    dict_feature[None] = []
    for key in selected_country2:
        fig5.add_trace(go.Scatter(x=years, y=dict_feature[key], name=key, line_width=2.0, line=dict(color='orange')))


    fig5.update_layout(title=f'{selected_features} through the years by country',
                      xaxis_title='Year',
                      yaxis_title='Value',
                      titlefont={'size': 25, 'family':'Serif'},
                      showlegend=True,
                      paper_bgcolor='lightgray',
                      width=750, height=500,
                     )
    st.plotly_chart(fig5)


##################################################################################################################
# Run the app
app()
