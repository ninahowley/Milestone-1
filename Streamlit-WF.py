import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import requests

mealDict = {"Bates":{"Breakfast":145,"Lunch":146,"Dinner":311,"LocationID":95},"Lulu":{"Breakfast":148,"Lunch":149,"Dinner":312,"LocationID":96},"Tower":{"Breakfast":153,"Lunch":154,"Dinner":310,"LocationID":97},"StoneD":{"Breakfast":261,"Lunch":262,"Dinner":263,"LocationID":131}}

def getMenu(locationID, mealID, date):
    base_url = "https://dish.avifoodsystems.com/api/menu-items/week"
    params = {"date":d,"locationID":locationID,"mealID":mealID}
    response = requests.get(base_url,params=params)
    data = response.json()

    df = pd.DataFrame(data)
    df['date'] = df['date'].apply(lambda x: x.strip("T00:00:00"))
    df = df[df['date']== str(date)]
    df2 = pd.DataFrame({"name":df["name"],"station":df["categoryName"],"description":df["description"]}, )
    st.dataframe(df2, hide_index=True)
    return df2

st.set_page_config(page_title="WF Streamlit", layout="wide")

st.header("Milestone 1")
st.subheader(f"Today: {date.today()}")

location = st.selectbox(
    "Pick a location!",
    ("Bates", "Lulu", "Tower", "StoneD"),
)

meal = st.selectbox(
    "Pick a meal!",
    ("Breakfast", "Lunch", "Dinner")
)

mealID = mealDict[location][meal]
locationID = mealDict[location]["LocationID"]
today = date.today().weekday()
d = date.today()


__, col2, __ = st.columns((0.5, 1, 0.5), gap = "small", vertical_alignment="center")
with col2:
    values = [6, 0, 1, 2, 3, 4, 5] #our week starts on Sunday (6)
    labels = ['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']   
    selection = st.select_slider('Choose a range',values, value=today, format_func=(lambda x:labels[x]))

if( selection == 6):
    selection = -1
d = d + timedelta(days=selection - today)
st.write("Selected Date: ", d)

menu_shown = st.toggle("Show menu")
if (menu_shown):
    getMenu(locationID,mealID, d)
