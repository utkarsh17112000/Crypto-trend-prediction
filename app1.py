import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
from datetime import datetime
from bs4 import BeautifulSoup
import requests

start='2019-01-01'
end=datetime.now()



st.title('CRYPTO TREND PREDICTION')

user_input=st.text_input('Enter Crypto ','BTC-USD')
df=data.DataReader(user_input,'yahoo',start,end)

# Describing data
st.subheader('Data Till Date')
st.write(df.describe())

st.subheader('Data Of Last 2 Days')
st.write(df.tail(2))


#Display a chart
st.bar_chart(df.Close)
#visualization

st.subheader('Prices vs Time Chart')
fig=plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)



st.subheader('Prices vs Time Chart With 100MA')
ma100=df.Close.rolling(100).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Prices vs Time Chart With 200MA')
ma200=df.Close.rolling(200).mean()
ma100=df.Close.rolling(100).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100,'r')
plt.plot(ma200,'g')
plt.plot(df.Close,'b')
st.pyplot(fig)


data_training=pd.DataFrame(df['Close'][0:int(len(df)*.70)])
data_testing=pd.DataFrame(df['Close'][int(len(df)*.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler= MinMaxScaler(feature_range=(0,1))

data_training_array=scaler.fit_transform(data_training)



# Load the model
model=load_model('keras_model12.h5')

# Testing Part
past_100_days=data_training.tail(100)

final_df=past_100_days.append(data_testing , ignore_index=True)

input_data=scaler.fit_transform(final_df)



# Test
x_test=[]
y_test=[]

for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])

x_test , y_test=np.array(x_test) , np.array(y_test)

y_predicted=model.predict(x_test)

scaler=scaler.scale_

scale_factor=1/scaler[0]
y_predicted=y_predicted*scale_factor
y_test=y_test*scale_factor



# Final Graph
st.subheader('Predictions vs Original')

fig2=plt.figure(figsize=(12,6))
plt.plot(y_test,'b',label='Original ')
plt.plot(y_predicted,'r',label='Predicted ')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

# user_input = st.text_input("Add your RSS link here!", "https://economictimes.indiatimes.com/markets/cryptocurrency/rssfeeds/82519373.cms")

user_input = st.text_input("Add your RSS link here!", "https://Blockchain.News/RSS/")

def extract_text_from_rss(rss_link):
    """
    Parses the XML and extracts the headings from the 
    links in a python list.
    """
    headings = []
    
    r2 = requests.get(rss_link)
    
    soup2 = BeautifulSoup(r2.content, features='lxml')
    
    headings2 = (soup2.findAll('title'))
    print(headings2)
    headings = headings2
    return headings
fin_headings = extract_text_from_rss(user_input)
with st.expander("Expand for Crypto News!"):
    for h in fin_headings:
        st.markdown("* " + h.text)