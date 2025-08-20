import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Streamlit app structure
st.title("Self Service Reporting App")
st.write("""
Welcome to the Self Service Reporting App!

Here's how to use it:
1.  **Upload your data file:** Use the file uploader in the sidebar to upload your data in CSV or Excel format.
2.  **View Data Preview:** Once uploaded, you will see a preview of your data below.
3.  **Select Visualization:** Choose a visualization type from the dropdown in the sidebar.
4.  **Select Columns:** Select the columns you want to use for the visualization.
5.  **Customize Visualization (Optional):** Add a title, axis labels, or choose colors for your plot.
6.  **View Visualization:** The generated plot will appear below the data preview.
7.  **Export Data:** You can download the processed data as a CSV file using the button at the bottom.
""")
st.sidebar.header("User Inputs")

# Data upload logic
uploaded_file = st.sidebar.file_uploader("Upload your data file", type=['csv', 'xlsx'])

# Data display logic
df = None # Initialize df
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        st.write("Data Preview:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload a data file to get started.")

# Visualization options and generation logic
if df is not None:
    st.subheader("Data Visualization")
    visualization_type = st.sidebar.selectbox(
        "Select Visualization Type",
        ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Histogram']
    )

    # Add customization options
    st.sidebar.subheader("Visualization Options")
    plot_title = st.sidebar.text_input("Enter plot title", "")
    x_axis_label = st.sidebar.text_input("Enter x-axis label", "")
    y_axis_label = st.sidebar.text_input("Enter y-axis label", "")
    # Basic color option (can be expanded)
    color = st.sidebar.color_picker("Select plot color", "#1f77b4")


    try:
        if visualization_type == 'Bar Chart':
            categorical_col = st.selectbox("Select categorical column for x-axis", df.columns)
            numerical_col = st.selectbox("Select numerical column for y-axis", df.columns)
            if categorical_col and numerical_col:
                if pd.api.types.is_numeric_dtype(df[numerical_col]):
                    fig, ax = plt.subplots()
                    sns.barplot(x=categorical_col, y=numerical_col, data=df, ax=ax, color=color)
                    ax.set_title(plot_title)
                    ax.set_xlabel(x_axis_label if x_axis_label else categorical_col)
                    ax.set_ylabel(y_axis_label if y_axis_label else numerical_col)
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning(f"Column '{numerical_col}' is not numerical and cannot be used for the y-axis in a Bar Chart. Please select a numerical column.")

        elif visualization_type == 'Line Chart':
            x_col = st.selectbox("Select column for x-axis", df.columns)
            y_col = st.selectbox("Select numerical column for y-axis", df.columns)
            if x_col and y_col:
                 if pd.api.types.is_numeric_dtype(df[y_col]):
                    fig, ax = plt.subplots()
                    sns.lineplot(x=x_col, y=y_col, data=df, ax=ax, color=color)
                    ax.set_title(plot_title)
                    ax.set_xlabel(x_axis_label if x_axis_label else x_col)
                    ax.set_ylabel(y_axis_label if y_axis_label else y_col)
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
                    plt.close(fig)
                 else:
                    st.warning(f"Column '{y_col}' is not numerical and cannot be used for the y-axis in a Line Chart. Please select a numerical column.")

        elif visualization_type == 'Scatter Plot':
            x_col = st.selectbox("Select column for x-axis", df.columns)
            y_col = st.selectbox("Select column for y-axis", df.columns)
            if x_col and y_col:
                fig, ax = plt.subplots()
                sns.scatterplot(x=x_col, y=y_col, data=df, ax=ax, color=color)
                ax.set_title(plot_title)
                ax.set_xlabel(x_axis_label if x_axis_label else x_col)
                ax.set_ylabel(y_axis_label if y_axis_label else y_col)
                plt.xticks(rotation=45, ha='right')
                st.pyplot(fig)
                plt.close(fig)

        elif visualization_type == 'Histogram':
            numerical_col = st.selectbox("Select numerical column", df.columns)
            if numerical_col:
                if pd.api.types.is_numeric_dtype(df[numerical_col]):
                    fig, ax = plt.subplots()
                    sns.histplot(data=df, x=numerical_col, ax=ax, color=color)
                    ax.set_title(plot_title)
                    ax.set_xlabel(x_axis_label if x_axis_label else numerical_col)
                    ax.set_ylabel(y_axis_label if y_axis_label else "Frequency")
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning(f"Column '{numerical_col}' is not numerical and cannot be used for a Histogram. Please select a numerical column.")

    except Exception as e:
        st.error(f"An error occurred during visualization generation: {e}")

# Data export logic
if df is not None:
    st.subheader("Export Data")
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv_data,
        file_name='exported_data.csv',
        mime='text/csv',
    )
