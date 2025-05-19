
import streamlit as st

st.set_page_config(
    page_title="Mind Genomics Idea Laboratory",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧪 Mind Genomics Idea Laboratory")
st.markdown("""
Design ideas not by guessing — but by toggling truths.
Explore which minds respond to which cues, and why.
""")

# Cue setup
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
for label, var in cues.items():
    if st.sidebar.checkbox(label):
        active_cues.append(var)

# Coefficients
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
        st.success("📦 Strategy: Position this combo as Botanical + Clinical Clean — ideal for aluminum-free messaging")
    if "cosy_calm" in active_cues and "plant_pure" in active_cues:
        st.success("📦 Strategy: Use cozy comfort + natural care — suitable for calming narratives on digital channels")
    if len(active_cues) >= 4:
        st.info("💡 Consider testing this cue bundle in a targeted AB test across 2 personas")

st.sidebar.markdown("---")
scenario_name = st.sidebar.text_input("Save this configuration as:")
if st.sidebar.button("💾 Save Scenario"):
    st.sidebar.success(f"Scenario '{scenario_name}' saved (not persistent in demo)")
