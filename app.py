import streamlit as st
import pandas as pd

# ===============================
# App Config
# ===============================
st.set_page_config(page_title="JEE College Predictor", layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>🎓 JEE College Predictor</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>Your Dream College Awaits: "
    " Unlock Your JEE Admission Chances.</p>",
    unsafe_allow_html=True
)

# ===============================
# Load Data
# ===============================
@st.cache_data
def load_data():
    # Placeholder for loading actual data files
    try:
        main_df = pd.read_excel("jee_main_cutoffs.xls")
        adv_df = pd.read_csv("jee_advanced_cutoffs.csv")
    except FileNotFoundError:
        # Create empty DataFrames for demonstration if files are missing
        st.error("Cutoff CSV files (jee_main_cutoffs.csv and jee_advanced_cutoffs.csv) not found. Displaying empty dataframes.")
        cols = ["Institute", "Academic Program Name", "Quota", "Opening Rank", "Closing Rank", "Opening Percentile", "Closing Percentile", "Opening Marks", "Closing Marks", "Seat Type", "Gender", "PWD_Status", "Branch"]
        main_df = pd.DataFrame(columns=cols)
        adv_df = pd.DataFrame(columns=cols)
        
    return main_df, adv_df

jee_main_df, jee_adv_df = load_data()

# ===============================
# Thresholds
# ===============================
TOTAL_CANDIDATES = 1_000_000

# JEE Main
MIN_MAIN_PERCENTILE = 75.0
MIN_MAIN_MARKS = 95
MAX_MAIN_RANK = 400_000

# JEE Advanced
MIN_ADV_PERCENTILE = 97
MIN_ADV_MARKS = 220
MAX_ADV_RANK = 29_247

# ===============================
# Branch Options
# ===============================
BRANCH_OPTIONS = [
    "Any",
    "Computer Science and Engineering",
    "Electronics and Communication Engineering",
    "Mechanical Engineering",
    "Electrical Engineering",
    "Civil Engineering"
]

# ===============================
# Conversion Helpers
# ===============================
def percentile_to_rank(percentile):
    return max(int((100 - percentile) / 100 * TOTAL_CANDIDATES), 1)

def marks_to_percentile(marks):
    # This is a highly generalized and inaccurate model; rank-based is always better
    return (marks / 300) * 100 

# ===============================
# Rank Derivation
# ===============================
def get_main_rank(value, input_type):
    if input_type == "Rank":
        return int(value) if value <= MAX_MAIN_RANK else None
    elif input_type == "Percentile":
        return percentile_to_rank(value) if value >= MIN_MAIN_PERCENTILE else None
    else:
        return percentile_to_rank(marks_to_percentile(value)) if value >= MIN_MAIN_MARKS else None

def get_adv_rank(value, input_type):
    # Note: JEE Advanced Rank conversion is complex and usually requires a fixed mapping table.
    # The current percentile/marks logic is a placeholder and should be treated as highly approximate.
    if input_type == "Rank":
        return int(value) if value <= MAX_ADV_RANK else None
    elif input_type == "Percentile":
        # Approximate: Assume 100-percentile * X = rank (for low ranks)
        return int((100 - value) * 1000) if value >= MIN_ADV_PERCENTILE else None
    else:
        # Approximate: Assume 300-marks * X = rank (for low ranks)
        return int((300 - value) * 100) if value >= MIN_ADV_MARKS else None

# ===============================
# Filters
# ===============================
def apply_filters(df, gender, category, pwd, branch):
    if gender == "Female":
        # Includes Gender-Neutral and Female-Only seats
        df = df[df["Gender"] == "Female"] 
    else:
        # Only Gender-Neutral seats for Male
        df = df[df["Gender"] == "Male"]

    df = df[df["Seat Type"] == category]
    df = df[df["PWD_Status"] == pwd]

    if branch != "Any":
        df = df[df["Branch"] == branch]

    return df

# ===============================
# UI (Centered)
# ===============================
c1, c2, c3 = st.columns(3)

