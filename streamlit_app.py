# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Order! :cup_with_straw:")
st.write(
  """Orders that need to be filled
  """
)


name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be: ', name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_dataset,(og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID']), [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})])
            
            st.sucess('Orders Updated',icon="👍")
        except:
            st.write('Something went wrong')
else:
    st.success('There are no pending orders right now',icon="👍")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
