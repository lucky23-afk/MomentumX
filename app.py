import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="MomentumX",
    page_icon="🏎️",
    layout="wide"
)

# --------------------------------------------------
# Styling
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0b0f14;
}

.main-title {
    font-size: 48px;
    font-weight: 700;
    color: white;
    margin-bottom: 0;
}

.subtitle {
    font-size: 18px;
    color: #9ca3af;
    margin-top: 0;
}

.card {
    background-color: #151b23;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #26303d;
}

.decision {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    padding: 25px;
    border-radius: 15px;
    margin-top: 10px;
}

.small-text {
    color: #9ca3af;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown('<p class="main-title">MomentumX</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">AI Powered Motorsport Energy and Overtake Decision Support</p>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# Sidebar inputs
# --------------------------------------------------

st.sidebar.header("Race Conditions")

battery = st.sidebar.slider(
    "Battery Level",
    0,
    100,
    65
)

gap = st.sidebar.slider(
    "Gap to Car Ahead",
    0.1,
    5.0,
    1.0,
    0.1
)

speed_advantage = st.sidebar.slider(
    "Relative Speed Advantage",
    -20,
    30,
    10
)

remaining_laps = st.sidebar.slider(
    "Remaining Laps",
    1,
    70,
    20
)

tyre_condition = st.sidebar.selectbox(
    "Tyre Condition",
    ["Good", "Medium", "Poor"]
)

track_position = st.sidebar.selectbox(
    "Track Position",
    ["Overtaking Zone", "Normal Zone", "Low Opportunity Zone"]
)

# --------------------------------------------------
# Scoring logic
# This can later be replaced with a trained ML model
# --------------------------------------------------

tyre_score = {
    "Good": 100,
    "Medium": 65,
    "Poor": 30
}[tyre_condition]

track_score = {
    "Overtaking Zone": 100,
    "Normal Zone": 60,
    "Low Opportunity Zone": 25
}[track_position]

# Overtake probability

gap_score = max(0, 100 - gap * 20)
speed_score = min(100, max(0, 50 + speed_advantage * 2.5))

overtake_probability = (
    0.30 * gap_score +
    0.30 * speed_score +
    0.20 * tyre_score +
    0.20 * track_score
)

overtake_probability = max(
    0,
    min(100, overtake_probability)
)

# Energy opportunity

energy_score = battery

# Race management score
race_management = max(
    0,
    min(100, 100 - remaining_laps * 1.2)
)

# --------------------------------------------------
# Decision engine
# --------------------------------------------------

attack_score = (
    battery * 0.35 +
    overtake_probability * 0.45 +
    speed_score * 0.20
)

save_score = (
    (100 - battery) * 0.55 +
    remaining_laps * 1.2 +
    (100 - overtake_probability) * 0.20
)

balanced_score = 100 - abs(attack_score - save_score)

if attack_score > 70 and overtake_probability > 60:
    decision = "Attack"
    decision_message = "Strong overtaking opportunity detected. Energy deployment is recommended."
    decision_color = "#22c55e"

elif save_score > 70:
    decision = "Save"
    decision_message = "Energy conservation is recommended for better long term race performance."
    decision_color = "#ef4444"

else:
    decision = "Balanced"
    decision_message = "Maintain current pace and wait for a stronger overtaking opportunity."
    decision_color = "#f59e0b"

# Confidence score

scores = sorted(
    [attack_score, balanced_score, save_score],
    reverse=True
)

confidence = min(
    95,
    max(55, 55 + (scores[0] - scores[1]) * 1.5)
)

# --------------------------------------------------
# Top metrics
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Battery",
    f"{battery}%"
)

col2.metric(
    "Overtake Probability",
    f"{overtake_probability:.0f}%"
)

col3.metric(
    "Decision Confidence",
    f"{confidence:.0f}%"
)

col4.metric(
    "Race Stage",
    f"{remaining_laps} laps left"
)

st.divider()

# --------------------------------------------------
# Main section
# --------------------------------------------------

left, right = st.columns([1, 1])

