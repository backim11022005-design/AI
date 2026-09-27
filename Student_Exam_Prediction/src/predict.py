import os
import joblib
import numpy as np

def predict_student_status(study_hours, attendance, midterm, assignment, absences):
    # --- BƯỚC 1: KIỂM TRA QUY TẮC ĐIỀU KIỆN CỨNG ---
    # Điều kiện bị đánh TRƯỢT:
    # 1. Số buổi vắng mặt TRÊN 3 buổi (absences > 3)
    # 2. Tỷ lệ chuyên cần DƯỚI 80% (attendance < 80.0)
    # 3. Điểm giữa kỳ DƯỚI 3 (midterm < 3.0)
    # 4. Điểm bài tập DƯỚI 5 (assignment < 5.0)
    
    failed_reasons = []
    if absences > 3:
        failed_reasons.append("Vắng mặt > 3 buổi")
    if attendance < 80.0:
        failed_reasons.append("Tỷ lệ chuyên cần < 80%")
    if midterm < 3.5:
        failed_reasons.append("Điểm giữa kỳ < 3.5")
    if assignment < 5.0:
        failed_reasons.append("Điểm bài tập < 5.0")

    # Nếu vi phạm bất kỳ điều kiện nào -> Trả về ngay kết quả TRƯỢT
    if len(failed_reasons) > 0:
        reason_msg = "Vi phạm quy tắc điều kiện: " + ", ".join(failed_reasons)
        return 0, np.array([1.0, 0.0]), reason_msg

    # --- BƯỚC 2: NẾU ĐẠT ĐIỀU KIỆN -> SỬ DỤNG MÔ HÌNH MACHINE LEARNING ---
    model_path = os.path.join('models', 'model_random_forest.pkl')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError("Chưa tìm thấy file mô hình! Vui lòng chạy train_model.py trước.")
        
    model = joblib.load(model_path)
    
    # Tạo mảng dữ liệu đầu vào
    input_data = np.array([[study_hours, attendance, midterm, assignment, absences]])
    
    # Dự đoán nhãn và xác suất
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    return prediction, probabilities, "Được dự đoán bởi Mô hình Học máy (Random Forest)"