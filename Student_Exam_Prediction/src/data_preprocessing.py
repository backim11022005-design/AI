import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data(file_path):
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(file_path)
    
    # Xử lý giá trị khuyết (nếu có)
    df = df.fillna(df.mean())
    
    # Chia đặc trưng (X) và nhãn (y)
    X = df[['StudyHours', 'AttendanceRate', 'MidtermScore', 'AssignmentScore', 'Absences']]
    y = df['Passed']
    
    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X, y, X_scaled, scaler