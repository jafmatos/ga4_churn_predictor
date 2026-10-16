from ga4_churn_predictor.data import y_train
from ga4_churn_predictor.data import X_train
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from ga4_churn_predictor.data import y_test
from sklearn.metrics import classification_report
from ga4_churn_predictor.data import X_test
from ga4_churn_predictor.config import MODEL_PATH
import joblib

model = joblib.load(MODEL_PATH)

y_pred = model.predict(X_test)

print(
    f"""
Classification Report:

{classification_report(y_test, y_pred)}
"""
)

print(
    f"""
ROC AUC Score:

{roc_auc_score(y_test, y_pred):.2f}
"""
)

print(
    f"""
Confusion Matrix:

{confusion_matrix(y_test, y_pred)}
"""
)

print(
    f"""
Cross-Validation Score (k=5):

AUC-ROC Mean: {cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc").mean():.4f}
AUC-ROC Std: {cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc").std():.4f}

Accuracy Mean: {cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy").mean():.4f}
Accuracy Std: {cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy").std():.4f}
"""
)

results = cross_validate(model, X_train, y_train, cv=5)
predict_times_in_ms = results["score_time"] * 1000
mean_time_in_ms = predict_times_in_ms.mean()
std_time_in_ms = predict_times_in_ms.std()

print(f"""
Tempo médio por dobra: {mean_time_in_ms:.2f} ms
Desvio padrão: {std_time_in_ms:.2f} ms
""")