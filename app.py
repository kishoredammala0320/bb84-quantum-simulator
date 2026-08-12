import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from main import simulate_bb84 

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="BB84 Quantum Laboratory Console",
    layout="wide",
    page_icon="⚛️",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"
if 'results' not in st.session_state:
    st.session_state.results = None
if 'status' not in st.session_state:
    st.session_state.status = "IDLE"

# --- LIGHT THEME + ANIMATED SVG MINIATURE STYLES ---
def apply_custom_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Fira+Code:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    color: #0f172a !important;
}

.stApp {
    background-color: #f8fafc;
}

/* --- SVG VECTOR ANIMATIONS --- */
@keyframes pulse-emitter {
    0% { r: 6px; opacity: 0.8; }
    50% { r: 16px; opacity: 0.2; }
    100% { r: 6px; opacity: 0.8; }
}

@keyframes laser-beam-pulse {
    0% { opacity: 0.4; stroke-width: 2; }
    50% { opacity: 1; stroke-width: 4; }
    100% { opacity: 0.4; stroke-width: 2; }
}

@keyframes eve-scan-rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes eve-probe-move {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-4px); }
    100% { transform: translateY(0px); }
}

@keyframes bob-wave-expand {
    0% { opacity: 1; transform: scale(0.6); transform-origin: center; }
    100% { opacity: 0; transform: scale(1.4); transform-origin: center; }
}

@keyframes photon-travel {
    0% { left: 0%; opacity: 0; }
    20% { opacity: 1; }
    80% { opacity: 1; }
    100% { left: 90%; opacity: 0; }
}

@keyframes warning-pulse {
    0% { box-shadow: 0 0 5px rgba(220, 38, 38, 0.2); }
    100% { box-shadow: 0 0 20px rgba(220, 38, 38, 0.5); }
}

.svg-pulse-ring { animation: pulse-emitter 2s infinite ease-in-out; }
.svg-laser-line { animation: laser-beam-pulse 1.5s infinite ease-in-out; }
.svg-scan-hand { transform-origin: 50px 50px; animation: eve-scan-rotate 3s linear infinite; }
.svg-eve-container { animation: eve-probe-move 2s ease-in-out infinite; }
.svg-wave-ring { animation: bob-wave-expand 2s ease-out infinite; }

/* --- STREAMLIT TABS --- */
.stTabs [data-baseweb="tab-list"] button {
    color: #475569 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    color: #0284c7 !important;
    border-bottom-color: #0284c7 !important;
}

/* --- BUTTON STYLING & HOVER --- */
.stButton > button {
    background: #0284c7 !important;
    color: #ffffff !important;
    border: 2px solid #0369a1 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 10px 20px !important;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.2) !important;
    transition: all 0.2s ease-in-out !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #0369a1 !important;
    color: #ffffff !important;
    border-color: #075985 !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4) !important;
    transform: translateY(-2px) !important;
}

div.stButton > button[key="eve_btn"] {
    background: #dc2626 !important;
    border-color: #b91c1c !important;
    box-shadow: 0 2px 8px rgba(220, 38, 38, 0.2) !important;
}

div.stButton > button[key="eve_btn"]:hover {
    background: #b91c1c !important;
    color: #ffffff !important;
    border-color: #7f1d1d !important;
    box-shadow: 0 4px 14px rgba(220, 38, 38, 0.4) !important;
}

/* --- NODE CARDS --- */
.node-card {
    border-radius: 16px;
    padding: 22px;
    background: #ffffff;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
    transition: all 0.3s ease;
    text-align: center;
}

.alice-card {
    border: 2px solid #0284c7;
}

.eve-card-idle {
    border: 2px dashed #94a3b8;
}

.eve-card-active {
    border: 2px solid #dc2626;
    box-shadow: 0 0 20px rgba(220, 38, 38, 0.25);
    animation: warning-pulse 1.5s infinite alternate;
}

.bob-card {
    border: 2px solid #7e22ce;
}

