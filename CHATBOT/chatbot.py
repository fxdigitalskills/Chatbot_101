# Set page config and theme
st.set_page_config(
    page_title="Malaysian Price Analysis",
    page_icon="🛒",
    layout="wide"
)

# Title and description
st.title("Malaysian Price Analysis Dashboard")
st.write("Analysis of essential goods prices from DOSM Price Catcher data")

# Load data
@st.cache_data  # This caches the data to improve performance
def load_data():
    # Replace these paths with your actual CSV file paths
    df_2022 = pd.read_csv('price_catcher_2022.csv')
    df_2023 = pd.read_csv('price_catcher_2023.csv')
    return df_2022, df_2023

try:
    df_2022, df_2023 = load_data()
    
    # Create comparison dataframe
    # Assuming your CSVs have 'Item' and 'Price' columns
    comparison_data = {
        'Items': ['Eggs', 'Rice', 'Cooking Oil', 'Chicken'],  # Add your items
        'Price_2022': df_2022.groupby('Item')['Price'].mean(),  # Adjust column names
        'Price_2023': df_2023.groupby('Item')['Price'].mean()  # Adjust column names
    }
    comparison_df = pd.DataFrame(comparison_data)

    # Create bar chart
    fig = px.bar(comparison_df, 
                 x='Items',
                 y=['Price_2022', 'Price_2023'],
                 title='Price Comparison 2022 vs 2023',
                 labels={'value': 'Price (RM)', 'variable': 'Year'},
                 barmode='group',
                 range_y=[0, 25])  # Adjust y-axis range as needed

    # Customize layout
    fig.update_layout(
        xaxis_title="Items",
        yaxis_title="Price (RM)",
        yaxis_tickformat='RM %.2f'
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Please ensure your CSV files are in the correct format and location")
