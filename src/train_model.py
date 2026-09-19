import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ============================================================
# 1. Load dataset
# ============================================================

print("=" * 70)
print("PHISHING URL DETECTOR - MODEL TRAINING")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv("data/real_urls.csv")

df = df[["url", "label"]].copy()

print("Original dataset:", df.shape)


# ============================================================
# 2. Clean dataset
# ============================================================

print("\nCleaning dataset...")

df["url"] = (
    df["url"]
    .astype(str)
    .str.strip()
)

df["label"] = (
    df["label"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# Remove empty URLs
df = df[df["url"] != ""]

# Remove duplicate URLs
df = df.drop_duplicates(
    subset="url"
)

# Convert labels
df["label"] = df["label"].map({
    "legitimate": 0,
    "phishing": 1
})

# Remove unknown labels
df = df.dropna(
    subset=["label"]
)

df["label"] = df["label"].astype(int)

print("Clean dataset:", df.shape)

print("\nLabel distribution:")
print(df["label"].value_counts())


# ============================================================
# 3. Separate input and target
# ============================================================

X = df["url"]

y = df["label"]


# ============================================================
# 4. Train / Test split
# ============================================================

print("\nCreating train/test split...")

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("Training URLs:", len(X_train))
print("Testing URLs :", len(X_test))


# ============================================================
# 5. Character-level TF-IDF
# ============================================================

print("\nCreating character-level TF-IDF model...")

vectorizer = TfidfVectorizer(

    analyzer="char",

    ngram_range=(3, 5),

    min_df=2,

    max_features=200000,

    sublinear_tf=True
)


# ============================================================
# 6. Logistic Regression
# ============================================================

print("Creating classifier...")

classifier = LogisticRegression(

    max_iter=1000,

    random_state=42,

    class_weight="balanced",

    solver="liblinear"
)


# ============================================================
# 7. Complete pipeline
# ============================================================

model = Pipeline([

    (
        "tfidf",
        vectorizer
    ),

    (
        "classifier",
        classifier
    )

])


# ============================================================
# 8. Train
# ============================================================

print("\nTraining character-level URL model...")
print("This may take some time.")

model.fit(
    X_train,
    y_train
)

print("\nTraining completed!")


# ============================================================
# 9. Predictions
# ============================================================

print("\nEvaluating model...")

y_pred = model.predict(
    X_test
)


# ============================================================
# 10. Performance
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)


print("\n" + "=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)

print(
    f"Accuracy : {accuracy:.4f}"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1 Score : {f1:.4f}"
)


# ============================================================
# 11. Confusion Matrix
# ============================================================

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ============================================================
# 12. Classification Report
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Legitimate",
            "Phishing"
        ]
    )
)


# ============================================================
# 13. Save model
# ============================================================

os.makedirs(
    "model",
    exist_ok=True
)

joblib.dump(
    model,
    "model/phishing_model.pkl"
)


print("\n" + "=" * 70)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 70)

print(
    "Location: model/phishing_model.pkl"
)

print("\nTraining process completed!")