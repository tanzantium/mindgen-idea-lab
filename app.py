
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Mind Genomics Idea Laboratory",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧪 Mind Genomics Idea Laboratory")
st.markdown("""Design ideas not by guessing — but by toggling truths.
Explore which minds respond to which cues, and why.""")

# ------------------------------
# CUE SETUP
# ------------------------------
cues = {
    "Nature’s Cleanse": "nature_cleanse",
    "Cosy Calm": "cosy_calm",
    "Fresh Vitality": "fresh_vitality",
    "Clean Wear": "clean_wear",
    "Sweat Away": "sweat_away",
    "Plant Pure": "plant_pure",
    "Touch Smooth": "touch_smooth",
    "Care Night": "care_night",
    "Breathe Air": "breathe_air"
}

st.sidebar.header("🔘 Toggle Cues")
active_cues = []
cue_state = {}

# Check if a scenario is loaded and apply it
selected_scenario = st.sidebar.selectbox("▶ Load saved scenario:", ["None"] + 
    (pd.read_csv("scenarios.csv")["name"].tolist() if os.path.exists("scenarios.csv") else []))

scenario_loaded = []
if selected_scenario != "None":
    df = pd.read_csv("scenarios.csv")
    scenario_loaded = df[df["name"] == selected_scenario]["cues"].values[0].split(",")

# Cue checkboxes
for label, var in cues.items():
    checked = var in scenario_loaded
    state = st.sidebar.checkbox(label, value=checked)
    cue_state[var] = state
    if state:
        active_cues.append(var)

# ------------------------------
# COEFFICIENTS & SCORING
# ------------------------------
coefficients = {
    "Cluster 1": [6, 19, 11, 4, 5, 10, 5, 4, 7],
    "Cluster 2": [16, 12, 14, 5, 6, 14, 6, 6, 11],
    "Cluster 3": [-42, -9, -1, 0, -3, 2, -2, -1, 0]
}

cue_indices = {name: idx for idx, name in enumerate(cues.values())}
scores = {}
for cluster, weights in coefficients.items():
    score = sum([weights[cue_indices[cue]] for cue in active_cues])
    scores[cluster] = score

def interpret(cluster, score):
    if score >= 50:
        return "💥 Strong Activation — Build for this Mindset"
    elif score >= 20:
        return "✅ Moderate Activation — Test and Learn"
    elif score >= 0:
        return "⚠️ Low Signal — Weak Fit"
    else:
        return "🚫 Negative Activation — Avoid"

col1, col2 = st.columns([2, 3])
with col1:
    st.subheader("🧍 Who You’ve Activated")
    for cluster in scores:
        st.markdown(f"### {cluster}")
        st.markdown(f"**Score:** {scores[cluster]}")
        st.markdown(f"{interpret(cluster, scores[cluster])}")
        if cluster == "Cluster 1":
            st.info("🧬 Female-leaning, open to aluminum-free, prefers clean + natural cues")
        elif cluster == "Cluster 2":
            st.info("🧬 Males, heavy sweaters, prefer performance and comfort themes")
        elif cluster == "Cluster 3":
            st.info("🧬 Minimalist mindsets, sensitive to over-claim or over-scent")

with col2:
    st.subheader("🧭 Strategic Prompt")
    if "nature_cleanse" in active_cues and "clean_wear" in active_cues:
        st.success("📦 Strategy: Botanical + Clinical Clean — ideal for aluminum-free messaging")
    if "cosy_calm" in active_cues and "plant_pure" in active_cues:
        st.success("📦 Strategy: Cozy comfort + natural care — digital-first channel testing")
    if len(active_cues) >= 4:
        st.info("💡 Consider AB testing this cue bundle with 2 personas")

# ------------------------------
# SCENARIO SAVE
# ------------------------------
st.sidebar.markdown("---")
scenario_name = st.sidebar.text_input("Save this configuration as:")
if st.sidebar.button("💾 Save Scenario"):
    cue_string = ",".join(active_cues)
    df_new = pd.DataFrame([[scenario_name, cue_string]], columns=["name", "cues"])
    if os.path.exists("scenarios.csv"):
        df_existing = pd.read_csv("scenarios.csv")
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.drop_duplicates(subset="name", keep="last").to_csv("scenarios.csv", index=False)
    st.sidebar.success(f"Scenario '{scenario_name}' saved ✅")
