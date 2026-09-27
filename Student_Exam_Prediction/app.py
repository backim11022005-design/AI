import streamlit as st
import sys
import os
import matplotlib.pyplot as plt

# Thêm thư mục src vào hệ thống path
sys.path.append(os.path.abspath('src'))
from predict import predict_student_status

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hệ thống AI Dự đoán Kết quả Học tập",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Tùy chỉnh CSS giao diện
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .result-card-pass {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        margin-bottom: 15px;
    }
    .result-card-fail {
        background: linear-gradient(135deg, #dc3545 0%, #f8d7da 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
        margin-bottom: 15px;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #007bff 0%, #0056b3 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
        border: none;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #0056b3 0%, #003d80 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,123,255,0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Thanh bên (Sidebar)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135810.png", width=100)
st.sidebar.title("📌 Nhập Thông Tin Học Tập")

study_hours = st.sidebar.slider("📖 Số giờ tự học / tuần:", 0.0, 40.0, 18.0, 0.5)
attendance = st.sidebar.slider("🏫 Tỷ lệ chuyên cần (%):", 0.0, 100.0, 85.0, 1.0)
midterm = st.sidebar.number_input("📝 Điểm thi giữa kỳ (0-10):", 0.0, 10.0, 7.0, 0.25)
assignment = st.sidebar.number_input("📂 Điểm bài tập (0-10):", 0.0, 10.0, 7.5, 0.25)
absences = st.sidebar.slider("❌ Số buổi vắng mặt:", 0, 20, 2, 1)

# 4. Trang chính
st.title("🎓 HỆ THỐNG DỰ ĐOÁN KẾT QUẢ THI SINH VIÊN")
st.caption("Kết hợp **Quy tắc điều kiện cứng** và **Mô hình AI Random Forest**.")
st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📋 Thông số đã chọn")
    
    m1, m2 = st.columns(2)
    m1.metric("Giờ tự học/tuần", f"{study_hours} giờ")
    m2.metric("Chuyên cần", f"{attendance}%")
    
    m3, m4, m5 = st.columns(3)
    m3.metric("Điểm giữa kỳ", f"{midterm}")
    m4.metric("Điểm bài tập", f"{assignment}")
    m5.metric("Số buổi vắng", f"{absences}")

    st.write("")
    predict_btn = st.button("🚀 KÍCH HOẠT DỰ ĐOÁN AI", use_container_width=True)

with col_right:
    st.subheader("🤖 Kết quả Đánh giá")
    
    if predict_btn:
        try:
            prediction, proba, reason = predict_student_status(study_hours, attendance, midterm, assignment, absences)
            pass_prob = proba[1] * 100
            fail_prob = proba[0] * 100

            # Thẻ kết quả
            if prediction == 1:
                st.markdown(f"""
                    <div class="result-card-pass">
                        <h2 style="margin:0; color:white;">🎉 KẾT QUẢ: ĐỖ (PASS)</h2>
                        <h3 style="margin:8px 0 0 0; color:white;">Xác suất Đỗ: {pass_prob:.1f}%</h3>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="result-card-fail">
                        <h2 style="margin:0; color:white;">⚠️ KẾT QUẢ: TRƯỢT (FAIL)</h2>
                        <h3 style="margin:8px 0 0 0; color:white;">Xác suất Trượt: {fail_prob:.1f}%</h3>
                    </div>
                """, unsafe_allow_html=True)

            # Căn cứ đánh giá
            st.info(f"📌 **Căn cứ đánh giá:** {reason}")

            # Biểu đồ tròn
            fig, ax = plt.subplots(figsize=(4, 3))
            labels = ['Đỗ (Pass)', 'Trượt (Fail)']
            sizes = [pass_prob, fail_prob]
            colors = ['#28a745', '#dc3545']
            explode = (0.05, 0) if prediction == 1 else (0, 0.05)

            ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                   shadow=True, startangle=90, textprops={'fontsize': 10, 'weight': 'bold'})
            ax.axis('equal')
            fig.patch.set_facecolor('#f8f9fa')
            
            st.pyplot(fig)

            # Khuyến nghị
            if prediction == 0:
                st.warning("💡 **Khuyến nghị:** Sinh viên cần đảm bảo: Số buổi vắng ≤ 3, Tỷ lệ chuyên cần ≥ 80%, Điểm GK ≥ 3.0, Điểm BT ≥ 5.0.")
            else:
                st.info("🌟 **Nhận xét:** Sinh viên đạt đủ các chỉ số điều kiện tối thiểu và có kết quả học tập tốt!")

        except Exception as e:
            st.error(f"❌ Xảy ra lỗi: {e}")
            st.warning("💡 Bấm `python src/train_model.py` trong Terminal trước nếu chưa lưu mô hình.")
    else:
        st.info("👈 Tùy chỉnh thông số ở thanh điều khiển bên trái và nhấn **KÍCH HOẠT DỰ ĐOÁN AI**.")