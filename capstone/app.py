import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="TikTok Content Performance",
    layout="wide"
)

DATA_PATH = Path(__file__).parent / "data" / "tiktok_performance.csv"
df = pd.read_csv(DATA_PATH)

st.title("📊 TikTok Content Performance Dashboard")
st.caption("Digital Marketing Analytics | Organic Content Performance")


# --------------------------------------------------
# Decision Question
# --------------------------------------------------

st.header("Decision Question")
st.write(
    "ควรปรับสัดส่วน Content Mix อย่างไร "
    "เพื่อเพิ่ม Organic Reach และ Interaction ของคอนเทนต์?"
)


# --------------------------------------------------
# Data Preparation
# --------------------------------------------------

df["post_date"] = pd.to_datetime(
    pd.to_numeric(df["post_date"]),
    unit="D",
    origin="1899-12-30"
)

df["interaction_rate"] = (
    (df["likes"] + df["comments"]) / df["views"]
) * 100


# --------------------------------------------------
# Executive KPIs
# --------------------------------------------------

st.header("Executive KPIs")

# Define comparison periods
baseline_df = df[
    (df["post_date"] >= "2026-03-01") &
    (df["post_date"] <= "2026-05-31")
].copy()

current_df = df[
    (df["post_date"] >= "2026-06-01") &
    (df["post_date"] <= "2026-08-31")
].copy()

# Calculate KPIs
baseline_median_views = baseline_df["views"].median()
current_median_views = current_df["views"].median()

baseline_interaction = baseline_df["interaction_rate"].median()
current_interaction = current_df["interaction_rate"].median()

baseline_posts = len(baseline_df)
current_posts = len(current_df)

baseline_median_interactions = (
    baseline_df["likes"] + baseline_df["comments"]
).median()

current_median_interactions = (
    current_df["likes"] + current_df["comments"]
).median()

# --------------------------------------------------
# Calculate changes
# --------------------------------------------------

views_change = (
    (current_median_views - baseline_median_views)
    / baseline_median_views * 100
)

interaction_change = current_interaction - baseline_interaction

posts_change_pct = (
    (current_posts - baseline_posts)
    / baseline_posts * 100
)

interactions_change = (
    (current_median_interactions - baseline_median_interactions)
    / baseline_median_interactions * 100
)


# --------------------------------------------------
# Display KPI cards
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

# KPI 1: Median Views
c1.metric(
    "Median Views / Post",
    f"{current_median_views:,.0f}",
    f"{views_change:+.1f}%"
)
c1.caption(
    f"Baseline: {baseline_median_views:,.0f}"
)


# KPI 2: Median Interaction Rate
c2.metric(
    "Median Interaction Rate",
    f"{current_interaction:.2f}%",
    f"{interaction_change:+.2f} pp"
)
c2.caption(
    f"Baseline: {baseline_interaction:.2f}%"
)


# KPI 3: Posts Published
c3.metric(
    "Posts Published",
    f"{current_posts:,}",
    f"{posts_change_pct:+.1f}%"
)
c3.caption(
    f"Baseline: {baseline_posts:,} posts"
)


# KPI 4: Median Interactions
c4.metric(
    "Median Interactions / Post",
    f"{current_median_interactions:,.0f}",
    f"{interactions_change:+.1f}%"
)
c4.caption(
    f"Baseline: {baseline_median_interactions:,.0f}"
)


st.caption(
    "Current: Jun–Aug 2026 | Baseline: Mar–May 2026"
    
)
st.info(
    "แม้จำนวนโพสต์ลดลง 16.1% แต่ Median Views / Post เพิ่มขึ้น 10.1% "
    "และ Median Interaction Rate เพิ่มขึ้น 0.86 percentage points "
    "สะท้อนว่า Performance ต่อโพสต์ดีขึ้นเมื่อเทียบกับ Baseline"
)

# --------------------------------------------------
# Evidence
# --------------------------------------------------

st.header("Evidence")

st.subheader("1. Performance by Content Format")

format_summary = (
    df.groupby("format", as_index=False)
      .agg(
          Posts=("post_id", "count"),
          Median_Views=("views", "median"),
          Median_Interaction_Rate=("interaction_rate", "median")
      )
)

fig_format = px.scatter(
    format_summary,
    x="Median_Views",
    y="Median_Interaction_Rate",
    size="Posts",
    hover_name="format",
    text="format",
    title="Reach vs Interaction by Content Format",
    labels={
        "Median_Views": "Median Views / Post",
        "Median_Interaction_Rate": "Median Interaction Rate (%)",
        "Posts": "Number of Posts"
    }
)

