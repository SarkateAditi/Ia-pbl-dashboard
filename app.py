import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Telemedicine Market Intelligence", layout="wide", page_icon="🏥")

# ─── DARK THEME CSS ───
st.markdown("""
<style>
    /* Global dark overrides */
    .stApp { background-color: #0E1117; }
    h1, h2, h3, h4, h5, h6 { color: #E2E8F0 !important; }
    .stMarkdown p, .stMarkdown li, .stMarkdown span { color: #CBD5E1; }
    .stMetric label { color: #94A3B8 !important; }
    .stMetric [data-testid="stMetricValue"] { color: #E2E8F0 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] { background-color: #1A1F2B; color: #CBD5E1; border-radius: 6px 6px 0 0; padding: 8px 16px; }
    .stTabs [aria-selected="true"] { background-color: #0D9488 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #1A1F2B; }
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 { color: #E2E8F0 !important; }
    .stDataFrame { border: 1px solid #2D3748; border-radius: 8px; }
    div[data-testid="stExpander"] { background-color: #1A1F2B; border: 1px solid #2D3748; border-radius: 8px; }
    .stAlert { background-color: #1A2332 !important; color: #CBD5E1 !important; border: 1px solid #2D3748; }
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ───
@st.cache_data
def load_data():
    d = pd.read_csv("Telemedicine_Survey_Cleaned.csv")
    d["Q24_Open_Response"] = d["Q24_Open_Response"].fillna("")
    return d

df = load_data().copy()  # .copy() so we can safely add columns later

# ─── COLOUR PALETTE ───
COLORS = {"Yes": "#0D9488", "Maybe": "#F59E0B", "No": "#EF4444"}
PAL = ["#0D5C63", "#178A94", "#F7941D", "#EF4444", "#6366F1", "#10B981", "#F472B6"]
BG = "rgba(0,0,0,0)"

# ─── LABEL MAPS ───
Q10_LABELS = {
    "Q10_Language_barriers": "Language Barriers",
    "Q10_Long_waiting_times": "Long Waiting Times",
    "Q10_High_out-of-pocket_costs": "High Out-of-Pocket Costs",
    "Q10_Difficulty_finding_specialists": "Difficulty Finding Specialists",
    "Q10_Lack_of_insurance_knowledge": "Lack of Insurance Knowledge",
    "Q10_Inconvenient_locations_hours": "Inconvenient Locations/Hours",
    "Q10_Difficulty_with_medical_records": "Difficulty with Medical Records",
    "Q10_Limited_mental_health_services": "Limited Mental Health Services",
    "Q10_Lack_of_trust_with_providers": "Lack of Trust with Providers",
    "Q10_Difficulty_with_prescriptions": "Difficulty with Prescriptions",
    "Q10_No_challenges": "No Challenges",
}
Q16_LABELS = {
    "Q16_Virtual_consultations_in_preferred_language": "Virtual Consults (Own Language)",
    "Q16_Specialist_referrals_and_booking": "Specialist Referrals & Booking",
    "Q16_E-prescriptions_and_medication_delivery": "E-Prescriptions & Delivery",
    "Q16_Health_record_management": "Health Record Management",
    "Q16_Insurance_compatibility_checker": "Insurance Compatibility Checker",
    "Q16_AI_symptom_checker_triage": "AI Symptom Checker / Triage",
    "Q16_Mental_health_and_counseling": "Mental Health & Counseling",
    "Q16_Lab_test_booking_and_home_collection": "Lab Tests & Home Collection",
    "Q16_Doctor_clinic_reviews_and_ratings": "Doctor/Clinic Reviews & Ratings",
    "Q16_Emergency_helpline_and_hospital_locator": "Emergency Helpline & Locator",
    "Q16_Health_tips_for_expat_lifestyle": "Health Tips (Expat Lifestyle)",
}
Q10_COLS = [c for c in df.columns if c.startswith("Q10_") and c != "Q10_No_challenges"]
Q16_COLS = [c for c in df.columns if c.startswith("Q16_")]
Q21_COLS = [c for c in df.columns if c.startswith("Q21_") and c != "Q21_No_concerns"]
Q22_COLS = [c for c in df.columns if c.startswith("Q22_")]

AGE_ORDER = ["18-24", "25-34", "35-44", "45-54", "55+"]
INCOME_ORDER = ["Below 5,000", "5,000-10,000", "10,001-20,000", "20,001-35,000", "35,001-50,000", "Above 50,000", "Prefer not to say"]
INTEREST_ORDER = ["Yes", "Maybe", "No"]
WTP_ORDER = ["Free only", "Up to AED 30", "AED 31-60", "AED 61-100", "AED 101-150", "More than AED 150"]
TELEMED_ORDER = ["No, never heard", "No, but aware", "Yes, once or twice", "Yes, regularly"]
SAT_ORDER = [1, 2, 3, 4, 5]

def fmt_chart(fig, h=420):
    fig.update_layout(plot_bgcolor=BG, paper_bgcolor=BG,
                      font=dict(size=12, color="#E2E8F0"),
                      title_font=dict(size=16, color="#E2E8F0"),
                      margin=dict(l=20, r=20, t=50, b=20), height=h,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                                  font=dict(color="#E2E8F0")),
                      xaxis=dict(gridcolor="#2D3748", zerolinecolor="#2D3748",
                                 title_font=dict(color="#E2E8F0"), tickfont=dict(color="#CBD5E1")),
                      yaxis=dict(gridcolor="#2D3748", zerolinecolor="#2D3748",
                                 title_font=dict(color="#E2E8F0"), tickfont=dict(color="#CBD5E1")))
    return fig

def insight_box(text):
    st.markdown(f"<div style='background:#1A2332;border-left:4px solid #0D9488;padding:10px 14px;margin:8px 0;border-radius:4px;font-size:14px;color:#CBD5E1'>{text}</div>", unsafe_allow_html=True)

def metric_card(label, value, delta=None):
    st.metric(label=label, value=value, delta=delta)

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("## 🏥 Telemedicine App")
    st.markdown("### Market Intelligence Dashboard")
    st.markdown("---")
    st.markdown("**North Star Metric:**")
    st.markdown("🎯 App Adoption Likelihood (Q25)")
    st.markdown("---")
    yes_pct = (df["Q25_Interest"] == "Yes").mean() * 100
    maybe_pct = (df["Q25_Interest"] == "Maybe").mean() * 100
    no_pct = (df["Q25_Interest"] == "No").mean() * 100
    st.markdown(f"**🟢 Yes:** {yes_pct:.1f}%")
    st.markdown(f"**🟡 Maybe:** {maybe_pct:.1f}%")
    st.markdown(f"**🔴 No:** {no_pct:.1f}%")
    st.markdown("---")
    st.markdown(f"**Respondents:** {len(df):,}")
    st.markdown(f"**Features:** {df.shape[1]} columns")
    st.markdown("---")
    st.markdown("*UAE Expat Telemedicine Survey*")

# ─── TABS ───
tabs = st.tabs(["📋 Data Overview", "👥 Demographics", "🏥 Healthcare Landscape",
                "📊 Adoption Drivers", "🎯 Segmentation", "🔗 Association Rules",
                "🤖 Predictive Models", "💡 Recommendations"])

# ═══════════════════════════════════════════════════════════
# TAB 1 — DATA OVERVIEW & QUALITY
# ═══════════════════════════════════════════════════════════
with tabs[0]:
    st.header("Data Overview & Quality Report")
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Rows", f"{len(df):,}")
    with c2: metric_card("Columns", df.shape[1])
    with c3: metric_card("Missing Values", 0)
    with c4: metric_card("Outliers Treated", "17 capped")

    st.subheader("Column Types Summary")
    dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
    dtype_counts.columns = ["Data Type", "Count"]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(dtype_counts, hide_index=True, width="stretch")
    with col2:
        fig = px.pie(dtype_counts, values="Count", names="Data Type", color_discrete_sequence=PAL)
        fmt_chart(fig, 300)
        st.plotly_chart(fig, width="stretch")

    st.subheader("Missing Value Treatment Summary")
    missing_data = pd.DataFrame({
        "Column": ["Q1_Age_Group", "Q6_Income_AED", "Q9_Visit_Frequency", "Q12_Satisfaction",
                    "Q15_Digital_Comfort", "Q19_Willingness_to_Pay", "Q24_Open_Response"],
        "Missing Count": [20, 20, 20, 20, 20, 20, 962],
        "Missing %": ["1.0%", "1.0%", "1.0%", "1.0%", "1.0%", "1.0%", "48.1%"],
        "Treatment": ["Mode imputation ('25-34')", "Conditional mode (by employment group)",
                       "Mode imputation ('Occasionally 2-4')", "Median imputation (3)",
                       "Median imputation (4)", "Conditional mode (by income bracket)",
                       "Filled with empty string (voluntary non-response)"],
        "Rationale": [
            "Key clustering/classification predictor; mode preserves dominant distribution",
            "Income correlates with employment; conditional mode is more accurate than global",
            "Ordinal predictor for classification & regression; mode preserves utilisation distribution",
            "Likert scale — median respects ordinal nature without inflating modal class",
            "Same as Q12; median assigns neutral value that won't bias classifier",
            "WTP tightly coupled with income; conditional mode preserves income–WTP relationship",
            "Open-ended Qs routinely have 40-60% non-response; blank = no suggestion"
        ]
    })
    st.dataframe(missing_data, hide_index=True, width="stretch")

    st.subheader("Outlier Detection — Monthly Healthcare Spend (IQR Method)")
    col1, col2 = st.columns(2)
    with col1:
        outlier_stats = pd.DataFrame({
            "Metric": ["Q1 (25th percentile)", "Q3 (75th percentile)", "IQR", "Lower Fence",
                       "Upper Fence", "Outliers Flagged", "Plausible High Spenders", "Implausible (Capped)"],
            "Value": ["330 AED", "1,132 AED", "802 AED", "-874 AED", "2,336 AED",
                       "156 (7.8%)", "139", "17 → capped at 10,000 AED"]
        })
        st.dataframe(outlier_stats, hide_index=True, width="stretch")
    with col2:
        fig = px.box(df, y="Q13_Monthly_Spend_AED", color_discrete_sequence=[PAL[1]])
        fig.update_layout(title="Post-Cleaning Spend Distribution", yaxis_title="AED/month")
        fmt_chart(fig, 380)
        st.plotly_chart(fig, width="stretch")

    st.subheader("Cleaning Steps Applied")
    steps = [
        "**Step 1:** Removed 10 near-duplicate submissions (IDs > R2000) — prevents profile inflation in clustering",
        "**Step 2:** Imputed ~1% missing values across 6 columns using mode/median/conditional mode — zero row loss",
        "**Step 3:** Capped 17 implausible spend values (>10K AED) at 10,000; flagged 139 high spenders; created log-transformed column",
        "**Step 4:** Label-encoded 8 ordinal variables as ranked integers; created binary Q25 target",
        "**Step 5:** One-hot encoded 7 nominal variables into 32 binary dummies",
        "**Step 6:** Verified all 34 multi-select binary columns (Q10, Q16, Q21, Q22) — clean 0/1 values",
        "**Step 7:** Final dataset: 2,000 rows × 99 columns — zero missing values, all Q25 labels preserved"
    ]
    for s in steps:
        st.markdown(f"- {s}")

# ═══════════════════════════════════════════════════════════
# TAB 2 — DEMOGRAPHIC PROFILE
# ═══════════════════════════════════════════════════════════
with tabs[1]:
    st.header("Demographic Profile of Respondents")

    col1, col2 = st.columns(2)
    with col1:
        # 1. Age
        age_df = df["Q1_Age_Group"].value_counts().reindex(AGE_ORDER).reset_index()
        age_df.columns = ["Age Group", "Count"]
        fig = px.bar(age_df, x="Age Group", y="Count", color_discrete_sequence=[PAL[0]], text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(title="1. Age Group Distribution")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("The 25-44 age range dominates (~65%), reflecting UAE's working-age expat population. This is also the most digitally active demographic — a strong foundation for app adoption.")

    with col2:
        # 2. Gender
        gender_df = df["Q2_Gender"].value_counts().reset_index()
        gender_df.columns = ["Gender", "Count"]
        fig = px.pie(gender_df, values="Count", names="Gender", hole=0.45, color_discrete_sequence=PAL)
        fig.update_layout(title="2. Gender Distribution")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("~68% male respondents mirrors the UAE expat workforce composition. Both genders should be considered in UX design, but marketing can initially skew toward the majority segment.")

    col1, col2 = st.columns(2)
    with col1:
        # 3. Nationality
        nat_df = df["Q3_Nationality"].value_counts().reset_index()
        nat_df.columns = ["Nationality", "Count"]
        fig = px.bar(nat_df.sort_values("Count", ascending=True), x="Count", y="Nationality",
                     orientation="h", color_discrete_sequence=[PAL[1]], text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(title="3. Nationality / Region Breakdown")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("South Asians form the largest bloc (~42%), followed by Southeast Asians (~18%). Multilingual support — especially Hindi/Urdu, Tagalog, and Arabic — is critical for reaching the majority.")

    with col2:
        # 4. Employment
        emp_df = df["Q5_Employment"].value_counts().reset_index()
        emp_df.columns = ["Employment", "Count"]
        fig = px.bar(emp_df.sort_values("Count", ascending=True), x="Count", y="Employment",
                     orientation="h", color_discrete_sequence=[PAL[2]], text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(title="4. Employment Status Distribution")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("Full-time employees (~52%) represent the core audience with employer insurance and stable income. Self-employed and dependents form secondary segments with distinct needs.")

    # 5. Income
    inc_df = df["Q6_Income_AED"].value_counts().reindex(INCOME_ORDER).reset_index()
    inc_df.columns = ["Income Bracket", "Count"]
    fig = px.bar(inc_df, x="Income Bracket", y="Count", color_discrete_sequence=[PAL[0]], text="Count")
    fig.update_traces(textposition="outside")
    fig.update_layout(title="5. Monthly Household Income Distribution (AED)")
    fmt_chart(fig, 400)
    st.plotly_chart(fig, width="stretch")
    insight_box("The income distribution peaks at AED 10,001-20,000 (~28%), indicating a solid middle-income base. Pricing strategy should anchor around what this segment can afford (AED 30-60/month subscription).")

# ═══════════════════════════════════════════════════════════
# TAB 3 — HEALTHCARE LANDSCAPE
# ═══════════════════════════════════════════════════════════
with tabs[2]:
    st.header("Current Healthcare Landscape")

    col1, col2 = st.columns(2)
    with col1:
        # 6. Insurance
        ins_df = df["Q8_Insurance"].value_counts().reset_index()
        ins_df.columns = ["Insurance Status", "Count"]
        fig = px.bar(ins_df, x="Insurance Status", y="Count", color_discrete_sequence=[PAL[0]], text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(title="6. Insurance Status")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("~45% have employer-provided insurance, but a significant portion are self-insured or uninsured. The insurance compatibility checker feature addresses a real pain point for these segments.")

    with col2:
        # 7. Visit frequency
        visit_order = ["Rarely (0-1)", "Occasionally (2-4)", "Regularly (5-8)", "Frequently (9+)"]
        visit_df = df["Q9_Visit_Frequency"].value_counts().reindex(visit_order).reset_index()
        visit_df.columns = ["Visit Frequency", "Count"]
        fig = px.bar(visit_df, x="Visit Frequency", y="Count", color_discrete_sequence=[PAL[1]], text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(title="7. Doctor Visit Frequency (per year)")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("~70% visit a healthcare provider 0-4 times/year — the app could convert infrequent visitors into regular users through convenient virtual consultations and preventive health features.")

    col1, col2 = st.columns(2)
    with col1:
        # 8. Satisfaction
        sat_df = df["Q12_Satisfaction"].value_counts().sort_index().reset_index()
        sat_df.columns = ["Satisfaction (1-5)", "Count"]
        sat_colors = ["#EF4444", "#F59E0B", "#9CA3AF", "#10B981", "#0D9488"]
        fig = px.bar(sat_df, x="Satisfaction (1-5)", y="Count", color="Satisfaction (1-5)",
                     color_discrete_sequence=sat_colors)
        fig.update_traces(texttemplate="%{y}", textposition="outside")
        fig.update_layout(title="8. Healthcare Satisfaction Level", showlegend=False)
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("The satisfaction distribution centres around 3 (neutral), with a notable tail of dissatisfied respondents (1-2). These ~30% dissatisfied expats represent the highest-propensity adopters.")

    with col2:
        # 9. Top challenges
        challenge_counts = df[list(Q10_LABELS.keys())].sum().sort_values(ascending=True)
        ch_df = pd.DataFrame({"Challenge": [Q10_LABELS[c] for c in challenge_counts.index],
                               "Count": challenge_counts.values})
        fig = px.bar(ch_df, x="Count", y="Challenge", orientation="h", color_discrete_sequence=[PAL[2]], text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(title="9. Top Healthcare Challenges (Multi-Select)")
        fmt_chart(fig, 480)
        st.plotly_chart(fig, width="stretch")
        insight_box("High out-of-pocket costs (49%), long waiting times (44%), and language barriers (36%) are the top three challenges — directly mapping to e-prescriptions, appointment booking, and multilingual consultation features.")

    # 10. Spend histogram
    fig = px.histogram(df, x="Q13_Monthly_Spend_AED", nbins=50, color_discrete_sequence=[PAL[0]],
                       marginal="box")
    fig.update_layout(title="10. Monthly Healthcare Expenditure Distribution (AED)", xaxis_title="AED/month",
                      yaxis_title="Frequency")
    fmt_chart(fig, 420)
    st.plotly_chart(fig, width="stretch")
    insight_box("Heavily right-skewed with median ~660 AED. The long tail includes high spenders (chronic conditions, families) — these are economically valuable targets. Outliers beyond 10K AED were capped during cleaning.")

# ═══════════════════════════════════════════════════════════
# TAB 4 — ADOPTION DRIVERS
# ═══════════════════════════════════════════════════════════
with tabs[3]:
    st.header("Adoption Drivers — Everything vs Q25 Interest")

    col1, col2 = st.columns(2)
    with col1:
        # 11. Age vs Q25
        ct = pd.crosstab(df["Q1_Age_Group"], df["Q25_Interest"], normalize="index").reindex(AGE_ORDER)[INTEREST_ORDER] * 100
        fig = go.Figure()
        for interest in INTEREST_ORDER:
            fig.add_trace(go.Bar(name=interest, x=ct.index, y=ct[interest], marker_color=COLORS[interest]))
        fig.update_layout(barmode="group", title="11. Age Group vs Adoption Interest (%)", yaxis_title="% within age group")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("Younger age groups (18-34) show the highest 'Yes' rates. The 55+ segment has the lowest adoption — they may need simplified UX or assisted onboarding.")

    with col2:
        # 12. Income vs Q25
        ct = pd.crosstab(df["Q6_Income_AED"], df["Q25_Interest"], normalize="index")
        ct = ct.reindex([i for i in INCOME_ORDER if i in ct.index])[INTEREST_ORDER] * 100
        fig = go.Figure()
        for interest in INTEREST_ORDER:
            fig.add_trace(go.Bar(name=interest, x=ct.index, y=ct[interest], marker_color=COLORS[interest]))
        fig.update_layout(barmode="stack", title="12. Income Level vs Adoption Interest (%)", yaxis_title="%", xaxis_tickangle=-30)
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("Mid-to-high income brackets (20K-50K AED) show stronger 'Yes' rates. Low-income respondents lean toward 'Maybe' — pricing sensitivity is a conversion barrier for this group.")

    col1, col2 = st.columns(2)
    with col1:
        # 13. Insurance vs Q25
        ct = pd.crosstab(df["Q8_Insurance"], df["Q25_Interest"], normalize="index")[INTEREST_ORDER] * 100
        fig = go.Figure()
        for interest in INTEREST_ORDER:
            fig.add_trace(go.Bar(name=interest, x=ct.index, y=ct[interest], marker_color=COLORS[interest]))
        fig.update_layout(barmode="group", title="13. Insurance Status vs Adoption Interest (%)", yaxis_title="%")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("Uninsured respondents show polarised responses — high 'Yes' (they need affordable care) but also high 'No' (they may not trust digital health). The insurance checker feature could convert the 'Maybe' group.")

    with col2:
        # 14. Satisfaction vs Q25
        ct = pd.crosstab(df["Q12_Satisfaction"], df["Q25_Interest"], normalize="index")[INTEREST_ORDER] * 100
        fig = go.Figure()
        for interest in INTEREST_ORDER:
            fig.add_trace(go.Bar(name=interest, x=ct.index, y=ct[interest], marker_color=COLORS[interest]))
        fig.update_layout(barmode="group", title="14. Satisfaction vs Adoption Interest (%)", yaxis_title="%",
                          xaxis_title="Satisfaction (1-5)")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("Clear inverse relationship: dissatisfied respondents (scores 1-2) show the highest 'Yes' rates. Satisfaction is one of the strongest adoption predictors — target the frustrated first.")

    col1, col2 = st.columns(2)
    with col1:
        # 15. Spend vs Q25 — box plot
        fig = px.box(df, x="Q25_Interest", y="Q13_Monthly_Spend_AED", color="Q25_Interest",
                     category_orders={"Q25_Interest": INTEREST_ORDER}, color_discrete_map=COLORS)
        fig.update_layout(title="15. Monthly Spend vs Adoption Interest", yaxis_title="AED/month", showlegend=False)
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("'Yes' respondents tend to have higher median spend — they are currently spending more and see the app as a way to manage costs better. These are economically valuable adopters.")

    with col2:
        # 16. Most desired features
        feat_counts = df[Q16_COLS].sum().sort_values(ascending=True)
        feat_df = pd.DataFrame({"Feature": [Q16_LABELS.get(c, c) for c in feat_counts.index],
                                 "Count": feat_counts.values})
        fig = px.bar(feat_df, x="Count", y="Feature", orientation="h", color_discrete_sequence=[PAL[1]], text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(title="16. Most Desired App Features")
        fmt_chart(fig, 480)
        st.plotly_chart(fig, width="stretch")
        insight_box("E-prescriptions, specialist referrals, virtual consultations, and emergency helpline top the list. These four features should form the MVP core.")

    col1, col2 = st.columns(2)
    with col1:
        # 17. Consultation mode vs Q25
        ct = pd.crosstab(df["Q18_Consultation_Mode"], df["Q25_Interest"], normalize="index")[INTEREST_ORDER] * 100
        fig = go.Figure()
        for interest in INTEREST_ORDER:
            fig.add_trace(go.Bar(name=interest, x=ct.index, y=ct[interest], marker_color=COLORS[interest]))
        fig.update_layout(barmode="group", title="17. Consultation Mode vs Adoption (%)", yaxis_title="%")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("Video call preference shows the highest 'Yes' rate — invest in high-quality video consultation infrastructure first, with voice and chat as secondary options.")

    with col2:
        # 18. WTP vs Q25
        ct = pd.crosstab(df["Q19_Willingness_to_Pay"], df["Q25_Interest"], normalize="index")
        ct = ct.reindex([w for w in WTP_ORDER if w in ct.index])[INTEREST_ORDER] * 100
        fig = go.Figure()
        for interest in INTEREST_ORDER:
            fig.add_trace(go.Bar(name=interest, x=ct.index, y=ct[interest], marker_color=COLORS[interest]))
        fig.update_layout(barmode="stack", title="18. Willingness to Pay vs Adoption (%)", yaxis_title="%", xaxis_tickangle=-30)
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("Higher WTP brackets show progressively higher 'Yes' rates. The 'Free only' group is mostly 'Maybe/No' — a freemium model can capture them while monetising willingness in mid-to-high tiers.")

    col1, col2 = st.columns(2)
    with col1:
        # 19. Telemedicine experience vs Q25
        ct = pd.crosstab(df["Q14_Prior_Telemedicine"], df["Q25_Interest"], normalize="index")
        ct = ct.reindex([t for t in TELEMED_ORDER if t in ct.index])[INTEREST_ORDER] * 100
        fig = go.Figure()
        for interest in INTEREST_ORDER:
            fig.add_trace(go.Bar(name=interest, x=ct.index, y=ct[interest], marker_color=COLORS[interest]))
        fig.update_layout(barmode="group", title="19. Prior Telemedicine Experience vs Adoption (%)", yaxis_title="%")
        fmt_chart(fig)
        st.plotly_chart(fig, width="stretch")
        insight_box("Prior users are dramatically more likely to say 'Yes'. This confirms the 'try it once' hypothesis — offering free trial consultations could be the strongest conversion lever.")

    with col2:
        # 20. Correlation heatmap
        num_cols = ["Q1_Age_Group_Encoded", "Q4_Duration_UAE_Encoded", "Q6_Income_AED_Encoded",
                    "Q7_Education_Encoded", "Q9_Visit_Frequency_Encoded", "Q12_Satisfaction",
                    "Q13_Monthly_Spend_AED", "Q14_Prior_Telemedicine_Encoded", "Q15_Digital_Comfort",
                    "Q17_Language_Importance", "Q19_Willingness_to_Pay_Encoded",
                    "Q23_Recommend_Likelihood", "Q25_Interest_Encoded"]
        short_labels = ["Age", "Duration", "Income", "Education", "Visits", "Satisfaction",
                        "Spend", "Telemed Exp.", "Digital Comfort", "Lang. Import.", "WTP",
                        "Recommend", "Interest(Q25)"]
        corr = df[num_cols].corr()
        fig = px.imshow(corr.values, x=short_labels, y=short_labels, color_continuous_scale="Teal",
                        zmin=-1, zmax=1, text_auto=".2f", aspect="auto")
        fig.update_layout(title="20. Correlation Heatmap (Ordinal & Numeric Variables)",
                          coloraxis_colorbar=dict(tickfont=dict(color="#CBD5E1")))
        fmt_chart(fig, 520)
        st.plotly_chart(fig, width="stretch")
        insight_box("Q25 Interest correlates most with Digital Comfort, Prior Telemedicine Experience, and inversely with Satisfaction — confirming that tech-savvy, dissatisfied expats with prior telemedicine exposure are the prime adopters.")

    # 21. Sankey Diagram — Challenge → Feature → Adoption flow
    st.subheader("21. Adoption Flow: Challenges → Features → Interest")
    st.markdown("*How healthcare challenges drive feature demand, which flows into adoption intent.*")

    # Build Sankey: top 5 challenges → top 5 features → Q25 (Yes/Maybe/No)
    top_ch = df[Q10_COLS].sum().nlargest(5)
    top_ft = df[Q16_COLS].sum().nlargest(5)
    ch_names = [Q10_LABELS.get(c, c) for c in top_ch.index]
    ft_names = [Q16_LABELS.get(c, c) for c in top_ft.index]
    q25_names = ["Yes", "Maybe", "No"]
    all_labels = ch_names + ft_names + q25_names  # 5 + 5 + 3 = 13 nodes

    sources, targets, values = [], [], []

    # Layer 1: Challenge → Feature (count of respondents who have both)
    for ci, ch_col in enumerate(top_ch.index):
        for fi, ft_col in enumerate(top_ft.index):
            overlap = ((df[ch_col] == 1) & (df[ft_col] == 1)).sum()
            if overlap > 30:  # threshold for visual clarity
                sources.append(ci)
                targets.append(5 + fi)  # offset by 5 (challenge nodes)
                values.append(int(overlap))

    # Layer 2: Feature → Q25 Interest
    for fi, ft_col in enumerate(top_ft.index):
        for qi, interest in enumerate(q25_names):
            count = ((df[ft_col] == 1) & (df["Q25_Interest"] == interest)).sum()
            if count > 20:
                sources.append(5 + fi)
                targets.append(10 + qi)  # offset by 10
                values.append(int(count))

    # Node colours
    node_colors = (["#0D9488"] * 5 +    # challenges = teal
                   ["#F59E0B"] * 5 +     # features = amber
                   ["#10B981", "#6366F1", "#EF4444"])  # Yes/Maybe/No
    link_colors = ["rgba(13,148,136,0.2)"] * len(values)

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(pad=20, thickness=25, line=dict(color="#2D3748", width=1),
                  label=all_labels, color=node_colors),
        link=dict(source=sources, target=targets, value=values, color=link_colors)
    ))
    fig.update_layout(title="Adoption Flow: Top Challenges → Top Features → Interest",
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E2E8F0"),
                      title_font=dict(color="#E2E8F0", size=16), height=550)
    st.plotly_chart(fig, width="stretch")
    insight_box("The Sankey reveals the dominant pathway: cost and waiting-time challenges drive demand for e-prescriptions and specialist referrals, which flow heavily into 'Yes' and 'Maybe' adoption. Language barriers create a distinct pathway toward multilingual virtual consultations. These three feature channels carry the most adoption volume.")

# ═══════════════════════════════════════════════════════════
# TAB 5 — CUSTOMER SEGMENTATION (K-MEANS)
# ═══════════════════════════════════════════════════════════
with tabs[4]:
    st.header("Customer Segmentation — K-Means Clustering")

    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.decomposition import PCA

    # Prepare features
    cluster_features = (["Q1_Age_Group_Encoded", "Q4_Duration_UAE_Encoded", "Q6_Income_AED_Encoded",
                         "Q7_Education_Encoded", "Q9_Visit_Frequency_Encoded", "Q12_Satisfaction",
                         "Q13_Spend_Log", "Q15_Digital_Comfort", "Q17_Language_Importance",
                         "Q19_Willingness_to_Pay_Encoded", "Q23_Recommend_Likelihood"]
                        + Q10_COLS + [c for c in Q21_COLS])

    X_cluster = df[cluster_features].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_cluster)

    # ── PCA dimensionality reduction ──
    # With 27 features (many sparse binary), Euclidean distances become noisy.
    # PCA concentrates variance into fewer components, giving K-Means denser signal.
    pca_full = PCA(random_state=42).fit(X_scaled)
    cumvar = np.cumsum(pca_full.explained_variance_ratio_)
    n_components = int(np.argmax(cumvar >= 0.80)) + 1  # retain ≥80% variance
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    var_explained = pca.explained_variance_ratio_.sum() * 100

    st.subheader("PCA Dimensionality Reduction")
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(1, len(cumvar)+1)), y=cumvar * 100,
                                 mode="lines+markers", marker=dict(color=PAL[1], size=6),
                                 line=dict(color=PAL[1])))
        fig.add_hline(y=80, line_dash="dash", line_color="#EF4444",
                      annotation_text="80% threshold", annotation_font_color="#EF4444")
        fig.update_layout(title="Cumulative Variance Explained by PCA",
                          xaxis_title="Number of Components", yaxis_title="Cumulative Variance (%)")
        fmt_chart(fig, 380)
        st.plotly_chart(fig, width="stretch")

    with col2:
        # Per-component variance
        comp_var = pca_full.explained_variance_ratio_[:n_components] * 100
        fig = go.Figure()
        fig.add_trace(go.Bar(x=list(range(1, n_components+1)), y=comp_var,
                             marker_color=PAL[0]))
        fig.update_layout(title=f"Variance per Component (Top {n_components})",
                          xaxis_title="Component", yaxis_title="Variance Explained (%)")
        fmt_chart(fig, 380)
        st.plotly_chart(fig, width="stretch")

    st.info(f"**PCA: {len(cluster_features)} features → {n_components} components** "
            f"retaining {var_explained:.1f}% of total variance. "
            f"This reduces noise from sparse binary indicators and improves K-Means distance quality.")

    # 2D PCA for scatter plot later
    pca_2d = PCA(n_components=2, random_state=42).fit_transform(X_scaled)

    # ── Elbow & Silhouette (on PCA-reduced data) ──
    K_range = range(2, 9)
    inertias, sil_scores = [], []
    # Also compute silhouette WITHOUT PCA for comparison
    sil_no_pca = []
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_pca)
        inertias.append(km.inertia_)
        sil_scores.append(silhouette_score(X_pca, km.labels_, sample_size=1000, random_state=42))
        km2 = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
        sil_no_pca.append(silhouette_score(X_scaled, km2.labels_, sample_size=1000, random_state=42))

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(K_range), y=inertias, mode="lines+markers",
                                 marker=dict(color=PAL[0], size=10), line=dict(color=PAL[0])))
        fig.update_layout(title="Elbow Method — Optimal k (PCA)", xaxis_title="Number of Clusters (k)",
                          yaxis_title="Inertia")
        fmt_chart(fig, 380)
        st.plotly_chart(fig, width="stretch")

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(K_range), y=sil_scores, mode="lines+markers",
                                 marker=dict(color=PAL[2], size=10), line=dict(color=PAL[2]),
                                 name="With PCA"))
        fig.add_trace(go.Scatter(x=list(K_range), y=sil_no_pca, mode="lines+markers",
                                 marker=dict(color=PAL[3], size=8), line=dict(color=PAL[3], dash="dot"),
                                 name="Without PCA"))
        fig.update_layout(title="Silhouette Score: PCA vs Raw", xaxis_title="Number of Clusters (k)",
                          yaxis_title="Silhouette Score")
        fmt_chart(fig, 380)
        st.plotly_chart(fig, width="stretch")

    # Fit optimal k — Kneedle algorithm (max perpendicular distance from chord)
    # Pure silhouette favours k=2 with high-dimensional binary data (scores are all ~0.05).
    # Kneedle finds the true elbow; business constraint clamps to [4, 6] for actionable personas.
    k_list = list(K_range)
    x = np.array(k_list, dtype=float)
    y = np.array(inertias, dtype=float)
    x_norm = (x - x.min()) / (x.max() - x.min())
    y_norm = (y - y.min()) / (y.max() - y.min())
    p1, p2 = np.array([x_norm[0], y_norm[0]]), np.array([x_norm[-1], y_norm[-1]])
    distances = [abs(np.cross(p2 - p1, p1 - np.array([x_norm[i], y_norm[i]]))) / np.linalg.norm(p2 - p1)
                 for i in range(len(x_norm))]
    elbow_k = k_list[int(np.argmax(distances))]
    optimal_k = max(min(elbow_k, 6), 4)  # business constraint: 4-6 personas

    st.info(f"**Optimal k = {optimal_k}** — Kneedle elbow at k={elbow_k}, "
            f"business range [4-6]. Silhouette at k={optimal_k}: {sil_scores[optimal_k - 2]:.3f}")

    km_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    df["Cluster"] = km_final.fit_predict(X_pca)

    # 2D PCA scatter plot coloured by cluster
    st.subheader("2D PCA Projection — Cluster Visualisation")
    scatter_df = pd.DataFrame({"PC1": pca_2d[:, 0], "PC2": pca_2d[:, 1],
                                "Cluster": df["Cluster"].astype(str)})
    fig = px.scatter(scatter_df, x="PC1", y="PC2", color="Cluster",
                     color_discrete_sequence=PAL, opacity=0.6,
                     labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2"})
    fig.update_layout(title="Respondents in PCA Space (Coloured by Cluster)")
    fmt_chart(fig, 450)
    st.plotly_chart(fig, width="stretch")

    # Profile clusters
    profile_cols = ["Q1_Age_Group_Encoded", "Q6_Income_AED_Encoded", "Q9_Visit_Frequency_Encoded",
                    "Q12_Satisfaction", "Q13_Monthly_Spend_AED", "Q15_Digital_Comfort",
                    "Q17_Language_Importance", "Q19_Willingness_to_Pay_Encoded", "Q23_Recommend_Likelihood"]
    profile_labels = ["Age", "Income", "Visit Freq.", "Satisfaction", "Spend (AED)",
                      "Digital Comfort", "Language Import.", "WTP", "Recommend"]

    cluster_profiles = df.groupby("Cluster")[profile_cols].mean()

    # Adoption rate per cluster
    adoption_rates = pd.crosstab(df["Cluster"], df["Q25_Interest"], normalize="index")[INTEREST_ORDER] * 100

    # Name clusters based on their profiles
    persona_names = {}
    for c in range(optimal_k):
        p = cluster_profiles.loc[c]
        traits = []
        if p["Q6_Income_AED_Encoded"] >= 4: traits.append("High-Income")
        elif p["Q6_Income_AED_Encoded"] <= 2.5: traits.append("Budget-Conscious")
        else: traits.append("Mid-Income")
        if p["Q15_Digital_Comfort"] >= 4: traits.append("Digital-Savvy")
        elif p["Q15_Digital_Comfort"] <= 2.5: traits.append("Tech-Hesitant")
        if p["Q1_Age_Group_Encoded"] <= 2: traits.append("Young")
        elif p["Q1_Age_Group_Encoded"] >= 4: traits.append("Senior")
        if p["Q12_Satisfaction"] <= 2.5: traits.append("Dissatisfied")
        if p["Q13_Monthly_Spend_AED"] >= 1200: traits.append("High-Spenders")
        elif p["Q13_Monthly_Spend_AED"] <= 500: traits.append("Low-Spenders")
        if p["Q17_Language_Importance"] >= 4: traits.append("Language-Sensitive")
        if p["Q19_Willingness_to_Pay_Encoded"] <= 2.5: traits.append("Price-Sensitive")
        elif p["Q19_Willingness_to_Pay_Encoded"] >= 4.5: traits.append("Premium-Ready")
        persona_names[c] = " ".join(traits[:3]) + " Expats"

    # Deduplicate: if two clusters share the same name, append the 4th trait
    seen = {}
    for c in range(optimal_k):
        name = persona_names[c]
        if name in seen:
            p = cluster_profiles.loc[c]
            all_traits_c = []
            if p["Q6_Income_AED_Encoded"] >= 4: all_traits_c.append("High-Income")
            elif p["Q6_Income_AED_Encoded"] <= 2.5: all_traits_c.append("Budget-Conscious")
            else: all_traits_c.append("Mid-Income")
            if p["Q15_Digital_Comfort"] >= 4: all_traits_c.append("Digital-Savvy")
            if p["Q12_Satisfaction"] <= 2.5: all_traits_c.append("Dissatisfied")
            if p["Q13_Monthly_Spend_AED"] >= 1200: all_traits_c.append("High-Spenders")
            elif p["Q13_Monthly_Spend_AED"] <= 500: all_traits_c.append("Low-Spenders")
            if p["Q17_Language_Importance"] >= 4: all_traits_c.append("Language-Sensitive")
            if p["Q19_Willingness_to_Pay_Encoded"] <= 2.5: all_traits_c.append("Price-Sensitive")
            # Use more traits to differentiate
            persona_names[c] = " ".join(all_traits_c[:4]) + " Expats"
            # If still duplicate, append cluster adoption rank
            if persona_names[c] in seen:
                yes_rate = adoption_rates.loc[c, "Yes"]
                persona_names[c] = persona_names[c].replace("Expats", f"(Adopt {yes_rate:.0f}%) Expats")
        seen[persona_names[c]] = c

    # Cluster size
    cluster_sizes = df["Cluster"].value_counts().sort_index()
    size_df = pd.DataFrame({"Cluster": [f"C{c}: {persona_names[c]}" for c in cluster_sizes.index],
                             "Count": cluster_sizes.values,
                             "Pct": (cluster_sizes.values / len(df) * 100).round(1)})

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(size_df, x="Cluster", y="Count", color_discrete_sequence=[PAL[0]], text="Pct",
                     labels={"Pct": "% of total"})
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(title="Cluster Size Distribution", xaxis_tickangle=-20)
        fmt_chart(fig, 400)
        st.plotly_chart(fig, width="stretch")

    with col2:
        # Adoption rate per cluster
        fig = go.Figure()
        cluster_labels = [f"C{c}: {persona_names[c]}" for c in adoption_rates.index]
        for interest in INTEREST_ORDER:
            fig.add_trace(go.Bar(name=interest, x=cluster_labels, y=adoption_rates[interest],
                                 marker_color=COLORS[interest]))
        fig.update_layout(barmode="stack", title="Adoption Rate by Cluster (%)", yaxis_title="%", xaxis_tickangle=-20)
        fmt_chart(fig, 400)
        st.plotly_chart(fig, width="stretch")

    # Radar chart
    st.subheader("Cluster Profile Comparison — Radar Chart")
    radar_data = cluster_profiles.copy()
    # Normalise to 0-1 for radar
    for col in radar_data.columns:
        mn, mx = radar_data[col].min(), radar_data[col].max()
        if mx > mn:
            radar_data[col] = (radar_data[col] - mn) / (mx - mn)
        else:
            radar_data[col] = 0.5

    fig = go.Figure()
    for c in range(optimal_k):
        vals = radar_data.loc[c].values.tolist()
        vals.append(vals[0])
        labels_r = profile_labels + [profile_labels[0]]
        fig.add_trace(go.Scatterpolar(r=vals, theta=labels_r, fill="toself",
                                       name=f"C{c}: {persona_names[c]}", line_color=PAL[c % len(PAL)]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor="#2D3748", color="#E2E8F0"),
                                  angularaxis=dict(gridcolor="#2D3748", color="#E2E8F0"),
                                  bgcolor="rgba(0,0,0,0)"),
                      title="Cluster Profiles (Normalised)", height=520,
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#E2E8F0"),
                      legend=dict(font=dict(color="#E2E8F0")))
    st.plotly_chart(fig, width="stretch")

    # Persona cards
    st.subheader("Persona Descriptions")
    cols = st.columns(min(optimal_k, 4))
    for i, c in enumerate(range(optimal_k)):
        with cols[i % len(cols)]:
            p = cluster_profiles.loc[c]
            yes_rate = adoption_rates.loc[c, "Yes"]
            st.markdown(f"""
<div style='background:linear-gradient(135deg, #132A2E 0%, #0E2429 100%);padding:16px;border-radius:10px;border:1px solid #0D9488;margin-bottom:12px'>
<h4 style='color:#5EEAD4;margin:0'>🎯 C{c}: {persona_names[c]}</h4>
<p style='font-size:13px;color:#CBD5E1;margin-top:8px'>
<b>Size:</b> {cluster_sizes[c]} ({cluster_sizes[c]/len(df)*100:.1f}%)<br>
<b>Adoption (Yes):</b> {yes_rate:.1f}%<br>
<b>Avg Income Tier:</b> {p["Q6_Income_AED_Encoded"]:.1f}/6<br>
<b>Avg Satisfaction:</b> {p["Q12_Satisfaction"]:.1f}/5<br>
<b>Digital Comfort:</b> {p["Q15_Digital_Comfort"]:.1f}/5<br>
<b>Avg Spend:</b> AED {p["Q13_Monthly_Spend_AED"]:,.0f}/mo<br>
<b>WTP Tier:</b> {p["Q19_Willingness_to_Pay_Encoded"]:.1f}/6</p></div>""", unsafe_allow_html=True)

    # Business interpretation
    best_cluster = adoption_rates["Yes"].idxmax()
    st.subheader("💼 Business Interpretation")
    st.markdown(f"""
**Priority target for launch: Cluster {best_cluster} — {persona_names[best_cluster]}**

This persona shows the **highest adoption rate ({adoption_rates.loc[best_cluster, "Yes"]:.1f}% Yes)** and combines:
- **High digital comfort** — low onboarding friction
- **Strong willingness to pay** — viable for subscription monetisation
- **Higher healthcare spend** — economically valuable users who see the app as cost management
- **Lower satisfaction with current care** — high motivation to switch

**Secondary target:** Focus on converting 'Maybe' respondents in mid-sized clusters through free trials and feature demonstrations addressing their specific challenges.

**Avoid over-investing** in clusters with high 'No' rates and low digital comfort — these require costly education campaigns with uncertain ROI.
""")

# ═══════════════════════════════════════════════════════════
# TAB 6 — ASSOCIATION RULE MINING
# ═══════════════════════════════════════════════════════════
with tabs[5]:
    st.header("Pattern Discovery — Association Rule Mining")
    st.markdown("*Filtered to potential adopters only (Q25 = Yes or Maybe)*")

    from mlxtend.frequent_patterns import apriori, association_rules

    adopters = df[df["Q25_Interest"].isin(["Yes", "Maybe"])].copy()
    st.info(f"Analysis dataset: {len(adopters)} potential adopters ({len(adopters)/len(df)*100:.1f}% of total)")

    def run_arm(data, cols, label_map, min_sup=0.01, min_conf=0.5, max_len=4):
        basket = data[cols].astype(bool)
        basket.columns = [label_map.get(c, c.split("_", 1)[-1].replace("_", " ").title()) for c in cols]
        freq = apriori(basket, min_support=min_sup, use_colnames=True, max_len=max_len)
        if len(freq) == 0:
            return pd.DataFrame()
        rules = association_rules(freq, metric="confidence", min_threshold=min_conf, num_itemsets=len(freq))
        rules["antecedents"] = rules["antecedents"].apply(lambda x: ", ".join(sorted(x)))
        rules["consequents"] = rules["consequents"].apply(lambda x: ", ".join(sorted(x)))
        rules["rule"] = rules["antecedents"] + " → " + rules["consequents"]
        return rules.sort_values("lift", ascending=False).head(20)

    arm_tabs = st.tabs(["🔴 Challenge Co-occurrence", "🟢 Feature Co-occurrence", "🔗 Challenges × Features"])

    # 6a. Challenges
    with arm_tabs[0]:
        st.subheader("6a. Healthcare Challenge Co-occurrence Patterns")
        rules_ch = run_arm(adopters, Q10_COLS, Q10_LABELS)
        if len(rules_ch) > 0:
            st.dataframe(rules_ch[["rule", "support", "confidence", "lift"]].round(3), hide_index=True,
                         width="stretch")
            fig = px.scatter(rules_ch, x="confidence", y="lift", size="support", hover_data=["rule"],
                             color_discrete_sequence=[PAL[3]], size_max=20,
                             labels={"confidence": "Confidence", "lift": "Lift"})
            fig.update_layout(title="Confidence vs Lift — Challenge Rules")
            fmt_chart(fig, 400)
            st.plotly_chart(fig, width="stretch")
        else:
            st.warning("No rules found with current thresholds.")

    # 6b. Features
    with arm_tabs[1]:
        st.subheader("6b. Desired Feature Co-occurrence Patterns")
        rules_ft = run_arm(adopters, Q16_COLS, Q16_LABELS)
        if len(rules_ft) > 0:
            st.dataframe(rules_ft[["rule", "support", "confidence", "lift"]].round(3), hide_index=True,
                         width="stretch")
            fig = px.scatter(rules_ft, x="confidence", y="lift", size="support", hover_data=["rule"],
                             color_discrete_sequence=[PAL[4]], size_max=20)
            fig.update_layout(title="Confidence vs Lift — Feature Rules")
            fmt_chart(fig, 400)
            st.plotly_chart(fig, width="stretch")
        else:
            st.warning("No rules found with current thresholds.")

    # 6c. Cross-mine
    with arm_tabs[2]:
        st.subheader("6c. Cross-Mining: Challenges → Features")
        all_cols = Q10_COLS + Q16_COLS
        all_labels = {**Q10_LABELS, **Q16_LABELS}
        rules_cross = run_arm(adopters, all_cols, all_labels, min_sup=0.01, min_conf=0.5)
        if len(rules_cross) > 0:
            st.dataframe(rules_cross[["rule", "support", "confidence", "lift"]].round(3), hide_index=True,
                         width="stretch")
            fig = px.scatter(rules_cross, x="confidence", y="lift", size="support", hover_data=["rule"],
                             color_discrete_sequence=[PAL[5]], size_max=20)
            fig.update_layout(title="Confidence vs Lift — Cross-Mined Rules")
            fmt_chart(fig, 400)
            st.plotly_chart(fig, width="stretch")
        else:
            st.warning("No rules found with current thresholds.")

    st.subheader("💼 Business Interpretation")
    st.markdown("""
**Key findings from association rule mining:**

1. **Challenge clustering:** High out-of-pocket costs, long waiting times, and lack of insurance knowledge frequently co-occur — respondents facing one tend to face all three. This "cost-frustrated" cluster needs the **insurance checker + e-prescription** combo most urgently.

2. **Feature bundling:** Virtual consultations, specialist referrals, and e-prescriptions are the most commonly co-selected features — they form a natural **MVP feature bundle** that addresses the top 3 challenges.

3. **Cross-mining insight:** The strongest challenge→feature rules confirm that language barriers drive demand for multilingual consultations, cost concerns drive demand for insurance checkers and e-prescriptions, and waiting time frustration drives demand for appointment booking. **Build the features that directly resolve the most common challenge combinations.**
""")

# ═══════════════════════════════════════════════════════════
# TAB 7 — PREDICTIVE MODELS
# ═══════════════════════════════════════════════════════════
with tabs[6]:
    st.header("Predictive Models")

    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler as SS
    from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    try:
        from xgboost import XGBClassifier
        HAS_XGB = True
    except ImportError:
        HAS_XGB = False
    from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                                  confusion_matrix, mean_absolute_error, mean_squared_error, r2_score)

    # ── CLASSIFICATION ──
    class_tab, reg_tab = st.tabs(["🎯 Classification (Q25 Prediction)", "💰 Regression (Spend Prediction)"])

    with class_tab:
        st.subheader("7-Model Classification — Predicting App Adoption (Q25)")

        # Feature set for classification
        exclude_cls = ["Respondent_ID", "Q25_Interest", "Q25_Interest_Encoded", "Q25_Binary",
                       "Q24_Open_Response", "Q13_Outlier_Flag", "Cluster"]
        str_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
        feat_cls = [c for c in df.columns if c not in exclude_cls and c not in str_cols]

        X_cls = df[feat_cls].copy()
        y_cls = df["Q25_Interest_Encoded"].copy()

        X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_cls, y_cls, test_size=0.2,
                                                                       random_state=42, stratify=y_cls)
        scaler_c = SS()
        X_train_sc = scaler_c.fit_transform(X_train_c)
        X_test_sc = scaler_c.transform(X_test_c)

        models_cls = {
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
            "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=10),
            "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
            "SVM": SVC(kernel="rbf", random_state=42),
            "KNN": KNeighborsClassifier(n_neighbors=7),
            "Naive Bayes": GaussianNB(),
        }
        if HAS_XGB:
            models_cls["XGBoost"] = XGBClassifier(n_estimators=200, random_state=42,
                                                   eval_metric="mlogloss", verbosity=0)

        results_cls = []
        best_model_name, best_f1 = None, 0
        fitted_models = {}

        for name, model in models_cls.items():
            if name in ["Logistic Regression", "SVM", "KNN", "Naive Bayes"]:
                model.fit(X_train_sc, y_train_c)
                preds = model.predict(X_test_sc)
            else:
                model.fit(X_train_c, y_train_c)
                preds = model.predict(X_test_c)
            fitted_models[name] = (model, preds)

            acc = accuracy_score(y_test_c, preds)
            prec = precision_score(y_test_c, preds, average="weighted", zero_division=0)
            rec = recall_score(y_test_c, preds, average="weighted", zero_division=0)
            f1 = f1_score(y_test_c, preds, average="weighted", zero_division=0)
            results_cls.append({"Model": name, "Accuracy": acc, "Precision": prec, "Recall": rec, "F1-Score": f1})
            if f1 > best_f1:
                best_f1, best_model_name = f1, name

        res_df = pd.DataFrame(results_cls).sort_values("F1-Score", ascending=False)

        st.markdown(f"**Best model: {best_model_name}** (F1 = {best_f1:.4f})")
        st.dataframe(res_df.style.format({"Accuracy": "{:.4f}", "Precision": "{:.4f}",
                                           "Recall": "{:.4f}", "F1-Score": "{:.4f}"}),
                     hide_index=True, width="stretch")

        col1, col2 = st.columns(2)
        with col1:
            # Comparison bar chart
            res_melt = res_df.melt(id_vars="Model", var_name="Metric", value_name="Score")
            fig = px.bar(res_melt, x="Model", y="Score", color="Metric", barmode="group",
                         color_discrete_sequence=PAL)
            fig.update_layout(title="7-Model Comparison", xaxis_tickangle=-30, yaxis_range=[0, 1])
            fmt_chart(fig, 420)
            st.plotly_chart(fig, width="stretch")

        with col2:
            # Confusion matrix for best model
            _, best_preds = fitted_models[best_model_name]
            cm = confusion_matrix(y_test_c, best_preds)
            labels = ["No (0)", "Maybe (1)", "Yes (2)"]
            fig = px.imshow(cm, text_auto=True, x=labels, y=labels, color_continuous_scale="Teal",
                            labels=dict(x="Predicted", y="Actual"))
            fig.update_layout(title=f"Confusion Matrix — {best_model_name}",
                              coloraxis_colorbar=dict(tickfont=dict(color="#CBD5E1")))
            fmt_chart(fig, 420)
            st.plotly_chart(fig, width="stretch")

        # Feature importance
        st.subheader("Feature Importance — Top 20")
        tree_models = ["XGBoost", "Random Forest", "Decision Tree"]
        imp_model_name = next((m for m in tree_models if m in fitted_models), None)
        if imp_model_name:
            imp_model = fitted_models[imp_model_name][0]
            importances = imp_model.feature_importances_
            feat_imp = pd.DataFrame({"Feature": feat_cls, "Importance": importances})
            feat_imp = feat_imp.sort_values("Importance", ascending=True).tail(20)
            fig = px.bar(feat_imp, x="Importance", y="Feature", orientation="h",
                         color_discrete_sequence=[PAL[0]], text="Importance")
            fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
            fig.update_layout(title=f"Feature Importance — {imp_model_name}")
            fmt_chart(fig, 550)
            st.plotly_chart(fig, width="stretch")

        st.subheader("💼 Business Interpretation — Classification")
        st.markdown(f"""
The **{best_model_name}** achieves the best performance with an F1-score of **{best_f1:.4f}**.

**Key adoption drivers** (from feature importance):
- **Digital comfort & prior telemedicine experience** are the strongest predictors — people who are already comfortable with technology and have used telemedicine before are most likely to adopt.
- **Healthcare satisfaction** is inversely predictive — the more dissatisfied someone is, the more likely they are to say "Yes".
- **Willingness to pay & income** contribute significantly — economic capacity enables adoption intent.
- **Healthcare challenges** (especially cost and language barriers) provide additional predictive signal.

**Actionable insight:** Target digitally comfortable expats who are dissatisfied with their current care and have mid-to-high income. Offer free first consultations to convert the "Maybe" group.
""")

    # ── REGRESSION ──
    with reg_tab:
        st.subheader("3-Model Regression — Predicting Monthly Healthcare Spend (Q13)")
        st.markdown("*Using log-transformed spend (log₁₊ₓ) to normalise right-skewed distribution and improve model fit.*")

        reg_features = ["Q1_Age_Group_Encoded", "Q4_Duration_UAE_Encoded", "Q6_Income_AED_Encoded",
                        "Q9_Visit_Frequency_Encoded", "Q12_Satisfaction", "Q15_Digital_Comfort",
                        "Q14_Prior_Telemedicine_Encoded", "Q17_Language_Importance",
                        "Q19_Willingness_to_Pay_Encoded", "Q23_Recommend_Likelihood",
                        "Q10_High_out-of-pocket_costs", "Q10_Difficulty_finding_specialists",
                        "Q10_Difficulty_with_prescriptions"]

        # Add one-hot insurance columns
        ins_cols = [c for c in df.columns if c.startswith("Q8_Insurance_")]
        reg_features += ins_cols

        X_reg = df[reg_features].copy()
        y_reg_log = df["Q13_Spend_Log"].copy()        # log1p target
        y_reg_raw = df["Q13_Monthly_Spend_AED"].copy() # for back-transformed metrics

        X_train_r, X_test_r, y_train_r, y_test_r, y_train_raw, y_test_raw = train_test_split(
            X_reg, y_reg_log, y_reg_raw, test_size=0.2, random_state=42)

        scaler_r = SS()
        X_train_rs = scaler_r.fit_transform(X_train_r)
        X_test_rs = scaler_r.transform(X_test_r)

        models_reg = {
            "Linear Regression": LinearRegression(),
            "Ridge Regression": Ridge(alpha=1.0),
            "Lasso Regression": Lasso(alpha=0.01, max_iter=5000),
        }

        results_reg = []
        best_r2, best_reg_name = -999, None
        fitted_reg = {}

        for name, model in models_reg.items():
            model.fit(X_train_rs, y_train_r)
            preds_log = model.predict(X_test_rs)
            preds_aed = np.expm1(preds_log)  # back-transform to AED
            fitted_reg[name] = (model, preds_log, preds_aed)
            # R² on log scale (model's native fit quality)
            r2_log = r2_score(y_test_r, preds_log)
            # MAE and RMSE on AED scale (business-interpretable)
            mae_aed = mean_absolute_error(y_test_raw, preds_aed)
            rmse_aed = np.sqrt(mean_squared_error(y_test_raw, preds_aed))
            results_reg.append({"Model": name, "R² (log)": r2_log, "MAE (AED)": mae_aed, "RMSE (AED)": rmse_aed})
            if r2_log > best_r2:
                best_r2, best_reg_name = r2_log, name

        reg_df = pd.DataFrame(results_reg).sort_values("R² (log)", ascending=False)
        st.markdown(f"**Best model: {best_reg_name}** (R² = {best_r2:.4f} on log scale)")
        st.dataframe(reg_df.style.format({"R² (log)": "{:.4f}", "MAE (AED)": "{:.1f}", "RMSE (AED)": "{:.1f}"}),
                     hide_index=True, width="stretch")

        col1, col2 = st.columns(2)
        with col1:
            fig = make_subplots(rows=1, cols=3, subplot_titles=["R² (log)", "MAE (AED)", "RMSE (AED)"])
            for i, metric in enumerate(["R² (log)", "MAE (AED)", "RMSE (AED)"]):
                fig.add_trace(go.Bar(x=reg_df["Model"], y=reg_df[metric], marker_color=PAL[i],
                                     name=metric, showlegend=False), row=1, col=i+1)
            fig.update_layout(title="Regression Model Comparison", height=400)
            # Style subplot title fonts for dark theme
            fig.update_annotations(font=dict(color="#E2E8F0", size=13))
            fmt_chart(fig, 400)
            st.plotly_chart(fig, width="stretch")

        with col2:
            # Actual vs predicted in AED (back-transformed)
            _, _, best_preds_aed = fitted_reg[best_reg_name]
            fig = px.scatter(x=y_test_raw, y=best_preds_aed, opacity=0.5, color_discrete_sequence=[PAL[1]],
                             labels={"x": "Actual Spend (AED)", "y": "Predicted Spend (AED)"})
            max_val = max(y_test_raw.max(), best_preds_aed.max())
            fig.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val], mode="lines",
                                     line=dict(dash="dash", color="grey"), name="Ideal"))
            fig.update_layout(title=f"Actual vs Predicted (AED) — {best_reg_name}")
            fmt_chart(fig, 400)
            st.plotly_chart(fig, width="stretch")

        # Coefficients (on log scale — interpret as % change in spend)
        st.subheader(f"Regression Coefficients — {best_reg_name}")
        st.caption("Coefficients are on the log scale: a +0.1 coefficient ≈ +10% increase in predicted spend.")
        best_reg_model = fitted_reg[best_reg_name][0]
        coef_df = pd.DataFrame({"Feature": reg_features, "Coefficient": best_reg_model.coef_})
        coef_df = coef_df.reindex(coef_df["Coefficient"].abs().sort_values().index)
        fig = px.bar(coef_df, x="Coefficient", y="Feature", orientation="h", color_discrete_sequence=[PAL[0]],
                     text="Coefficient")
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig.update_layout(title=f"Feature Coefficients (Log Scale) — {best_reg_name}")
        fmt_chart(fig, 500)
        st.plotly_chart(fig, width="stretch")

        st.subheader("💼 Business Interpretation — Regression")
        st.markdown(f"""
The **{best_reg_name}** with log-transformed target achieves **R² = {best_r2:.4f}**, a significant improvement over raw-scale regression. Log transformation compresses the right-skewed spend distribution, stabilises variance, and produces more reliable predictions across all spend levels.

**Top spend drivers** (coefficients represent approximate % change in spend):
- **Visit frequency** has the largest positive effect — each step up in visit frequency increases predicted spend by ~{abs(best_reg_model.coef_[3])*100:.0f}%
- **Insurance status** (uninsured) significantly increases out-of-pocket spend
- **Income level** correlates positively — higher earners spend more on healthcare
- **Age** contributes to higher spend (older expats have more health needs)

**Combined with classification insights:**
The most **economically valuable adopters** are those who are both likely to say "Yes" (high digital comfort, dissatisfied, prior telemedicine use) AND are high spenders (frequent visitors, mid-to-high income, uninsured or self-insured). These users have both the **motivation to adopt** and the **budget to monetise** — they should be the **launch priority**.
""")

# ═══════════════════════════════════════════════════════════
# TAB 8 — RECOMMENDATIONS & SUMMARY
# ═══════════════════════════════════════════════════════════
with tabs[7]:
    st.header("Recommendations & Executive Summary")

    st.subheader("🎯 North Star Metric Recap")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div style='background:#132A2E;border:1px solid #0D9488;padding:24px;border-radius:12px;text-align:center'>
        <h1 style='color:#5EEAD4;margin:0'>{yes_pct:.1f}%</h1>
        <p style='color:#99F6E4;font-size:18px;margin:0'>Definite Adopters (Yes)</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style='background:#2A2010;border:1px solid #F59E0B;padding:24px;border-radius:12px;text-align:center'>
        <h1 style='color:#FCD34D;margin:0'>{maybe_pct:.1f}%</h1>
        <p style='color:#FDE68A;font-size:18px;margin:0'>Persuadable (Maybe)</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div style='background:#2A1215;border:1px solid #EF4444;padding:24px;border-radius:12px;text-align:center'>
        <h1 style='color:#FCA5A5;margin:0'>{no_pct:.1f}%</h1>
        <p style='color:#FECACA;font-size:18px;margin:0'>Not Interested (No)</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📌 One Key Insight from Each Analysis Tab")

    insights = [
        ("📋 Data Quality", "Dataset is clean with 2,000 respondents, zero missing values, and outliers treated — ready for reliable analysis."),
        ("👥 Demographics", "25-44 year old South Asian males dominate the respondent base — the app's primary UX should be designed for this core demographic."),
        ("🏥 Healthcare", "High costs (49%), long waits (44%), and language barriers (36%) are the top 3 challenges — these directly map to the app's core value proposition."),
        ("📊 Adoption Drivers", "Dissatisfied, digitally comfortable expats with prior telemedicine experience show the highest adoption intent — satisfaction is the strongest inverse predictor."),
        ("🎯 Segmentation", "K-Means identified distinct personas with adoption rates ranging from low to high — enabling targeted marketing rather than one-size-fits-all."),
        ("🔗 Association Rules", "Language barriers drive demand for multilingual consultations; cost concerns drive insurance checker + e-prescription demand — features should be bundled accordingly."),
        ("🤖 Predictive Models", f"The best classifier achieves F1={best_f1:.3f}; regression confirms frequent visitors and uninsured expats have the highest spend — making them high-value targets."),
    ]
    for icon_label, insight in insights:
        st.markdown(f"**{icon_label}:** {insight}")

    st.markdown("---")
    st.subheader("🚀 5 Actionable Business Recommendations")

    recs = [
        ("1. Launch with a Focused MVP — 4 Core Features",
         "Build virtual consultations (multilingual), specialist referrals & booking, e-prescriptions with delivery, and insurance compatibility checker first. These address the top 3 challenges and are the most commonly co-selected features in association analysis."),
        ("2. Target the 'Digital-Savvy Dissatisfied' Persona First",
         "Clustering and classification both confirm: digitally comfortable expats who are unhappy with current care and have used telemedicine before are the highest-propensity adopters. Focus launch marketing on this segment."),
        ("3. Adopt a Freemium Pricing Model at AED 30-60/month",
         "The 'Free only' group has the lowest adoption intent. A freemium model captures the 'Maybe' group for free while monetising willing payers at AED 31-60/month — the sweet spot where the largest income segment (10K-20K AED) shows willingness to pay."),
        ("4. Offer Free Trial Consultations as the Primary Conversion Lever",
         "Prior telemedicine experience is one of the strongest adoption predictors. Offering one free consultation dramatically increases the probability of converting 'Maybe' respondents to 'Yes' — the 'try it once' effect."),
        ("5. Prioritise Hindi/Urdu, Arabic, and Tagalog Language Support",
         "South Asian and Southeast Asian expats form 60%+ of the respondent base and show high language importance scores. Language barriers are a top-3 challenge — multilingual support is not a nice-to-have but a core differentiator."),
    ]
    for title, desc in recs:
        st.markdown(f"""
<div style='background:#1A2332;border-left:4px solid #0D9488;padding:14px 18px;margin:10px 0;border-radius:6px'>
<b style='color:#5EEAD4;font-size:15px'>{title}</b><br>
<span style='font-size:14px;color:#CBD5E1'>{desc}</span></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📋 Launch Strategy Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**🎯 Target Persona:**
Digitally comfortable, mid-to-high income expats (25-44 years) who are dissatisfied with current healthcare and face cost/language/waiting time challenges.

**🏗 Priority Features (MVP):**
1. Multilingual virtual consultations
2. Specialist referrals & appointment booking
3. E-prescriptions & medication delivery
4. Insurance compatibility checker
""")
    with col2:
        st.markdown("""
**💰 Pricing Strategy:**
Freemium model with a free tier (basic symptom checker + health tips) and premium subscription at AED 30-60/month for consultations, e-prescriptions, and specialist access.

**📢 Go-to-Market Focus:**
1. Partner with large employers for corporate health packages
2. Offer free first consultation as acquisition hook
3. Launch in Hindi/Urdu + English + Arabic first
4. Target social media ads at 25-44 age group in UAE
""")

    st.markdown("---")
    st.caption("Dashboard built for the Telemedicine App Market Intelligence project — UAE Expat Healthcare Survey Analysis")
