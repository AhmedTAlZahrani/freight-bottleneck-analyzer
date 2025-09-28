# Freight & Logistics Bottleneck Analyzer  

📦 **Freight transport is the backbone of economies.** Bottlenecks at highways, ports, and border crossings cause:  
- Higher logistics costs 💰  
- Longer delivery times ⏱  
- More carbon emissions 🌍  
- Reduced regional competitiveness 📉  

**Consulting Question:**  
> Where are the biggest freight bottlenecks, how much do they cost, and how can we predict future congestion?  

---

## 🚀 Project Objective
- Analyze freight chokepoints from open datasets.  
- Quantify their costs (delay hours, operating costs, economic losses).  
- Visualize bottleneck severity (charts & maps).  
- Predict (AI/ML) future congestion patterns.  

---

## 🌍 Why It Matters
- **Governments** → prioritize infrastructure investments.  
- **Companies** → optimize supply chain and fleet management.  
- **Consultants** → deliver insights linking infrastructure, business impact, and sustainability.  

---

## 📊 Data Sources
- **Sample Data** (50 rows, included in this repo):  
  [`data/raw/sample_bottlenecks.csv`](data/raw/sample_bottlenecks.csv)  

- **Full Dataset** (87 MB, too large for GitHub):  
  [FAF5.7.1 State database 2018–2024 (CSV)](https://faf.ornl.gov/faf5/Data/FAF5.7.1/faf5.7.1_od_state_2018_2024.csv.zip)  

---

## 🛠 Repo Structure

freight-bottleneck-analyzer/
├─ README.md              # Executive summary + instructions
├─ requirements.txt       # Python dependencies
├─ data/
│  ├─ raw/                # Original data (sample + link to full dataset)
│  ├─ processed/          # Cleaned/derived data
├─ src/
│  ├─ load_data.py        # Functions to load and clean datasets
│  ├─ indicators.py       # Calculations (delay hours, cost, emissions)
│  ├─ ai_model.py         # ML models for congestion prediction
│  ├─ viz.py              # Visualization scripts (charts & maps)
│  └─ main.py             # Entry point to run analysis
├─ notebooks/
│  ├─ 01_exploration.ipynb   # Explore the data
│  └─ 02_ai_prediction.ipynb # Train & test AI model
├─ tests/
│  ├─ test_indicators.py
│  └─ test_ai_model.py
├─ docs/
│  └─ roadmap.md           # Project roadmap + task list
├─ plots/                  # Output charts & maps



## 🎯 Learning Goals (for me as the builder)
- Learn to frame infrastructure problems like a consultant.  
- Apply data analysis + visualization with Python.  
- Practice AI/ML prediction (scikit-learn).  
- Combine **technical + business insights**.  

---

## 📈 Deliverables
- Professional GitHub repo (clean, structured).  
- Charts + maps highlighting bottlenecks.  
- AI notebook forecasting congestion.  
- Consulting-style README written for both **technical & business audiences**.  
