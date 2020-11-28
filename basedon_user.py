import streamlit as st

import pandas as pd

import plotly.express as px
from plotly.graph_objs import *
import plotly.graph_objects as go
import plotly as py
import plotly.io as pio
pio.renderers.default = 'chrome'



st.title('Recommended for you!')

cosine_sim = pd.read_pickle('cosine_sim.pickle')
indices = pd.read_pickle('indices.pickle')
df = pd.read_pickle('df.pickle')
reviews = pd.read_pickle('clean_review.pickle')
raw = pd.read_pickle("clean_data.pickle")


name = st.sidebar.text_input(''' Enter your user name''')

user = reviews[(reviews["User_Name"] == name) & (reviews["Polarity"] == "Positive")].reset_index(drop=True)

st.sidebar.table(user["Recipe"])


def get_recommendations(name, cosine_sim, raw):
    
    idx = indices[name]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]


    food_indices = [i[0] for i in sim_scores]

    recommend = pd.DataFrame(df['Name'].iloc[food_indices]).reset_index(drop=True)
    d = pd.merge(recommend, raw, on=None, left_on="Name", right_on="Name", how="left")
    return d.drop(columns=["Description","Ingredients","Preparation"])
    




def user(user_name, cosine_sim, raw):

    user_info = reviews[(reviews["User_Name"] == user_name) & (reviews["Polarity"] == "Positive")]
    
    if len(user_info) >= 1 :
        food = (user_info.sample(1)).iloc[0,1]
        return(get_recommendations(food, cosine_sim, raw))
    else:
        food = (df.sample(1)).iloc[0,1]
        return(get_recommendations(food, cosine_sim, raw))


recommended = user(name, cosine_sim, raw)
recommended.sort_values("Rating", ascending=False, inplace=True)
recommended = recommended.reset_index(drop=True)

recom = recommended.sort_values("Rating", ascending=False)

    
fig = px.bar(recom, x='Name', y='Rating', color='Name',color_discrete_sequence=px.colors.diverging.Geyser, height=600, width=900)
    
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
    
    
fig.update_layout(template="plotly_white",xaxis_showgrid=False, yaxis_showgrid=False)
    
fig.update_traces( marker_line_color='rgb(8,48,107)',
                  marker_line_width=2, opacity=0.6)
    
fig.update_layout(showlegend=False, title="Rating",
xaxis_title="Recommended Recipes",
yaxis_title="Rate")

    
fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
                               
st.table(recommended)

st.plotly_chart(fig)








                               
