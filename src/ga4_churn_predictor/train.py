from sklearn.model_selection import GridSearchCV
from ga4_churn_predictor.data import y_train
from ga4_churn_predictor.data import X_train
from ga4_churn_predictor.pipeline import pipeline
from ga4_churn_predictor.config import MODEL_PATH
import joblib

def train_and_save_model():
    parameters = {
        "feature_selection__k": [3, 4, 5, 6, 7, 8, 9, 10, 11],
        "model__max_depth": [2, 3, 4, 5, 6, 7],
        "model__learning_rate": [0.01, 0.05, 0.1],
    }

    grid_search = GridSearchCV(pipeline, parameters, cv=5, scoring="roc_auc", n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_pipeline = grid_search.best_estimator_

    column_transformer = best_pipeline.named_steps["column_transformer"]
    feature_selection_step = best_pipeline.named_steps['feature_selection']

    feature_names = column_transformer.get_feature_names_out()
    best_features = feature_names[feature_selection_step.get_support()]
    best_feature_scores = feature_selection_step.scores_[feature_selection_step.get_support()]

    for nome, score in sorted(zip(best_features, best_feature_scores), key=lambda x: x[1], reverse=True):
        print(f"{nome}: {score:.4f}")

    print(f"Melhor ROC-AUC: {grid_search.best_score_:.4f}")
    print(f"Melhor combinação de parâmetros: {grid_search.best_params_}")

    joblib.dump(grid_search.best_estimator_, MODEL_PATH)

    print(f"Modelo salvo em: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()