.node-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.badge-alice { background: #e0f2fe; color: #0369a1; border: 1px solid #38bdf8; }
.badge-eve-off { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
.badge-eve-on { background: #fee2e2; color: #b91c1c; border: 1px solid #f87171; }
.badge-bob { background: #f3e8ff; color: #6b21a8; border: 1px solid #c084fc; }

/* --- QUANTUM BEAM ANIMATION --- */
.beam-container {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 20px 0;
    position: relative;
}

.beam-line {
    width: 100%;
    height: 6px;
    border-radius: 3px;
    position: relative;
}

.beam-secure {
    background: #0284c7;
}

.beam-compromised {
    background: #dc2626;
}

.flying-qubit {
    position: absolute;
    top: -10px;
    animation: photon-travel 1.4s infinite linear;
}

/* --- BIT REGISTER CARDS --- */
.bit-register-box {
    background: #ffffff;
    border: 2px solid #cbd5e1;
    border-radius: 14px;
    padding: 20px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.bit-chip {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    background: #f1f5f9;
    border: 2px solid #0284c7;
    border-radius: 10px;
    padding: 10px 16px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.bit-chip-otp {
    background: #e0f2fe !important;
    border: 2px solid #0284c7 !important;
}

.bit-chip:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);
}

.bit-value {
    font-family: 'Fira Code', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: #0369a1;
}

.bit-label {
    font-size: 0.7rem;
    color: #475569;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* --- METRIC CARDS --- */
.stat-card {
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.stat-value-safe { color: #16a34a; font-size: 2.2rem; font-weight: 700; }
.stat-value-danger { color: #dc2626; font-size: 2.2rem; font-weight: 700; }

/* --- GATEWAY CARD --- */
.gateway-card {
    background: #ffffff;
    border: 2px solid #0284c7;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(2, 132, 199, 0.12);
}
</style>
""", unsafe_allow_html=True)

# --- DASHBOARD PAGE ---
def show_dashboard():
    st.markdown("""
<div style="text-align: center; padding: 10px 0 25px 0;">
    <h1 style="color: #0f172a; font-weight: 700; margin: 0; font-size: 2.3rem;">⚛️ BB84 QUANTUM KEY EXCHANGE CONSOLE</h1>
    <p style="color: #475569; font-size: 1.05rem; margin-top: 6px;">Interactive Simulation Node: Alice (Transmitter) ➔ Eve (Interception) ➔ Bob (Receiver)</p>
</div>
""", unsafe_allow_html=True)

    # 1. THREE-NODE CONSOLE (ALICE - EVE - BOB)
    col_alice, col_beam1, col_eve, col_beam2, col_bob = st.columns([2.5, 1, 2.5, 1, 2.5])

    # --- ALICE CARD ---
    with col_alice:
        alice_svg = """<div style="display: flex; justify-content: center; margin: 10px 0;">
    <svg width="90" height="90" viewBox="0 0 100 100">
        <rect x="20" y="35" width="60" height="45" rx="8" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
        <rect x="28" y="43" width="44" height="20" rx="4" fill="#0f172a"/>
        <circle cx="50" cy="53" r="6" fill="#0284c7"/>
        <circle cx="50" cy="53" r="10" fill="none" stroke="#38bdf8" stroke-width="2" class="svg-pulse-ring"/>
        <path d="M 50 20 L 50 35" stroke="#0284c7" stroke-width="3" stroke-dasharray="2,2" class="svg-laser-line"/>
        <circle cx="50" cy="18" r="4" fill="#38bdf8"/>
        <circle cx="70" cy="70" r="3" fill="#16a34a"/>
    </svg>
</div>"""

        st.markdown(f"""<div class="node-card alice-card">
<span class="node-badge badge-alice">Node A: Alice (Sender)</span>
{alice_svg}
<h3 style="color: #0284c7; margin: 0 0 8px 0;">📡 Quantum Transmitter</h3>
<p style="color: #475569; font-size: 0.88rem;">Broadcasting polarized photon bit states (+ / X bases).</p>
</div>""", unsafe_allow_html=True)
        
        st.write("")
        num_qubits = st.slider("Photons to Transmit", 20, 100, 40, step=10, key="num_qubits")
        if st.button("🚀 TRANSMIT FROM ALICE"):
            with st.spinner("Alice transmitting quantum states..."):
                time.sleep(0.3)
                res = simulate_bb84(num_qubits, False)
                st.session_state.results = res
                st.session_state.status = "SECURE"
                st.toast("🔒 Secure Key Exchange Completed!", icon="✅")
                st.rerun()

    # --- BEAM 1 ---
    with col_beam1:
        beam_style = "beam-compromised" if st.session_state.status == "COMPROMISED" else "beam-secure"
        qubit_color = "#dc2626" if st.session_state.status == "COMPROMISED" else "#0284c7"
        qubit_svg = f"""<svg width="24" height="24" viewBox="0 0 30 30" class="flying-qubit">
    <circle cx="15" cy="15" r="7" fill="{qubit_color}"/>
    <circle cx="15" cy="15" r="12" fill="none" stroke="{qubit_color}" stroke-width="2" stroke-dasharray="3,3"/>
</svg>"""

        st.markdown(f"""<div class="beam-container">
<div class="beam-line {beam_style}">
    {qubit_svg}
</div>
</div>""", unsafe_allow_html=True)

    # --- EVE CARD ---
    with col_eve:
        eve_style = "eve-card-active" if st.session_state.status == "COMPROMISED" else "eve-card-idle"
        badge_style = "badge-eve-on" if st.session_state.status == "COMPROMISED" else "badge-eve-off"
        badge_text = "🚨 EVE ACTIVE" if st.session_state.status == "COMPROMISED" else "👁️ EVE PASSIVE"
        
        scan_color = "#dc2626" if st.session_state.status == "COMPROMISED" else "#64748b"
        eve_svg = f"""<div style="display: flex; justify-content: center; margin: 10px 0;" class="svg-eve-container">
    <svg width="90" height="90" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="36" fill="#f8fafc" stroke="{scan_color}" stroke-width="2"/>
        <circle cx="50" cy="50" r="24" fill="none" stroke="{scan_color}" stroke-width="1" stroke-dasharray="4,4"/>
        <circle cx="50" cy="50" r="12" fill="none" stroke="{scan_color}" stroke-width="1"/>
        <line x1="14" y1="50" x2="86" y2="50" stroke="{scan_color}" stroke-width="1"/>
        <line x1="50" y1="14" x2="50" y2="86" stroke="{scan_color}" stroke-width="1"/>
        <g class="svg-scan-hand">
            <line x1="50" y1="50" x2="50" y2="14" stroke="{scan_color}" stroke-width="3"/>
            <polygon points="50,50 35,18 50,14" fill="{scan_color}" opacity="0.25"/>
        </g>
        <circle cx="50" cy="50" r="5" fill="{scan_color}"/>
    </svg>
</div>"""

        st.markdown(f"""<div class="node-card {eve_style}">
<span class="node-badge {badge_style}">{badge_text}</span>
{eve_svg}
<h3 style="color: #dc2626; margin: 0 0 8px 0;">👁️ Intercepting Node</h3>
<p style="color: #475569; font-size: 0.88rem;">Secretly eavesdropping & collapsing qubit wavefunctions.</p>
</div>""", unsafe_allow_html=True)
        
        st.write("")
        if st.button("🚨 TRIGGER EVE INTERCEPTION", key="eve_btn"):
            with st.spinner("Eve eavesdropping on fiber channel..."):
                time.sleep(0.3)
                st.session_state.results = simulate_bb84(num_qubits, True)
                st.session_state.status = "COMPROMISED"
                st.rerun()

    # --- BEAM 2 ---
    with col_beam2:
        st.markdown(f"""<div class="beam-container">
<div class="beam-line {beam_style}">
    {qubit_svg}
</div>
</div>""", unsafe_allow_html=True)

    # --- BOB CARD ---
    with col_bob:
        bob_svg = """<div style="display: flex; justify-content: center; margin: 10px 0;">
    <svg width="90" height="90" viewBox="0 0 100 100">
        <path d="M 30 75 L 70 75 L 60 60 L 40 60 Z" fill="#7e22ce"/>
        <path d="M 20 45 A 32 32 0 0 0 80 45 Z" fill="#f3e8ff" stroke="#7e22ce" stroke-width="3"/>
        <line x1="50" y1="45" x2="50" y2="30" stroke="#7e22ce" stroke-width="3"/>
        <circle cx="50" cy="28" r="4" fill="#a855f7"/>
        <circle cx="50" cy="28" r="10" fill="none" stroke="#c084fc" stroke-width="2" class="svg-wave-ring"/>
        <circle cx="50" cy="28" r="18" fill="none" stroke="#a855f7" stroke-width="1.5" class="svg-wave-ring" style="animation-delay: 0.5s;"/>
    </svg>
</div>"""

        st.markdown(f"""<div class="node-card bob-card">
<span class="node-badge badge-bob">Node B: Bob (Receiver)</span>
{bob_svg}
<h3 style="color: #7e22ce; margin: 0 0 8px 0;">🔬 Quantum Detector</h3>
<p style="color: #475569; font-size: 0.88rem;">Listening and measuring incoming photon filter bases.</p>
</div>""", unsafe_allow_html=True)
        
        st.write("")
        if st.session_state.results:
            st.success("✅ Quantum States Received")
        else:
            st.info("⏳ Waiting for Transmission")

    st.divider()

    # 2. RESULTS & METRICS DISPLAY
    if st.session_state.results:
        a_key, b_key, qber, alice_bits, a_bases, b_bases = st.session_state.results

        # TELEMETRY CARDS
        m1, m2, m3 = st.columns(3)
        with m1:
            val_class = "stat-value-danger" if qber >= 0.15 else "stat-value-safe"
            st.markdown(f"""<div class="stat-card">
<div style="color: #475569; font-size: 0.85rem; font-weight: 700; text-transform: uppercase;">Quantum Bit Error Rate (QBER)</div>
<div class="{val_class}">{qber:.1%}</div>
<div style="color: #64748b; font-size: 0.8rem;">Allowed Tolerance: < 15.0%</div>
</div>""", unsafe_allow_html=True)

        with m2:
            st.markdown(f"""<div class="stat-card">
<div style="color: #475569; font-size: 0.85rem; font-weight: 700; text-transform: uppercase;">Sifted Key Entropy</div>
<div style="color: #0284c7; font-size: 2.2rem; font-weight: 700;">{len(a_key)} Bits</div>
<div style="color: #64748b; font-size: 0.8rem;">Reconciled Bases</div>
</div>""", unsafe_allow_html=True)

        with m3:
            status_color = "#dc2626" if st.session_state.status == "COMPROMISED" else "#16a34a"
            st.markdown(f"""<div class="stat-card">
<div style="color: #475569; font-size: 0.85rem; font-weight: 700; text-transform: uppercase;">Link Integrity Status</div>
<div style="color: {status_color}; font-size: 2.2rem; font-weight: 700;">{st.session_state.status}</div>
<div style="color: #64748b; font-size: 0.8rem;">Channel Monitor</div>
</div>""", unsafe_allow_html=True)

        st.write("")

        # 3. SHARED SECRET OTP REGISTERS
        st.subheader("🔑 Shared Secret One-Time Pad (Sifted Key Register)")
        if len(a_key) >= 8:
            otp_str = "".join(map(str, a_key[:8]))
            st.info(f"💡 **Generated 8-Bit Quantum OTP Code:** `{otp_str}` (Use this code to log into the Gateway below)")
            
            slots_html = ""
            for i, b in enumerate(a_key[:20]):
                chip_class = "bit-chip bit-chip-otp" if i < 8 else "bit-chip"
                label = f"OTP #{i+1}" if i < 8 else f"BIT #{i+1}"
                slots_html += f'<div class="{chip_class}"><span class="bit-value">{b}</span><span class="bit-label">{label}</span></div>'
            
            st.markdown(f'<div class="bit-register-box">{slots_html}</div>', unsafe_allow_html=True)
        elif len(a_key) > 0:
            otp_str = "".join(map(str, a_key))
            st.info(f"💡 **Generated Quantum OTP Code:** `{otp_str}`")
        else:
            st.warning("All bits discarded during basis sifting.")

        st.write("")

        # 4. ACTION BUTTON TO PROCEED TO GATEWAY
        if st.session_state.status == "SECURE":
            if st.button("🔐 PROCEED TO SECURE LOGIN GATEWAY ➔"):
                st.session_state.page = "login"
                st.rerun()

        st.write("")

        # 5. HIGH-CONTRAST LIGHT GRAPHICAL CHARTS & TELEMETRY
        tab1, tab2 = st.tabs(["📊 Fidelity Analysis", "📜 Alice ➔ Bob Telemetry Log"])

        with tab1:
            matching = sum(1 for i in range(min(len(a_key), len(b_key))) if a_key[i] == b_key[i])
            fig = go.Figure(data=[
                go.Bar(
                    x=['Alice Transmitted Key', 'Bob Received Key', 'Verified Bit Match'],
                    y=[len(a_key), len(b_key), matching],
                    text=[len(a_key), len(b_key), matching],
                    textposition='outside',
                    textfont=dict(color='#0f172a', size=15, family="Space Grotesk"),
                    marker=dict(
                        color=['#0284c7', '#7e22ce', '#16a34a' if qber < 0.15 else '#dc2626'],
                        line=dict(color='#0f172a', width=1.5)
                    )
                )
            ])
            fig.update_layout(
                title=dict(text="Qubit Reconciliation & Key Fidelity", font=dict(color="#0f172a", size=18, family="Space Grotesk")),
                height=380,
                paper_bgcolor='#ffffff',
                plot_bgcolor='#f1f5f9',
                font=dict(color="#0f172a", size=14, family="Space Grotesk"),
                xaxis=dict(
                    gridcolor='#cbd5e1',
                    tickfont=dict(color="#0f172a", size=14, family="Space Grotesk")
                ),
                yaxis=dict(
                    gridcolor='#cbd5e1',
                    title=dict(text="Bit Count", font=dict(color="#0f172a", size=14)),
                    tickfont=dict(color="#0f172a", size=12)
                ),
                margin=dict(l=40, r=40, t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            display_count = min(12, len(alice_bits))
            sifted_idx = 0
            key_bit_col = []
            for i in range(display_count):
                if a_bases[i] == b_bases[i]:
                    if sifted_idx < len(a_key):
                        key_bit_col.append(str(a_key[sifted_idx]))
                        sifted_idx += 1
                    else:
                        key_bit_col.append("-")
                else:
                    key_bit_col.append("-")

            df = pd.DataFrame({
                "Photon Slot": [f"Photon #{i+1}" for i in range(display_count)],
                "Alice Bit": [alice_bits[i] for i in range(display_count)],
                "Alice Basis": ["Rectilinear (+)" if b==0 else "Diagonal (X)" for b in a_bases[:display_count]],
                "Bob Basis": ["Rectilinear (+)" if b==0 else "Diagonal (X)" for b in b_bases[:display_count]],
                "Basis Reconciliation": ["✅ Match" if a_bases[i]==b_bases[i] else "❌ Discard" for i in range(display_count)],
                "Resulting Key Bit": key_bit_col
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

        if qber >= 0.15:
            st.error("🚨 SECURITY BREACH DETECTED: Eavesdropper collapsed quantum states! Access to Gateway is locked.")


# --- SECURE LOGIN PAGE WITH ANIMATED AUTHENTICATION FORM ---
# --- SECURE LOGIN PAGE WITH ANIMATED AUTHENTICATION FORM ---
def show_login_page():
    # Retrieve OTP generated from transmission
    if st.session_state.results and len(st.session_state.results[0]) > 0:
        a_key = st.session_state.results[0]
        expected_otp = "".join(map(str, a_key[:8]))
    else:
        expected_otp = "10110100"

    # CSS for Animated Shield & Sleek Portal Form
    st.markdown("""
<style>
@keyframes lock-glow {
    0% { filter: drop-shadow(0 0 6px rgba(2, 132, 199, 0.4)); transform: scale(1); }
    50% { filter: drop-shadow(0 0 18px rgba(2, 132, 199, 0.8)); transform: scale(1.03); }
    100% { filter: drop-shadow(0 0 6px rgba(2, 132, 199, 0.4)); transform: scale(1); }
}

@keyframes badge-pulse {
    0% { opacity: 0.7; }
    50% { opacity: 1; }
    100% { opacity: 0.7; }
}

.login-container {
    max-width: 520px;
    margin: 20px auto;
    background: #ffffff;
    border: 2px solid #0284c7;
    border-radius: 20px;
    padding: 35px 30px;
    box-shadow: 0 12px 32px rgba(2, 132, 199, 0.15);
    text-align: center;
    position: relative;
}

.svg-lock-animated {
    animation: lock-glow 3s infinite ease-in-out;
}

.quantum-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #f0fdf4;
    border: 1px solid #22c55e;
    color: #15803d;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 18px;
    animation: badge-pulse 2s infinite ease-in-out;
}

.otp-display-box {
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 20px;
    font-family: 'Fira Code', monospace;
    font-size: 1.1rem;
    color: #0369a1;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.otp-code-highlight {
    background: #0284c7;
    color: #ffffff;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2.5, 1])
    with center:
        # Animated SVG Header Icon
        lock_svg = """<div style="display: flex; justify-content: center; margin-bottom: 15px;">
<svg class="svg-lock-animated" width="85" height="85" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="42" fill="#e0f2fe" stroke="#0284c7" stroke-width="2.5"/>
    <path d="M 50 25 L 72 34 V 52 C 72 66 50 78 50 78 C 50 78 28 66 28 52 V 34 Z" fill="#ffffff" stroke="#0284c7" stroke-width="3"/>
    <circle cx="50" cy="48" r="5" fill="#0284c7"/>
    <polygon points="48,50 52,50 54,62 46,62" fill="#0284c7"/>
</svg>
</div>"""

        # Header Title and Pill Status (Unindented HTML string)
        st.markdown(f"""
<div class="login-container">
{lock_svg}
<div class="quantum-status-pill">
<span style="height: 8px; width: 8px; background-color: #22c55e; border-radius: 50%; display: inline-block;"></span>
Quantum Channel Active & Secure
</div>
<h2 style="color: #0f172a; margin: 0 0 6px 0; font-weight: 700; font-size: 1.6rem;">ADMIN SECURITY GATEWAY</h2>
<p style="color: #64748b; font-size: 0.9rem; margin-bottom: 20px;">Authenticated via BB84 Quantum One-Time Pad Protocol</p>
<div class="otp-display-box">
<span style="font-size: 0.82rem; color: #475569; font-weight: 600;">ACTIVE QUANTUM OTP:</span>
<span class="otp-code-highlight">{expected_otp}</span>
</div>
</div>
""", unsafe_allow_html=True)

        # Interactive Form Control
        autofill = st.checkbox("⚡ Pre-fill Quantum Passcode for Presentation Demo", value=True)

        with st.form("auth_form_portal"):
            st.text_input("User Identity", value="administrator@quantum.node")
            
            pwd_default = expected_otp if autofill else ""
            pwd = st.text_input("Quantum One-Time Pad (OTP)", value=pwd_default, type="password", placeholder="Enter 8-bit quantum code")
            
            st.write("")
            submit = st.form_submit_button("🔐 AUTHENTICATE & DECRYPT GATEWAY")

            if submit:
                if pwd == expected_otp:
                    st.balloons()
                    st.success("✅ IDENTITY VERIFIED: Quantum key reconciliation successful. Access granted.")
                else:
                    st.error("❌ ACCESS DENIED: OTP mismatch or quantum state corrupted.")

        st.write("")
        if st.button("← Return to Quantum Control Console"):
            st.session_state.page = "dashboard"
            st.rerun()


# --- MAIN APPLICATION ENTRY POINT ---
apply_custom_styles()

if st.session_state.page == "dashboard":
    show_dashboard()
elif st.session_state.page == "login":
    show_login_page()