with left:

    st.subheader("Strategy Recommendation")

    st.markdown(
        f"""
        <div class="decision" style="
        background-color: {decision_color}20;
        border: 2px solid {decision_color};
        color: {decision_color};
        ">
        {decision}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.info(decision_message)

    st.markdown("### Decision Modes")

    mode1, mode2, mode3 = st.columns(3)

    with mode1:
        if decision == "Attack":
            st.success("Attack")
        else:
            st.write("Attack")

    with mode2:
        if decision == "Balanced":
            st.warning("Balanced")
        else:
            st.write("Balanced")

    with mode3:
        if decision == "Save":
            st.error("Save")
        else:
            st.write("Save")

    st.markdown("### Why this decision?")

    reasons = []

    if battery >= 60:
        reasons.append("Strong battery availability supports energy deployment")
    else:
        reasons.append("Battery level should be managed carefully")

    if gap <= 1.5:
        reasons.append("The gap to the car ahead creates a possible overtaking opportunity")
    else:
        reasons.append("The gap to the car ahead reduces the immediate overtaking opportunity")

    if speed_advantage > 5:
        reasons.append("Positive speed advantage improves overtaking potential")
    else:
        reasons.append("Limited speed advantage increases the risk of an overtake")

    for reason in reasons:
        st.write("• " + reason)

# --------------------------------------------------
# Right side charts
# --------------------------------------------------

with right:

    st.subheader("Race Intelligence")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=overtake_probability,
            title={"text": "Overtake Opportunity"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": decision_color},
                "steps": [
                    {"range": [0, 35], "color": "#2a2f38"},
                    {"range": [35, 65], "color": "#343a45"},
                    {"range": [65, 100], "color": "#3d4652"}
                ]
            }
        )
    )

    fig.update_layout(
        height=300,
        paper_bgcolor="#151b23",
        font={"color": "white"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Strategy Score Comparison")

    score_data = pd.DataFrame({
        "Strategy": ["Attack", "Balanced", "Save"],
        "Score": [
            round(attack_score, 1),
            round(balanced_score, 1),
            round(save_score, 1)
        ]
    })

    fig2 = go.Figure(
        go.Bar(
            x=score_data["Strategy"],
            y=score_data["Score"],
            marker_color=[
                "#22c55e",
                "#f59e0b",
                "#ef4444"
            ]
        )
    )

    fig2.update_layout(
        height=280,
        paper_bgcolor="#151b23",
        plot_bgcolor="#151b23",
        font={"color": "white"},
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# --------------------------------------------------
# Telemetry chart
# --------------------------------------------------

st.divider()
st.subheader("Simulated Race Telemetry")

laps = np.arange(1, 21)

simulated_battery = np.clip(
    battery - laps * 1.5 + np.random.normal(0, 2, 20),
    0,
    100
)

simulated_gap = np.clip(
    gap + np.sin(laps / 2) * 0.5 +
    np.random.normal(0, 0.15, 20),
    0.1,
    5
)

telemetry = go.Figure()

telemetry.add_trace(
    go.Scatter(
        x=laps,
        y=simulated_battery,
        mode="lines+markers",
        name="Battery Level"
    )
)

telemetry.add_trace(
    go.Scatter(
        x=laps,
        y=simulated_gap * 20,
        mode="lines",
        name="Gap Trend"
    )
)

telemetry.update_layout(
    xaxis_title="Race Simulation Step",
    yaxis_title="Telemetry Value",
    paper_bgcolor="#151b23",
    plot_bgcolor="#151b23",
    font={"color": "white"},
    height=400
)

st.plotly_chart(
    telemetry,
    use_container_width=True
)

# --------------------------------------------------
# Final summary
# --------------------------------------------------

st.divider()

st.subheader("MomentumX Decision Summary")

st.write(
    f"""
    Based on the current race conditions, MomentumX recommends the
    **{decision}** strategy with a decision confidence of
    **{confidence:.0f}%**.
    """
)

st.caption(
    "Prototype demonstration using simulated decision logic and telemetry data. "
    "A trained machine learning model can replace the decision logic in future development."
)