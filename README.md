
# TB Test Expiry Checker

A web-based HR tool to identify employees whose TB test will expire by June 30, 2025.

## 🚀 Features
- Upload Excel spreadsheet (`renewables.xlsx`)
- Automatically filters for:
  - Active employees
  - TB test dates in 2022
  - TB tests expiring within 3 years (by 2025-06-30)
- Displays results in browser
- Download results as CSV

## 📦 Setup Instructions

1. Clone this repo:
   ```
   git clone https://github.com/your-username/renewables-tb-checker.git
   cd renewables-tb-checker
   ```

2. Create virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the app:
   ```
   streamlit run app.py
   ```

## 🌐 Deploy to Streamlit Cloud
1. Push this repo to GitHub.
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud) and log in.
3. Click **"New App"**, choose your repo, and deploy.
