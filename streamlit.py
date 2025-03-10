# Import python packages
import streamlit as st
import requests

# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col



cnx = st.connection("snowflake")
session = cnx.session()
# Write directly to the app
st.title("My Smoothie App :cup_with_straw:")
st.write(
    """ choose the fruits you want in your custom Smoothie!
    """
)


title = st.text_input('Name on Smoothie: ')
st.write("The name on your smoothie will be: ", title)
name_on_order = title


# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    , max_selections = 5
)


if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + '  '
        
    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +  """', '""" + name_on_order +"""')"""


    st.write(my_insert_stmt)

    time_to_insert = st.button("submit Order")
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    # fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width= True)
    # st.text(fv_df)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + str(title), icon="✅")



