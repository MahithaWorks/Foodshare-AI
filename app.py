import streamlit as st
import pandas as pd

from agents import (
    run_foodshare_agents,
    analyze_food_image
)

from database import (
    create_database,
    add_donation,
    get_donations
)


# ============================================================
# DATABASE
# ============================================================

create_database()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FoodShare AI",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🍱 FoodShare AI")

    st.caption(
        "Smart Surplus Food Donation System"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Report Surplus Food",
            "📊 Donation Dashboard"
        ]
    )

    st.divider()

    st.markdown("### How it works")

    st.markdown("""
    **1. 🍱 Report Food**

    Enter surplus food details.

    **2. 👁️ AI Analysis**

    Upload an image for AI analysis.

    **3. 🎯 Priority**

    Determine donation priority.

    **4. 🤝 Matching**

    Find a suitable recipient.

    **5. 📢 Action**

    Generate the recommended action.

    **6. 📊 Tracking**

    Monitor donations through the dashboard.
    """)

    st.divider()

    st.caption("FoodShare AI")
    st.caption("College Project Prototype")


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🍱 FoodShare AI")

st.subheader(
    "AI-Based Surplus Food Donation & Recipient Matching System"
)

st.write(
    "Reduce food wastage by analyzing surplus food, "
    "prioritizing donations and recommending suitable recipients."
)

st.divider()


# ============================================================
# PAGE 1 — REPORT FOOD
# ============================================================

if page == "🏠 Report Surplus Food":

    st.header("📋 Report Surplus Food")

    st.write(
        "Enter the details of surplus food or upload a food image "
        "for AI-powered analysis."
    )

    st.write("")


    # ========================================================
    # INPUT AREA
    # ========================================================

    image_col, details_col = st.columns(
        [1, 1],
        gap="large"
    )


    # ========================================================
    # IMAGE
    # ========================================================

    with image_col:

        st.subheader("📷 Food Image")

        uploaded_image = st.file_uploader(
            "Upload a food image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the surplus food."
        )

        if uploaded_image:

            st.image(
                uploaded_image,
                caption="Uploaded Food",
                use_container_width=True
            )

            st.success(
                "Image uploaded successfully."
            )


    # ========================================================
    # FOOD DETAILS
    # ========================================================

    with details_col:

        st.subheader("🍛 Food Details")

        food_name = st.text_input(
            "Food Name",
            placeholder="Example: Vegetable Biryani"
        )

        quantity = st.number_input(
            "Quantity / Packets",
            min_value=1,
            max_value=10000,
            value=10
        )

        location = st.text_input(
            "Location",
            placeholder="Example: College Campus"
        )

        hours_old = st.number_input(
            "Hours Since Cooked",
            min_value=0,
            max_value=72,
            value=2
        )


    st.write("")


    # ========================================================
    # BUTTONS
    # ========================================================

    image_button, donation_button = st.columns(2)


    with image_button:

        analyze_image_button = st.button(
            "👁️ Analyze Food Image",
            use_container_width=True
        )


    with donation_button:

        analyze_donation_button = st.button(
            "🤖 Analyze Donation",
            use_container_width=True
        )


    # ========================================================
    # IMAGE ANALYSIS
    # ========================================================

    if analyze_image_button:

        if uploaded_image is None:

            st.warning(
                "📷 Please upload a food image first."
            )

        else:

            with st.spinner(
                "👁️ Vision AI is analyzing the image..."
            ):

                image_result = analyze_food_image(
                    uploaded_image.getvalue()
                )

            st.success(
                "Food image analysis completed!"
            )

            st.divider()

            st.header("👁️ Vision AI Analysis")

            result_col1, result_col2 = st.columns(2)


            with result_col1:

                st.metric(
                    "Detected Food",
                    image_result["food_name"]
                )


            with result_col2:

                st.metric(
                    "Category",
                    image_result["category"]
                )


            st.write("")

            st.info(
                image_result["description"]
            )

            st.caption(
                f"Confidence: {image_result['confidence']}"
            )


    # ========================================================
    # MULTI-AGENT ANALYSIS
    # ========================================================

    if analyze_donation_button:

        if not food_name.strip():

            st.error(
                "🍛 Please enter the food name."
            )

        elif not location.strip():

            st.error(
                "📍 Please enter the location."
            )

        else:

            with st.spinner(
                "🤖 AI agents are analyzing the donation..."
            ):

                result = run_foodshare_agents(
                    food_name,
                    quantity,
                    location,
                    hours_old
                )


            st.success(
                "✅ AI analysis completed!"
            )

            st.divider()


            # =================================================
            # ASSESSMENT
            # =================================================

            st.header("🎯 Donation Assessment")


            assessment1, assessment2, assessment3, assessment4 = (
                st.columns(4)
            )


            with assessment1:

                st.metric(
                    "🍛 Food",
                    food_name
                )


            with assessment2:

                st.metric(
                    "📦 Quantity",
                    quantity
                )


            with assessment3:

                st.metric(
                    "⏱️ Food Age",
                    f"{hours_old} hours"
                )


            with assessment4:

                st.metric(
                    "🎯 Priority",
                    result["priority"]
                )


            st.write("")


            # =================================================
            # PRIORITY MESSAGE
            # =================================================

            if result["priority"] == "HIGH":

                st.error(
                    "🔴 HIGH PRIORITY — Donation should be "
                    "processed promptly."
                )

            elif result["priority"] == "MEDIUM":

                st.warning(
                    "🟡 MEDIUM PRIORITY — Donation should be "
                    "processed soon."
                )

            else:

                st.success(
                    "🟢 LOW PRIORITY — Donation can be scheduled."
                )


            st.divider()


            # =================================================
            # THREE AGENTS
            # =================================================

            st.header("🤖 Multi-Agent AI Analysis")


            agent1, agent2, agent3 = st.columns(3)


            # -------------------------------------------------
            # AGENT 1
            # -------------------------------------------------

            with agent1:

                st.subheader(
                    "🔍 Food Analysis Agent"
                )

                st.write(
                    "Analyzes food details and determines "
                    "donation priority."
                )

                st.info(
                    result["analysis"]
                )


            # -------------------------------------------------
            # AGENT 2
            # -------------------------------------------------

            with agent2:

                st.subheader(
                    "🤝 Recipient Matching Agent"
                )

                st.write(
                    "Identifies a suitable recipient based "
                    "on food, quantity and location."
                )

                st.success(
                    result["recipient"]
                )


            # -------------------------------------------------
            # AGENT 3
            # -------------------------------------------------

            with agent3:

                st.subheader(
                    "📢 Action Agent"
                )

                st.write(
                    "Generates the recommended next action."
                )

                st.warning(
                    result["action"]
                )


            st.divider()


            # =================================================
            # DONATION SUMMARY
            # =================================================

            st.header("📦 Donation Summary")


            summary1, summary2 = st.columns(2)


            with summary1:

                st.metric(
                    "📍 Location",
                    location
                )


            with summary2:

                st.metric(
                    "🤝 Recommended Recipient",
                    result["recipient"]
                )


            st.write("")


            # =================================================
            # SAVE
            # =================================================

            add_donation(

                food_name,

                quantity,

                location,

                hours_old,

                "Cooked Food",

                result["priority"],

                result["recipient"],

                result["action"],

                "Pending"

            )


            st.success(
                "💾 Donation successfully registered "
                "in the FoodShare database."
            )


