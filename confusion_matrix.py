from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib
import pandas as pd

# Load your trained model
model = joblib.load("model_CNC_01.pkl")

# Load test data
data = pd.read_csv("sensor_history.csv")

# Example features used in your model
X = data[["temperature_C", "vibration_mm_s", "rpm", "current_A"]]

# Actual labels column in your CSV
y_true = data["status"]

# Predicted labels
y_pred = model.predict(X)

# Create confusion matrix
labels = ["normal", "warning", "critical"]

cm = confusion_matrix(y_true, y_pred, labels=labels)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

disp.plot(cmap="Blues", values_format="d")
plt.title("Confusion Matrix")
plt.show()