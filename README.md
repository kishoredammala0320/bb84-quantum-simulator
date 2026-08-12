# BB84 Quantum Key Exchange Console ⚛️ Laser & Qubit Simulator

An interactive, web-based simulation console for the **BB84 Quantum Key Distribution (QKD) Protocol**. This application simulates quantum state transmission between **Alice (Transmitter)**, **Eve (Interception Node)**, and **Bob (Receiver)**, providing real-time Quantum Bit Error Rate (QBER) telemetry, basis reconciliation, and a One-Time Pad (OTP) authentication gateway.

---

## 🚀 Features

* **Quantum State Transmission:** Simulates Alice emitting photon bit states using rectilinear ($+$) and diagonal ($\times$) polarization bases.
* **Eve Interception Engine:** Simulates eavesdropping attacks on the quantum channel, demonstrating wavefunction collapse and noise introduction.
* **Real-Time QBER Telemetry:** Automatically calculates the Quantum Bit Error Rate (QBER) and flags security breaches if errors exceed the $15\%$ threshold.
* **Sifted Key Reconciliation:** Displays step-by-step photon slot logs and basis matching results to form a secure One-Time Pad (OTP).
* **Authenticated Security Gateway:** Features a secondary login portal secured by the dynamically generated 8-bit quantum key.
* **Interactive Visual Analytics:** Visualizes key fidelity and reconciliation metrics using Plotly charts and custom-styled Streamlit UI components.

---

## 🧠 Protocol Details

This simulator implements the classic **BB84 Quantum Cryptography Protocol**:

1. **State Preparation:** Alice generates random classical bits and encodes them into photon states using randomly chosen bases ($+$ or $\times$).
2. **Channel Transmission:** Photons travel through the optical channel. If active, Eve intercepts and measures qubits in randomly chosen bases before re-transmitting them to Bob.
3. **Bob's Measurement:** Bob measures incoming qubits using his own randomly selected bases.
4. **Sifting:** Alice and Bob compare their chosen bases over a public channel and discard bits where their bases did not match.
5. **Error Estimation:** A subset of the sifted key is compared to detect eavesdropping. A QBER $\ge 15\%$ indicates interception.

---

## 🏗 Architecture

```text
bb84-quantum-simulator/
├── app.py              ← Streamlit multi-page UI, custom CSS, & dashboard logic
├── main.py             ← Quantum logic simulation engine (simulate_bb84)
├── .gitignore          ← Git security & cache rules
└── requirements.txt    ← Python package dependencies
```
---

## 🛠 Tech Stack
Language: Python 3.10+

Web Framework: Streamlit

Data Visualization: Plotly, Pandas, NumPy

Styling & Animation: CSS3, Inline SVGs 

---

---

## 🚀 Quick Start
## 1. Clone & Setup
```Bash
git clone [https://github.com/YOUR-USERNAME/bb84-quantum-simulator.git](https://github.com/YOUR-USERNAME/bb84-quantum-simulator.git)
cd bb84-quantum-simulator

## # Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## # Install dependencies
pip install -r requirements.txt
```
## 2. Run the Console
```Bash
streamlit run app.py
```
## 3. Open in Browser
```
Navigate to http://localhost:8501 in your browser.


