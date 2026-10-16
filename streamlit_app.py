# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col



# Write directly to the app
st.title(f"CUSTOMIZE YOUR SMOOTHIE HERE! :smiley::cup_with_straw:")
st.write(f"Choose the fruits you want in your favorite custom Smoothie!")


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


name_on_order = st.text_input('Name on SMoothie')
ingredients_list = st.multiselect('Choose up to 5 ingridients', my_dataframe, max_selections=5)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    time_to_insert = st.button('Submit Order')
    st.write(my_insert_stmt)
    
    if time_to_insert:    
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ', icon="✅")

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response.json())
sf_df=st.datafram(data=smoothiefroot_response.json(), use_container_width=True)
