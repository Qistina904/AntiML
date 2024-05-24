import streamlit as st # deployment

def EDA(li_small, hi_small):
    # Import libraries
    import numpy as np # numeric
    import pandas as pd # read data
    import matplotlib.pyplot as plt # data visualization
    import seaborn as sns # data visualization
    # Page Title
    st.title('Money Laundering: Analyzing and Detecting in IBM Transactions')
    st.subheader('**What is _Money Laundering_?**', divider='grey')

    st.markdown("""
    Money laundering is the process of making illegally obtained money appear legal by disguising its true source. 
    It typically involves three steps: 
    1. Placing the money into the financial system.
    2. Layering it through multiple transactions to obscure its origin.
    3. Integrating it into the economy as legitimate funds.
    """)

    st.image('Notebook/jason-leung-SAYzxuS1O3M-unsplash.jpg', caption='Money Backgrounds by Jason Leung')

    st.markdown("""
    **Anti-money laundering (AML)** measures are crucial to protect the financial system's integrity, prevent criminal activity, and ensure compliance with regulatory standards. \n
    This app performs analysis of IBM Transactions for Anti Money Laundering (AML) data
    * **Data set:**  LI-Small_trans and HI-Small_trans
    * **Data source:** [www.kaggle.com](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml/)
    """)
    
    # Payment Currency
    st.sidebar.header('Features for EDA')
    sorted_payment_currency = sorted(li_small["Payment Currency"].unique())
    selected_currency = st.sidebar.multiselect('Currency', sorted_payment_currency, sorted_payment_currency)
    
    li_small = li_small[li_small["Payment Currency"].isin(selected_currency)]
    hi_small = hi_small[hi_small["Payment Currency"].isin(selected_currency)]
    
    # Calculate counts and percentages for 'Is Laundering' in both datasets
    li_laundering_counts = li_small['Is Laundering'].value_counts()
    hi_laundering_counts = hi_small['Is Laundering'].value_counts()
    
    li_laundering_percentages = (li_small['Is Laundering'].value_counts(normalize=True) * 100).round(2)
    hi_laundering_percentages = (hi_small['Is Laundering'].value_counts(normalize=True) * 100).round(2)
    
    # Create a grouped bar chart
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x = np.arange(2)  # Two categories: 'Laundering' and 'No Laundering'
    width = 0.35  # Width of the bars
    
    # Create the bar plots
    bars1 = ax.bar(x - width / 2, [li_laundering_percentages.get(1, 0), li_laundering_percentages.get(0, 0)], width, label='li_small')
    bars2 = ax.bar(x + width / 2, [hi_laundering_percentages.get(1, 0), hi_laundering_percentages.get(0, 0)], width, label='hi_small')
    
    # Set chart labels and legend
    ax.set_xlabel("Laundering Status")
    ax.set_ylabel("Percentage (%)")
    ax.set_title("Comparison of Money Laundering Percentages")
    ax.set_xticks(x)
    ax.set_xticklabels(["Laundering", "No Laundering"])
    ax.legend()
    
    # Annotate the bars with percentages
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.2f}%", xy=(bar.get_x() + bar.get_width() / 2, height), ha='center', va='bottom')
    
    # Display the bar chart in Streamlit
    st.subheader("Dataset Description", divider='grey')
    st.write('Data Dimension(li_small): ' + str(li_small.shape[0]) + ' rows and ' + str(li_small.shape[1]) + ' columns.')
    st.write('Data Dimension(hi_small): ' + str(hi_small.shape[0]) + ' rows and ' + str(hi_small.shape[1]) + ' columns.')
    st.markdown("""
    * There are two independent datasets, and both datasets have the same _**11 features**_. \n
    * These features include: _Timestamp_, _Bank Name_, _Bank Account_, _Currency_, _Laundering Label_, and others.
    """)
    st.pyplot(fig)
    
    # Create a summary DataFrame
    laundering_summary = pd.DataFrame({
        "li_small - Percentage": li_laundering_percentages,
        "hi_small - Percentage": hi_laundering_percentages
    })
    
    # Display the summary DataFrame in Streamlit
    st.write("Laundering Summary:")
    st.dataframe(laundering_summary)
    st.markdown("""
    From the summary, we conclude that the li_small dataset contains 0.05% laundering transactions, while the hi_small dataset contains 0.1% laundering transactions.
    """)
    
    # Filter 'Is Laundering' == 1
    li_small_laundering = li_small[li_small['Is Laundering'] == 1]
    hi_small_laundering = hi_small[hi_small['Is Laundering'] == 1]
    
    # Utility function to create summary tables
    def create_match_summary(dataframe, condition, column_name):
        total_count = len(dataframe)
        match_count = condition.sum()
        no_match_count = total_count - match_count
        match_percentage = round((match_count / total_count) * 100, 2)
        no_match_percentage = round((no_match_count / total_count) * 100, 2)
        
        return {
            "Column": column_name,
            "Total": total_count,
            "Match Percentage": match_percentage,
            "No Match Percentage": no_match_percentage
        }
    
    # Create summary tables for each filtered dataset
    li_small_summary = [
        create_match_summary(li_small_laundering, li_small_laundering["Account"] == li_small_laundering["Account.1"], "Account"),
        create_match_summary(li_small_laundering, li_small_laundering["From Bank"] == li_small_laundering["To Bank"], "Bank"),
        create_match_summary(li_small_laundering, li_small_laundering["Receiving Currency"] == li_small_laundering["Payment Currency"], "Currency"),
        create_match_summary(li_small_laundering, li_small_laundering["Amount Received"] == li_small_laundering["Amount Paid"], "Amount")
    ]
    
    hi_small_summary = [
        create_match_summary(hi_small_laundering, hi_small_laundering["Account"] == hi_small_laundering["Account.1"], "Account"),
        create_match_summary(hi_small_laundering, hi_small_laundering["From Bank"] == hi_small_laundering["To Bank"], "Bank"),
        create_match_summary(hi_small_laundering, hi_small_laundering["Receiving Currency"] == hi_small_laundering["Payment Currency"], "Currency"),
        create_match_summary(hi_small_laundering, hi_small_laundering["Amount Received"] == hi_small_laundering["Amount Paid"], "Amount")
    ]
    
    # Convert to DataFrames
    li_small_summary_df = pd.DataFrame(li_small_summary)
    hi_small_summary_df = pd.DataFrame(hi_small_summary)
    
    # Display in Streamlit
    st.subheader("Unseen patterns that occur in laundering transactions", divider='grey')
    st.markdown("""
    In this step, we match the variables associated with laundering transactions.
    """)
    st.write('li_small_laundering:')
    st.dataframe(li_small_summary_df)
    
    st.write("hi_small_laundering:")
    st.dataframe(hi_small_summary_df)
    
    # Additional explanatory information
    st.markdown("""
    * **Match Account:**  Account == Account.1
    * **Match Bank:**  From Bank == To Bank
    * **Match Currency:**  Receiving Currency == Payment Currency
    * **Match Amount:**  Amount Received == Amount Paid \n
    As the result, currencies and amounts presented the highest percentage of matching on both data sets.
    """)
    
    # Create a subplot with two pie charts
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns
    
    # Pie chart for "Payment Currency" in li_small_laundering
    li_currency_counts = pd.Series(li_small_laundering["Payment Currency"]).value_counts()
    axes[0].pie(li_currency_counts, labels=li_currency_counts.index, autopct='%1.1f%%', startangle=90)
    axes[0].set_title("Payment Currency - li_small_laundering")
    axes[0].axis("equal")  # Ensure the pie chart is a circle
    
    # Pie chart for "Payment Currency" in hi_small_laundering
    hi_currency_counts = pd.Series(hi_small_laundering["Payment Currency"]).value_counts()
    axes[1].pie(hi_currency_counts, labels=hi_currency_counts.index, autopct='%1.1f%%', startangle=90)
    axes[1].set_title("Payment Currency - hi_small_laundering")
    axes[1].axis("equal")  # Ensure the pie chart is a circle
    
    # Adjust subplot layout for better spacing
    plt.tight_layout()
    
    # Display the pie chart subplot in Streamlit
    st.subheader("Currency vs. Money Laundering Activity", divider='grey')
    st.markdown("""
    Due to currencies and amounts presenting the highest percentage of matching in both datasets, we plot a pie chart to showcase the currency distribution.
    """)
    st.pyplot(fig)  # Display the plot
    st.markdown("""
    **The Top 3 currencies for money laundering activity**
    * **li_small**'s dataset : _**US Dollar**_, _**Euro**_, and the _**Yuan**_, accounting for _**40.8%**_, _**28.8%**_, and _**5.3%**_ respectively. 
    * **hi_small**'s dataset : _**US Dollar**_, _**Euro**_, and _**Saudi Riyal**_, accounting for _**36.9%**_, _**26.5%**_, and _**7.2%**_ respectively. 
    """)
    
    # Extract day from Timestamp and calculate the number of transactions by day
    li_small_laundering['Timestamp'] = pd.to_datetime(li_small_laundering['Timestamp'])
    hi_small_laundering['Timestamp'] = pd.to_datetime(hi_small_laundering['Timestamp'])
    
    li_small_laundering['Day'] = li_small_laundering['Timestamp'].dt.day
    hi_small_laundering['Day'] = hi_small_laundering['Timestamp'].dt.day
    
    li_small_laundering_by_day = li_small_laundering.groupby('Day').size()
    hi_small_laundering_by_day = hi_small_laundering.groupby('Day').size()
    
    # Calculate the mean for each dataset
    li_average = li_small_laundering_by_day.mean()
    hi_average = hi_small_laundering_by_day.mean()
    
    # Create line graphs with averages
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the lines for transaction counts by day
    ax.plot(li_small_laundering_by_day.index, li_small_laundering_by_day, 'b-o', label='li_small_laundering')
    ax.plot(hi_small_laundering_by_day.index, hi_small_laundering_by_day, 'r-o', label='hi_small_laundering')
    
    # Draw horizontal lines for the average
    ax.axhline(y=li_average, color='blue', linestyle='--', label=f'li_small_laundering mean: {li_average:.2f}')
    ax.axhline(y=hi_average, color='red', linestyle='--', label=f'hi_small_laundering mean: {hi_average:.2f}')
    
    # Set titles, labels, and legend
    ax.set_title("Number of Money Laundering Transactions by Day")
    ax.set_xlabel("Day")
    ax.set_ylabel("Number of Transactions")
    ax.grid(True)
    ax.legend()  # Display the legend to distinguish between the lines and average lines
    
    # Display the line graph in Streamlit
    st.subheader("Pattern of Laundering Transactions by Day", divider='grey')
    st.markdown("""
    We then observe the pattern of laundering transactions by day using a line graph.
    """)
    st.pyplot(fig)  # Display the plot
    st.markdown("""
    From the graph, laundering activity **most likely to happens from Day 1 to Day 10** for both data sets, above its own average. 
    """)