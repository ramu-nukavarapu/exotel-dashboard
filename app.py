import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📞 Exotel Status Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Check required columns
    if {"Status", "ToName"}.issubset(df.columns):
        # Count overall status
        status_counts = df["Status"].value_counts()
        col1, col2 = st.columns(2)
        total_count = status_counts['completed']+status_counts['missed-call']+status_counts['call-attempt']
        col1.metric("Total Calls Received", f"{total_count}")
        col2.metric("Number of Calls Completed: ", f"{status_counts['completed']}")
        col2.metric("Number of Calls Missed: ", f"{status_counts['missed-call']}")
        col2.metric("Number of Calls Attempted: ", f"{status_counts['call-attempt']}")
        st.subheader("📊 Overall Call Status Distribution")
        st.bar_chart(status_counts)

        st.subheader("Call Status Pie Chart")
        fig, ax = plt.subplots()
        ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        # Leaderboards
        st.subheader("🏆 Completed Calls Leaderboard")
        completed_leaderboard = (
            df[df["Status"] == "completed"]
            .groupby("ToName")
            .size()
            .sort_values(ascending=False)
            .reset_index(name="Completed Calls")
        )
        st.dataframe(completed_leaderboard)

        st.subheader("📉 Missed Calls Leaderboard")
        missed_leaderboard = (
            df[df["Status"] == "missed-call"]
            .groupby("ToName")
            .size()
            .sort_values(ascending=False)
            .reset_index(name="Missed Calls")
        )
        st.dataframe(missed_leaderboard)

    else:
        st.error("The uploaded file must contain 'status' and 'ToName' columns.")
