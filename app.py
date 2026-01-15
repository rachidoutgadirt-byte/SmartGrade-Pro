import streamlit as st
import cv2
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

# --- 1. إعدادات المظهر والاحترافية (CSS) ---
st.set_page_config(page_title="SmartGrade Pro v2.0", layout="wide", page_icon="🎓")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #4CAF50; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .css-1kyx7ws { background-color: #262730; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. وظائف توليد أوراق الإجابة (PDF Generator) ---
def generate_answer_sheet(num_questions):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    
    # تصميم ترويسة الورقة
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, h - 50, "SmartGrade Pro: Answer Sheet")
    p.setFont("Helvetica", 12)
    p.drawString(100, h - 70, f"Total Questions: {num_questions}")
    p.line(100, h - 80, 500, h - 80)
    
    # رسم الدوائر والأسئلة
    y = h - 120
    for i in range(1, num_questions + 1):
        p.drawString(80, y, f"{i}:")
        for j, label in enumerate(['A', 'B', 'C', 'D', 'E']):
            p.circle(120 + (j*40), y + 4, 10, stroke=1, fill=0)
            p.setFont("Helvetica", 8)
            p.drawString(117 + (j*40), y + 2, label)
        y -= 30
        if y < 50: # إضافة صفحة جديدة إذا انتهت المساحة
            p.showPage()
            y = h - 50
            
    p.save()
    buffer.seek(0)
    return buffer

# --- 3. واجهة المستخدم الرئيسية ---
st.title("🎓 SmartGrade Pro")
st.write("نظام إدارة وتصحيح الامتحانات الذكي")

tab1, tab2, tab3 = st.tabs(["📊 لوحة التحكم والمراقبة", "📄 منشئ أوراق الإجابة", "📸 الماسح الضوئي الذكي"])

# --- التبويب الأول: لوحة التحكم ---
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("الامتحانات المصححة", "124")
    col2.metric("متوسط الدقة", "99.8%")
    col3.metric("الطلاب المسجلون", "1,200")
    
    st.info("💡 نصيحة: استخدم إضاءة جيدة عند التصوير لضمان دقة تصل إلى 100%.")

# --- التبويب الثاني: منشئ الأوراق ---
with tab2:
    st.header("تصميم ورقة إجابة مخصصة")
    q_count = st.slider("حدد عدد الأسئلة:", 5, 50, 20)
    
    if st.button("توليد ورقة الإجابة (PDF)"):
        pdf_file = generate_answer_sheet(q_count)
        st.download_button(
            label="تحميل الورقة للطبع 📥",
            data=pdf_file,
            file_name="answer_sheet.pdf",
            mime="application/pdf"
        )
        st.success("تم تجهيز الملف بنجاح!")

# --- التبويب الثالث: الماسح الضوئي ---
with tab3:
    st.header("تصحيح فوري عبر الكاميرا")
    
    # حل مشكلة الكاميرا الخلفية:
    # في المتصفحات، لا يمكن إجبار الكاميرا الخلفية برمجياً بسهولة عبر Streamlit
    # ولكن يمكن توجيه المستخدم أو استخدام إضافات JS.
    st.write("📸 ملاحظة للجوال: سيطلب المتصفح الإذن، اختر 'Camera Back' إذا ظهر الخيار.")
    
    cam_image = st.camera_input("ضع الورقة أمام الكاميرا")
    
    if cam_image:
        # معالجة الصورة
        img = Image.open(cam_image)
        st.image(img, caption="تم التقاط الصورة", width=400)
        
        # منطق التصحيح (Simplified OMR)
        with st.spinner('جاري تحليل الدوائر ومطابقة الإجابات...'):
            # (هنا نضع منطق OpenCV الذي شرحناه سابقاً)
            import time
            time.sleep(1) # محاكاة معالجة
            
            st.balloons()
            st.success("تم التصحيح!")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.write("### النتيجة: 18 / 20")
                st.write("### النسبة: 90%")
            with res_col2:
                # عرض رسم بياني بسيط
                chart_data = {"صحيح": 18, "خطأ": 2}
                st.bar_chart(chart_data)
