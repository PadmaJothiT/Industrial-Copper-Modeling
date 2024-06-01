import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix,accuracy_score


st.set_page_config(page_title= "Copper Modelling",
                   page_icon= 'random',
                   layout= "wide",)

st.markdown("<h1 style='text-align: center; color: purple;'>WELCOME TO INDUSTRIAL COPPER MODELLING</h1>",unsafe_allow_html=True)

selected = option_menu(None, ["PRICE PREDICTION","STATUS PREDICTION"],
            icons=['cash-coin','trophy',"check-circle"],orientation='horizontal',default_index=0)


# Price Prediction

if selected=='PRICE PREDICTION':
    try:
        if 'PRICE PREDICTION':
            item_list=['W', 'S', 'Others', 'PL', 'WI', 'IPL']
            status_list=['Won', 'To be approved', 'Lost', 'Not lost for AM', 'Wonderful', 'Revised','Offered', 'Offerable']
            country_list=['28', '32', '38', '78', '27', '30', '25', '77', '39', '40', '26', '84', '80', '79','113', '89']
            application_list=[10, 41, 28, 59, 15, 4, 38, 56, 42, 26, 27, 19, 20, 66,
                                29, 22, 40, 25, 67, 79, 3, 99, 2, 5,39, 69, 70, 65, 58, 68]

            product_list=[1670798778, 1668701718, 628377, 640665, 611993, 1668701376,
                            164141591, 1671863738, 1332077137,     640405, 1693867550, 1665572374,
                            1282007633, 1668701698, 628117, 1690738206, 628112, 640400,
                            1671876026, 164336407, 164337175, 1668701725, 1665572032, 611728,
                            1721130331, 1693867563, 611733, 1690738219, 1722207579, 929423819,
                            1665584320, 1665584662, 1665584642]
            st.write(
                    '##### ***<span style="color:black">Fill all the fields and Press the below button to view the :red[Pedicted price]   of copper</span>***',
                    unsafe_allow_html=True)

            c1,c2,c3=st.columns([2,2,2])
            with c1:
                quantity=st.text_input('**Enter Quantity  (Min:611728 & Max:1722207579) in tons**')
                thickness = st.text_input('**Enter Thickness (Min:0.18 & Max:400)**')
                width = st.text_input('**Enter Width  (Min:1 & Max:2990)**')


            with c2:
                country = st.selectbox('**Country Code**', country_list)
                status = st.selectbox('**Status**', status_list)
                item = st.selectbox('**Item Type**', item_list)

            with c3:
                application = st.selectbox('**Application Type**', application_list)
                product = st.selectbox('**Product Reference**', product_list)
                item_order_date = st.date_input("**Order Date**", datetime.date(2020, 7, 20))
                item_delivery_date = st.date_input("**Estimated Delivery Date**", datetime.date(2021, 12, 1))
            with c1:
                st.write('')
                st.write('')
                st.write('')
                if st.button('PREDICT PRICE'):
                    data = []
                    with open('status.pkl', 'rb') as file:
                        encode_status = pickle.load(file)
                    with open('item type.pkl', 'rb') as file:
                        encode_item = pickle.load(file)
                    with open('scaling.pkl', 'rb') as file:
                        scaled_data = pickle.load(file)
                    with open('ExtraTreeRegressor.pkl', 'rb') as f:
                        model = pickle.load(f)
  

                    transformed_status = encode_status.transform(status_list)
                    encode_st = None
                    for i, j in zip(status_list, transformed_status):
                        if status == i:
                            encode_st = j
                            break
                    else:
                        st.error("Status not found.")
                        exit()


                    encode=OrdinalEncoder()
                    encode_item=encode.fit(item_list)

                    transformed_item = encode_item.transform(item_list)
                    encode_it = None
                    for i, j in zip(item_list, transformed_item):
                        if item == i:
                            encode_it = j
                            break
                    else:
                        st.error("Item type not found.")
                        exit()



                    order = datetime.datetime.strptime(str(item_order_date), "%Y-%m-%d")
                    delivery = datetime.datetime.strptime(str(item_delivery_date), "%Y-%m-%d")
                    day = delivery - order


                    data.append(quantity)
                    data.append(thickness)
                    data.append(width)
                    data.append(country)
                    data.append(encode_st)
                    data.append(encode_it)
                    data.append(application)
                    data.append(product)
                    data.append(day.days)

                    x = np.array(data).reshape(1, -1)
                    pred_model= scaled_data.transform(x)
                    price_predict= model.predict(pred_model)
                    predicted_price = str(price_predict)[1:-1]

                    st.success(f'**Predicted Selling Price : :green[₹] :green[{predicted_price}]**')
    
    except:
        st.error('Please enter values in empty cells')