with c2:
    exam_type = st.selectbox("Select Exam", ["JEE Main", "JEE Advanced", "Both"])

    gender = st.selectbox("Gender", ["Male", "Female"])
    category = st.selectbox("Category", ["OPEN", "OBC-NCL", "EWS", "SC", "ST"])
    pwd = st.selectbox("PwD Status", ["No", "Yes"])
    branch = st.selectbox("Preferred Branch", BRANCH_OPTIONS)
    input_type = st.selectbox("Input Type", ["Rank", "Percentile", "Marks"])
    st.info(
        "ℹ️ Rank gives the most accurate prediction. "
        "Percentile and marks are approximate and based on historical trends."
    )


    if exam_type in ["JEE Main", "Both"]:
        main_value = st.number_input(f"JEE Main {input_type}", min_value=1.0, value=15000.0 if input_type=="Rank" else 95.0, key="main_input")

    if exam_type in ["JEE Advanced", "Both"]:
        adv_value = st.number_input(f"JEE Advanced {input_type}", min_value=1.0, value=3000.0 if input_type=="Rank" else 98.1, key="adv_input")

    predict_btn = st.button("🎯 Predict Colleges")

# ===============================
# Prediction
# ===============================
if predict_btn:

    def show_results(df, title, user_rank, user_value):
        # ---- FILTER BASED ON INPUT TYPE ----
        if input_type == "Rank":
            # Rank: User rank must be better (lower) than or equal to closing rank
            df = df[df["Closing Rank"] >= user_rank]
            df = df.sort_values(by=["Opening Rank", "Closing Rank"], ascending=True)

        elif input_type == "Percentile":
            # Percentile: User percentile must be better (higher) than or equal to closing percentile
            df = df[df["Closing Percentile"] <= user_value] 
            df = df.sort_values(by=["Opening Percentile", "Closing Percentile"], ascending=False)

        else:  # Marks
            # Marks: User marks must be better (higher) than or equal to closing marks
            df = df[df["Closing Marks"] <= user_value]
            df = df.sort_values(by=["Opening Marks", "Closing Marks"], ascending=False)

        if df.empty:
            st.warning(f"❌ No reliable predictions available for your criteria in {title}. Please adjust your input or filters.")
            return

        base_cols = ["Institute", "Academic Program Name", "Quota","Institute Type","Gender","Category"]

        if input_type == "Rank":
            cols = base_cols + ["Opening Rank", "Closing Rank"]
        elif input_type == "Percentile":
            cols = base_cols + ["Opening Percentile", "Closing Percentile"]
        else:
            cols = base_cols + ["Opening Marks", "Closing Marks"]

        # Using subheader for the list of colleges
        st.subheader(f"✅ {title} - Eligible Programs")
        st.dataframe(df[cols], use_container_width=True,hide_index=True)

    # -------- JEE MAIN --------
    if exam_type in ["JEE Main", "Both"]:
        main_rank = get_main_rank(main_value, input_type)

        if main_rank is None:
            st.error(
                "❌ JEE Main: Your input falls below the minimum confidence threshold "
                "or exceeds the maximum expected rank. No reliable predictions available."
            )
        else:
            st.header("1️⃣ JEE Main Results (NITs, IIITs, GFTIs)")
            
            main_df = apply_filters(jee_main_df.copy(), gender, category, pwd, branch)
            show_results(
                main_df,
                "JEE Main", # Simple title for show_results
                main_rank,
                main_value
            )

    if exam_type == "Both":
        st.markdown("---") # Clear separator between the two results

    # -------- JEE ADVANCED --------
    if exam_type in ["JEE Advanced", "Both"]:
        adv_rank = get_adv_rank(adv_value, input_type)

        if adv_rank is None:
            st.error(
                "❌ JEE Advanced: Your input falls below the minimum confidence threshold "
                "or exceeds the maximum expected rank. No reliable predictions available."
            )
        else:
            st.header("2️⃣ JEE Advanced Results (IITs)")
            
            adv_df = apply_filters(jee_adv_df.copy(), gender, category, pwd, branch)
            show_results(
                adv_df,
                "JEE Advanced", # Simple title for show_results
                adv_rank,
                adv_value
            )

# ===============================
# Footer
# ===============================
st.markdown(
    """
    ---
    ℹ️ Predictions are based on historical JoSAA cutoffs and do not guarantee admission. 
    The conversions from Percentile/Marks to Rank are highly approximate.
    """
)