fig_format.update_traces(
    textposition="top center"
)

st.plotly_chart(
    fig_format,
    width="stretch"
)

st.caption(
    "ขนาดของวงกลมแสดงจำนวนโพสต์ในแต่ละ Format "
    "ตำแหน่งด้านขวาหมายถึง Median Views สูงกว่า "
    "และตำแหน่งด้านบนหมายถึง Median Interaction Rate สูงกว่า"
)

st.info(
    "Video มี Median Views และ Median Interaction Rate สูงกว่า Carousel "
    "แต่มีจำนวนโพสต์น้อยกว่าอย่างมาก จึงยังควรตีความผลด้วยความระมัดระวัง "
    "และใช้การทดลองเพิ่ม Video เพื่อยืนยันว่า Performance สามารถเกิดซ้ำได้"
)
# --------------------------------------------------
# Evidence 2: Performance by Content Category
# --------------------------------------------------

st.subheader("2. Performance by Content Category")

category_summary = (
    df.groupby("category", as_index=False)
      .agg(
          Posts=("post_id", "count"),
          Median_Views=("views", "median"),
          Median_Interaction_Rate=("interaction_rate", "median")
      )
)

fig_category = px.scatter(
    category_summary,
    x="Median_Views",
    y="Median_Interaction_Rate",
    size="Posts",
    hover_name="category",
    text="category",
    title="Reach vs Interaction by Content Category",
    labels={
        "Median_Views": "Median Views / Post",
        "Median_Interaction_Rate": "Median Interaction Rate (%)",
        "Posts": "Number of Posts"
    }
)

fig_category.update_traces(
    textposition="top center"
)

st.plotly_chart(
    fig_category,
    width="stretch"
)

st.caption(
    "ขนาดของวงกลมแสดงจำนวนโพสต์ในแต่ละ Category "
    "ตำแหน่งด้านขวาหมายถึง Median Views สูงกว่า "
    "และตำแหน่งด้านบนหมายถึง Median Interaction Rate สูงกว่า"
)
# --------------------------------------------------
# Evidence 3: Format × Category Performance
# --------------------------------------------------

st.subheader("3. Performance by Format × Category")

combo_summary = (
    df.groupby(["format", "category"], as_index=False)
      .agg(
          Posts=("post_id", "count"),
          Median_Views=("views", "median"),
          Median_Interaction_Rate=("interaction_rate", "median")
      )
)

combo_summary["Content_Mix"] = (
    combo_summary["format"] + " × " + combo_summary["category"]
)

fig_combo = px.scatter(
    combo_summary,
    x="Median_Views",
    y="Median_Interaction_Rate",
    size="Posts",
    color="format",
    hover_name="Content_Mix",
    hover_data={
        "Posts": True,
        "Median_Views": ":,.0f",
        "Median_Interaction_Rate": ":.2f",
        "format": False,
        "category": False
    },
    text="category",
    title="Reach vs Interaction by Format × Category",
    labels={
        "Median_Views": "Median Views / Post",
        "Median_Interaction_Rate": "Median Interaction Rate (%)",
        "Posts": "Number of Posts",
        "format": "Format"
    }
)

fig_combo.update_traces(
    textposition="top center"
)

st.plotly_chart(
    fig_combo,
    width="stretch"
)

st.caption(
    "แต่ละจุดแทน Format × Category โดยขนาดของวงกลมแสดงจำนวนโพสต์ "
    "ตำแหน่งด้านขวาหมายถึง Median Views สูงกว่า "
    "และตำแหน่งด้านบนหมายถึง Median Interaction Rate สูงกว่า"
)
st.info(
    "Carousel × Daily Phrases มีข้อมูลย้อนหลังรองรับมากที่สุดกลุ่มหนึ่ง "
    "(59 posts) และยังรักษา Performance ในระดับสูง จึงเหมาะเป็น Core Content "
    "ขณะที่ Video × Daily Phrases มี Median Views 1,914 และ Median Interaction Rate 4.90% "
    "สูงกว่า Carousel × Daily Phrases แต่มีเพียง 3 posts "
    "จึงเป็นโอกาสที่ควรนำไปทดลองเพิ่มก่อนปรับ Content Mix ในระยะยาว"
)
# --------------------------------------------------
# Evidence Table: Format × Category
# --------------------------------------------------

st.subheader("Evidence Summary")