#  Status Prediction

if selected=='STATUS PREDICTION':
    try:
        if 'STATUS PREDICTION':
            item_list_cls = ['W', 'S', 'Others', 'PL', 'WI', 'IPL']
            country_list_cls = ['28', '32', '38', '78', '27', '30', '25', '77', '39', '40', '26', '84', '80', '79', '113', '89']
            application_list_cls = [10, 41, 28, 59, 15, 4, 38, 56, 42, 26, 27, 19, 20, 66,
                                    29, 22, 40, 25, 67, 79, 3, 99, 2, 5, 39, 69, 70, 65, 58, 68]
            product_list_cls = [1670798778, 1668701718, 628377, 640665, 611993, 1668701376,
                                    164141591, 1671863738, 1332077137, 640405, 1693867550, 1665572374,
                                    1282007633, 1668701698, 628117, 1690738206, 628112, 640400,
                                    1671876026, 164336407, 164337175, 1668701725, 1665572032, 611728,
                                    1721130331, 1693867563, 611733, 1690738219, 1722207579, 929423819,
                                    1665584320, 1665584662, 1665584642]

            st.write('##### ***<span style="color:GREEN">Fill all the fields and Press the below button to view the status :violet[WON] / :red[LOST] of copper in the desired time range</span>***',
                        unsafe_allow_html=True)

            cc1, cc2, cc3 = st.columns([2,2,2])
            with cc1:
                quantity_cls = st.text_input('ENTER QUANTITY  (Min:611728 & Max:1722207579) in tons')
                thickness_cls = st.text_input('ENTER THICKNESS (Min:0.18 & Max:400)')
                width_cls= st.text_input('ENTER WIDTH  (Min:1 & Max:2990)')

            with cc2:
                selling_price_cls= st.text_input('ENTER SELLING PRICE  (Min:1, Max:100001015)')
                item_cls = st.selectbox('ITEM TYPE', item_list_cls)
                country_cls= st.selectbox('COUNTRY CODE', country_list_cls)

            with cc3:
                application_cls = st.selectbox('APLLICATION TYPE', application_list_cls)
                product_cls = st.selectbox('PRODUCT REFERENCE', product_list_cls)
                item_order_date_cls = st.date_input("ORDER DATE", datetime.date(2020, 7, 20))
                item_delivery_date_cls = st.date_input("ESTIMATED DELIVERY DATE", datetime.date(2022,12, 1))

            with cc1:
                st.write('')
                st.write('')
                st.write('')
                if st.button('PREDICT STATUS'):
                    data_cls = []
                    with open('item type.pkl', 'rb') as file:
                        encode_item_cls = pickle.load(file)
                    with open('scaling_classify.pkl', 'rb') as file:
                        scaled_data_cls = pickle.load(file)
                    with open('RandomForestClassification.pkl', 'rb') as file:
                        trained_model_cls = pickle.load(file)

                    encode=OrdinalEncoder()
                    encode_item_cls=encode.fit(item_list_cls)      

                    transformed_item_cls = encode_item_cls.transform(item_list_cls)
                    encode_it_cls = None
                    for i, j in zip(item_list_cls, transformed_item_cls):
                        if item_cls == i:
                            encode_it_cls = j
                            break
                    else:
                        st.error("Item type not found.")
                        exit()

                    order_cls = datetime.datetime.strptime(str(item_order_date_cls), "%Y-%m-%d")
                    delivery_cls = datetime.datetime.strptime(str(item_delivery_date_cls), "%Y-%m-%d")
                    day_cls = delivery_cls- order_cls

                    data_cls.append(quantity_cls)
                    data_cls.append(thickness_cls)
                    data_cls.append(width_cls)
                    data_cls.append(selling_price_cls)
                    data_cls.append(country_cls)
                    data_cls.append(encode_it_cls)
                    data_cls.append(application_cls)
                    data_cls.append(product_cls)
                    data_cls.append(day_cls.days)

        

                    x_cls = np.array(data_cls).reshape(1, -1)  
                    scaling_model_cls = scaled_data_cls.transform(x_cls)
                    pred_status = trained_model_cls.predict(scaling_model_cls)
                    if pred_status==6:
                        st.success(f'**Predicted Status : :green[WON]**')
                    else:
                        st.error(f'**Predicted Status : :blue[LOST]**')
            
    except:
        st.error("Please enter values in empty cells")
