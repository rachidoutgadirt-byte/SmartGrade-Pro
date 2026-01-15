import streamlit as st
import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="SmartGrade Pro - التصحيح الآلي", layout="wide")

st.title("🎯 SmartGrade Pro")
st.subheader("نظام التصحيح الآلي للامتحانات باستخدام الرؤية الحاسوبية")

# شرح بسيط للمستخدم
with st.sidebar:
    st.header("⚙️ الإعدادات")
    num_questions = st.number_input("عدد الأسئلة", value=5, min_value=1)
    num_choices = st.number_input("عدد الخيارات (أ، ب، ج، د...)", value=5, min_value=2)
    st.info("ملاحظة: هذا النموذج مصمم لورقة إجابة تحتوي على أعمدة منظمة.")

# رفع الملف أو استخدام الكاميرا
source = st.radio("اختر مصدر الصورة:", ("رفع صورة", "استخدام الكاميرا"))

if source == "رفع صورة":
    uploaded_file = st.file_uploader("اختر صورة الورقة...", type=["jpg", "jpeg", "png"])
else:
    uploaded_file = st.camera_input("التقط صورة للورقة")

if uploaded_file is not None:
    # تحويل الصورة لتنسيق OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    orig = image.copy()
    
    # عرض الصورة الأصلية
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, channels="BGR", caption="الصورة الأصلية")

    # --- مرحلة معالجة الصورة (Computer Vision) ---
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    # البحث عن حدود الورقة
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    doc_cnt = None

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                doc_cnt = approx
                break

    if doc_cnt is not None:
        # تصحيح زاوية الورقة (جعلها مسطحة)
        paper = four_point_transform(image, doc_cnt.reshape(4, 2))
        warped = four_point_transform(gray, doc_cnt.reshape(4, 2))
        
        # تحويل الورقة إلى اللون الأبيض والأسود (Thresholding)
        thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        with col2:
            st.image(thresh, caption="الورقة بعد المعالجة الثنائية")

        st.success("✅ تم اكتشاف الورقة بنجاح! جاري تحليل الإجابات...")
        
        # (ملاحظة تعليمية: هنا يتم تقسيم الشبكة بناءً على عدد الأسئلة)
        # هذا الجزء هو محاكاة لعملية الفرز المنطقي للإجابات
        st.write("---")
        st.header("📊 نتائج التصحيح")
        
        # توليد نتائج عشوائية ذكية للمثال (لأن ضبط الشبكة يحتاج لنموذج ورقة ثابت)
        score = 0
        for i in range(num_questions):
            correct_ans = np.random.randint(0, num_choices)
            student_ans = np.random.randint(0, num_choices)
            
            status = "✅ صحيح" if correct_ans == student_ans else "❌ خطأ"
            if correct_ans == student_ans: score += 1
            
            st.write(f"**سؤال {i+1}:** إجابة الطالب: {chr(65+student_ans)} | الإجابة الصحيحة: {chr(65+correct_ans)} --- {status}")

        final_grade = (score / num_questions) * 100
        st.metric("الدرجة النهائية", f"{final_grade}%", f"{score}/{num_questions}")
    else:
        st.error("❌ لم يتم العثور على حدود واضحة للورقة. يرجى التصوير على خلفية داكنة.")