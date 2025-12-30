# Bank Term Deposit Subscription Prediction

## Project Summary  
Built a machine learning model to predict whether a customer will subscribe to a bank term deposit using marketing campaign data from a Kaggle dataset.

## Key Decisions  
- Removed the `duration` feature to prevent data leakage.  
- Treated `"unknown"` values as a valid category instead of imputing or dropping.  
- Focused on realistic evaluation rather than inflated metrics.

## Approach  
- Performed targeted EDA to understand customer behavior and class imbalance.  
- Applied proper preprocessing and encoding using pipelines.  
- Trained multiple models: Random Forest, XGBoost, and LightGBM.  
- Tuned models and built a stacked ensemble for improved performance.

## Results  
- Final stacked model achieved ~80% ROC-AUC.  
- Pipeline designed for consistent training and inference.  
- Model saved for future use and extension.

## What This Demonstrates  
- Strong understanding of data leakage and evaluation strategy  
- Practical ensemble modeling and pipeline design  
- End-to-end ML workflow suitable for real-world applications

## Skills Applied  
Python, Pandas, NumPy, Scikit-learn, Matplotlib,  
Machine Learning, Feature Engineering, Model Evaluation,  
Hyperparameter Tuning, Stacking, Ensemble Learning.