# ============================================================
# PAGE 2 — DASHBOARD
# ============================================================

else:

    st.header("📊 Donation Dashboard")

    st.write(
        "Monitor registered food donations and "
        "community distribution activity."
    )

    donations = get_donations()


    # ========================================================
    # EMPTY DATABASE
    # ========================================================

    if not donations:

        st.info(
            "📭 No donations registered yet."
        )

        st.write(
            "Go to **Report Surplus Food** to create "
            "your first donation."
        )


    else:

        columns = [
            "ID",
            "Food",
            "Quantity",
            "Location",
            "Hours Old",
            "Category",
            "Priority",
            "Recipient",
            "Recommendation",
            "Status"
        ]


        df = pd.DataFrame(
            donations,
            columns=columns
        )


        # ====================================================
        # METRICS
        # ====================================================

        total_donations = len(df)

        total_food = int(
            df["Quantity"].sum()
        )

        high_priority = len(
            df[
                df["Priority"] == "HIGH"
            ]
        )

        pending = len(
            df[
                df["Status"] == "Pending"
            ]
        )


        metric1, metric2, metric3, metric4 = st.columns(4)


        with metric1:

            st.metric(
                "📦 Total Donations",
                total_donations
            )


        with metric2:

            st.metric(
                "🍱 Food Units Saved",
                total_food
            )


        with metric3:

            st.metric(
                "🔴 High Priority",
                high_priority
            )


        with metric4:

            st.metric(
                "⏳ Pending",
                pending
            )


        st.divider()


        # ====================================================
        # CHARTS
        # ====================================================

        chart1, chart2 = st.columns(2)


        # PRIORITY CHART

        with chart1:

            st.subheader(
                "🎯 Donations by Priority"
            )

            priority_counts = (

                df["Priority"]

                .value_counts()

                .reindex(
                    [
                        "HIGH",
                        "MEDIUM",
                        "LOW"
                    ],
                    fill_value=0
                )

            )

            st.bar_chart(
                priority_counts
            )


        # FOOD CHART

        with chart2:

            st.subheader(
                "🍱 Food Distribution"
            )

            food_counts = (

                df.groupby(
                    "Food"
                )["Quantity"]

                .sum()

                .sort_values(
                    ascending=False
                )

                .head(10)

            )

            st.bar_chart(
                food_counts
            )


        st.divider()


        # ====================================================
        # DONATION TABLE
        # ====================================================

        st.subheader(
            "📋 Recent Donations"
        )


        display_df = df[
            [
                "ID",
                "Food",
                "Quantity",
                "Location",
                "Priority",
                "Recipient",
                "Status"
            ]
        ]


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        st.write("")


        # ====================================================
        # DOWNLOAD
        # ====================================================

        csv = df.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="⬇️ Download Donation Report",
            data=csv,
            file_name="foodshare_donations.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🍱 FoodShare AI • AI-powered surplus food management "
    "for community food distribution"
)