import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError 


#functions
def GetFruitVice(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # Normalize data 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def AddFruit(fruit, my_cnx):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into furit_load_list values ('"+ fruit +"')")
    return "Added " + fruit

def ShowFruitList(my_cnx):
  my_cur = my_cnx.cursor()
  my_cur.execute("select * from fruit_load_List")
  my_data_row = my_cur.fetchall()
  streamlit.text("The fruit load list: ")
  streamlit.dataframe(my_data_row)


#main prgram
streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# Display the table on the page.
streamlit.dataframe(my_fruit_list.loc[fruits_selected])





streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select fruit")
  else:
    streamlit.write('The user entered ', fruit_choice)
    # format into table and row
    streamlit.dataframe(GetFruitVice(fruit_choice))

except URLError as e: 
  streamlit.error()



#streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
add_choice = streamlit.text_input('What fruit would you like to add to this list?')
if streamlit.button("Add fruit"):
  AddFruit(add_choice, my_cnx)

if streamlit.button("show list"):
  ShowFruitList(my_cnx)

if steamlit.button("close connection"):
  my_cnx.close()
  streamlit.text("connection closed")

