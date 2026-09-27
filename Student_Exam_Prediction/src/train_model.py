import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from data_preprocessing import load_and_preprocess_data

def train_and_save_model():
    data_path = os.path.join('data', 'student_data.csv')
    X, y, X_scaled, scaler = load_and_preprocess_data(data_path)
    
    # Chia tập dữ liệu: 80% Train, 20% Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Khởi tạo mô hình Random Forest
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Đánh giá mô hình
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # Tạo thư mục models/ nếu chưa có
    os.makedirs('models', exist_ok=True)
    
    # Lưu mô hình và bộ chuẩn hóa
    joblib.dump(model, os.path.join('models', 'model_random_forest.pkl'))
    joblib.dump(scaler, os.path.join('models', 'scaler.pkl'))
    print("Đã lưu thành công mô hình và scaler vào thư mục models/!")

if __name__ == '__main__':
    train_and_save_model()