================================================================================
  TELEMEDICINE APP — MARKET INTELLIGENCE DASHBOARD
  README
================================================================================

DESCRIPTION
-----------
An interactive Streamlit dashboard that analyses survey data from 2,000 UAE
expats to inform the development and launch strategy of a telemedicine mobile
application. The dashboard covers descriptive analytics, customer segmentation,
association rule mining, classification, and regression — all anchored to the
north star metric: App Adoption Likelihood (Q25).


REQUIREMENTS
------------
- Python 3.9 or higher (tested on 3.10, 3.11, 3.12)
- pip (Python package manager)
- A modern web browser (Chrome, Firefox, Edge, Safari)


FILE STRUCTURE
--------------
Place all files in the same directory:

    telemedicine-dashboard/
    ├── .streamlit/
    │   └── config.toml                     # Dark theme configuration
    ├── app.py                              # Main Streamlit application
    ├── requirements.txt                    # Python dependencies
    ├── Telemedicine_Survey_Cleaned.csv     # Cleaned survey dataset
    └── README.txt                          # This file


INSTALLATION & SETUP
--------------------
1.  Open a terminal / command prompt.

2.  (Recommended) Create and activate a virtual environment:

        python -m venv venv

        # Windows
        venv\Scripts\activate

        # macOS / Linux
        source venv/bin/activate

3.  Install dependencies:

        pip install -r requirements.txt

4.  Verify the CSV file is in the same directory as app.py.


RUNNING THE DASHBOARD
---------------------
From the project directory, run:

    streamlit run app.py

The dashboard will open in your default browser at http://localhost:8501.


DEPLOYING TO STREAMLIT CLOUD
-----------------------------
1.  Push all four files to a GitHub repository.

2.  Go to https://share.streamlit.io and sign in with GitHub.

3.  Click "New app" and select your repository, branch, and "app.py" as the
    main file.

4.  Click "Deploy". Streamlit Cloud will install requirements.txt automatically.

Note: Ensure the CSV file and the .streamlit/ folder are both committed to the
repository in the same directory as app.py. The .streamlit/config.toml file
controls the dark theme — Streamlit Cloud reads it automatically.


DASHBOARD TABS
--------------
Tab 1 — Data Overview & Quality
    Dataset shape, column types, missing value treatment summary, outlier
    detection results (IQR method on monthly spend), and all cleaning steps.

Tab 2 — Demographic Profile
    Age, gender, nationality, employment, and income distributions with
    contextual insights for each chart.

Tab 3 — Healthcare Landscape
    Insurance status, visit frequency, satisfaction levels, top healthcare
    challenges (from multi-select), and expenditure histogram with outliers.

Tab 4 — Adoption Drivers (EDA)
    All demographic and behavioural variables cross-tabbed against Q25
    (Yes/Maybe/No). Includes correlation heatmap of all numeric variables.

Tab 5 — Customer Segmentation (K-Means)
    Elbow method and silhouette analysis, cluster profiles via radar chart,
    adoption rates per cluster, persona descriptions, and targeting
    recommendations.

Tab 6 — Pattern Discovery (Association Rules)
    Three sub-analyses: challenge co-occurrence, feature co-occurrence, and
    cross-mining (challenges → features). Top-20 rules tables and
    confidence-vs-lift scatter plots for each.

Tab 7 — Predictive Models
    Classification: 7 models (Logistic Regression, Decision Tree, Random
    Forest, SVM, KNN, Naive Bayes, XGBoost) compared on accuracy, precision,
    recall, F1-score. Confusion matrix and feature importance for the best
    model.
    Regression: 3 models (Linear, Ridge, Lasso) predicting monthly spend.
    R², MAE, RMSE comparison, coefficients, and actual-vs-predicted plot.

Tab 8 — Recommendations & Summary
    North star metric recap, one key insight per tab, 5 actionable business
    recommendations, and a launch strategy summary (target persona, priority
    features, pricing, go-to-market).


TROUBLESHOOTING
---------------
-  "FileNotFoundError: Telemedicine_Survey_Cleaned.csv"
   → Ensure the CSV file is in the same directory as app.py.

-  "ModuleNotFoundError: No module named 'xgboost'"
   → Run: pip install -r requirements.txt

-  Slow first load
   → Normal. Streamlit caches the data after first load. Subsequent
     interactions will be faster.

-  Port 8501 already in use
   → Run: streamlit run app.py --server.port 8502


================================================================================
