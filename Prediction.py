import streamlit as st
import pandas as pd
import joblib
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

def fit_label_encoders(data, columns):
    encoders = {}
    for column in columns:
        le = LabelEncoder()
        le.fit(data[column])
        encoders[column] = le
    return encoders

def predict(li_small):
    st.title("Money Laundering: Prediction")

    # Load the model
    model = joblib.load('Notebook/XGBoost_model.joblib')
    
    # Fit label encoders on the dataset
    label_encoders = fit_label_encoders(li_small, ['Receiving Currency', 'Payment Currency', 'Payment Format'])

    # Transform unique values back to original categorical values
    original_receiving_currency = sorted(li_small["Receiving Currency"].unique())
    original_payment_currency = sorted(li_small["Payment Currency"].unique())
    original_payment_format = sorted(li_small["Payment Format"].unique())

    # Form for user input
    with st.form(key='Prediction_form'):
        timestamp = st.text_input('Timestamp', value='', help='Format: YYYY-MM-DD HH:MM')
        from_bank = st.text_input('From Bank', value='', help='Numeric code of the bank from which the transaction originated')
        account = st.text_input('From Account', value='', help='Hexadecimal code of the account from which the transaction originated')
        to_bank = st.text_input('To Bank', value='', help='Numeric code of the bank where the transaction was closed')
        account_1 = st.text_input('To Account', value='', help='Hexadecimal code of the account from which the transaction originated End of Action')
        amount_received = st.text_input('Amount Received', value='', help='Amount of currency received from the recipient account')
        receiving_currency = st.selectbox('Receiving Currency', options=original_receiving_currency)
        amount_paid = st.text_input('Amount Paid', value='', help='The amount in the currency in which the payment was made')
        payment_currency = st.selectbox('Payment Currency', options=original_payment_currency)
        payment_format = st.selectbox('Payment Format', options=original_payment_format)

        # Convert inputs to appropriate data types
        try:
            timestamp = pd.to_datetime(timestamp)
            from_bank = int(from_bank)
            account = int(account, 16)
            to_bank = int(to_bank)
            account_1 = int(account_1, 16)  # Convert hexadecimal string to integer
            amount_received = float(amount_received)
            amount_paid = float(amount_paid)
        except ValueError:
            st.error("Error: Please enter valid values for the inputs.")
        
        submit_button = st.form_submit_button(label='Predict')
    
    # Perform prediction when form is submitted
    if submit_button:
        # Encode categorical variables using fitted label encoders
        receiving_currency_encoded = label_encoders['Receiving Currency'].transform([receiving_currency])[0]
        payment_currency_encoded = label_encoders['Payment Currency'].transform([payment_currency])[0]
        payment_format_encoded = label_encoders['Payment Format'].transform([payment_format])[0]
        
        # Prepare input features for prediction
        X = pd.DataFrame({
            'Timestamp': [timestamp],
            'From Bank': [from_bank],
            'Account': [account],
            'To Bank': [to_bank],
            'Account.1': [account_1],
            'Amount Received': [amount_received],
            'Receiving Currency': [receiving_currency_encoded],
            'Amount Paid': [amount_paid],
            'Payment Currency': [payment_currency_encoded],
            'Payment Format': [payment_format_encoded]
        })

        # Convert Timestamp to numerical format (e.g., Unix timestamp)
        X['Timestamp'] = X['Timestamp'].astype('int64') // 10**9

        # Convert DataFrame to DMatrix with enable_categorical parameter
        dmatrix = xgb.DMatrix(X, enable_categorical=True)

        # Make prediction
        y_pred = model.predict(dmatrix)

        # Display prediction result
        if y_pred[0] == 1:
            st.write("**Suspect Laundering**")
        else:
            st.write("**Low Possibility of Laundering**")