evidence_table = combo_summary[
    [
        "format",
        "category",
        "Posts",
        "Median_Views",
        "Median_Interaction_Rate"
    ]
].copy()

evidence_table = evidence_table.rename(
    columns={
        "format": "Format",
        "category": "Category",
        "Median_Views": "Median Views / Post",
        "Median_Interaction_Rate": "Median Interaction Rate (%)"
    }
)

evidence_table["Median Views / Post"] = (
    evidence_table["Median Views / Post"].round(0).astype(int)
)

evidence_table["Median Interaction Rate (%)"] = (
    evidence_table["Median Interaction Rate (%)"].round(2)
)

evidence_table = evidence_table.sort_values(
    by="Median Views / Post",
    ascending=False
)

st.dataframe(
    evidence_table,
    width="stretch",
    hide_index=True
)
# --------------------------------------------------
# Recommendation
# --------------------------------------------------

st.header("Recommendation")

st.markdown("""
**1. Maintain — รักษา Core Content**  
รักษา **Carousel × Daily Phrases** เป็น Core Content เนื่องจากมี Performance ที่ดี
และมีข้อมูลย้อนหลังรองรับจำนวนมาก (**59 posts**)

**2. Test — ทดลองเพิ่ม Video**  
ทดลองเพิ่ม **Video × Daily Phrases** เนื่องจากมี Median Views **1,914**
และ Median Interaction Rate **4.90%** ซึ่งสูงกว่า Carousel × Daily Phrases
แต่ปัจจุบันมีข้อมูลเพียง **3 posts**

**3. Decide — ประเมินก่อนปรับ Content Mix**  
หลังการทดลอง ให้เปรียบเทียบ Performance ของ Video กับ Baseline
ก่อนตัดสินใจว่าจะเพิ่มสัดส่วน Video ใน Content Mix รอบถัดไปหรือไม่
""")

# --------------------------------------------------
# Action Plan
# --------------------------------------------------

st.header("Action Plan")

action_plan = pd.DataFrame({
    "Action": [
        "รักษา Carousel × Daily Phrases",
        "ทดลอง Video × Daily Phrases"
    ],
    "Owner": [
        "Content Creator",
        "Content Creator"
    ],
    "Timeline": [
        "14 วัน",
        "14 วัน"
    ],
    "KPI": [
        "Median Views / Interaction Rate",
        "Median Views / Interaction Rate"
    ],
    "Baseline": [
        "996 Views / 3.71%",
        "996 Views / 3.71%"
    ],
    "Target": [
        "≥ 6 posts | Views ≥ 996 | IR ≥ 3.71%",
        "≥ 6 posts | Views ≥ 996 | IR ≥ 3.71%"
    ],
    "Expected Impact": [
        "รักษา Organic Performance",
        "ประเมินศักยภาพ Video เพื่อปรับ Content Mix"
    ]
})

st.dataframe(
    action_plan,
    width="stretch",
    hide_index=True,
    column_config={
        "Action": st.column_config.TextColumn(
            "Action",
            width="medium"
        ),
        "Owner": st.column_config.TextColumn(
            "Owner",
            width="medium"
        ),
        "Timeline": st.column_config.TextColumn(
            "Timeline",
            width="small"
        ),
        "KPI": st.column_config.TextColumn(
            "KPI",
            width="medium"
        ),
        "Baseline": st.column_config.TextColumn(
            "Baseline",
            width="medium"
        ),
        "Target": st.column_config.TextColumn(
            "Target",
            width="medium"
        ),
        "Expected Impact": st.column_config.TextColumn(
            "Expected Impact",
            width="large"
        )
    }
)

st.caption(
    "Pilot Design: 14 วัน | Daily Phrases 12 posts "
    "(Carousel 6 + Video 6) เพื่อเปรียบเทียบ Performance ในช่วงเวลาเดียวกัน"
)
# --------------------------------------------------
# Decision Rule
# --------------------------------------------------

st.header("Decision Rule")

st.write(
    "หลังจบการทดลอง 14 วัน จะเปรียบเทียบ Video × Daily Phrases "
    "กับ Baseline ของ Carousel × Daily Phrases"
)

st.markdown("""
- **Consider Increasing Video** — หาก Video มี Median Views ≥ 996 และ Interaction Rate ≥ 3.71%
- **Maintain Current Mix** — หาก Video ยังไม่สามารถรักษา Performance ได้ถึง Baseline
- **Continue Testing** — หากผลยังไม่ชัดเจนหรือมีความผันผวนสูง
""")