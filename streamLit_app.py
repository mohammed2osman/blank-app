import streamlit as st
import datetime

# إعدادات الصفحة
st.set_page_config(page_title="نظام إدارة الصيانة الاحترافية", page_icon="🛠️", layout="wide")

# تصميم الواجهة - العناوين الرئيسية
st.markdown("<h1 style='text-align: right; color: #1E3A8A;'>⚙️ لوحة تحكم مهندس الصيانة والتشغيل</h1>", unsafe_allow_config=True)
st.markdown("<h3 style='text-align: right; color: #4B5563;'>أهلاً بك يا هندسة، نظام مبسط لمتابعة أوامر الصيانة والمعدات</h3>", unsafe_allow_config=True)
st.write("---")

# --- نموذج إنشاء أمر صيانة جديد ---
st.markdown("<h2 style='text-align: right; color: #10B981;'>📝 إنشاء أمر صيانة جديد</h2>", unsafe_allow_config=True)

# تجميع المدخلات في نموذج (form) واحد لضمان إرسال البيانات مرة واحدة
with st.form("main_form", clear_on_submit=False):
    
    # 1. القائمة المنسدلة للقسم
    department_options = ["الصيانة الميكانيكية", "الصيانة الكهربائية", "الجودة"]
    department = st.selectbox("القسم 🔽", department_options, index=None, placeholder="اختر القسم...")
    
    # 2. القائمة المنسدلة لنوع الصيانة
    maintenance_type_options = ["PM (Preventive Maintenance)", "CM (Corrective Maintenance)", "Break Down"]
    maintenance_type = st.selectbox("نوع الصيانة 🔽", maintenance_type_options, index=None, placeholder="اختر نوع الصيانة...")
    
    # 3. تاريخ ووقت العطل
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("وقت العطل - التاريخ", datetime.date.today())
    with col2:
        start_time = st.time_input("وقت العطل - الساعة", datetime.time(8, 0))
    
    # 4. تاريخ ووقت الانتهاء
    col3, col4 = st.columns(2)
    with col3:
        end_date = st.date_input("وقت الانتهاء - التاريخ", datetime.date.today())
    with col4:
        end_time = st.time_input("وقت الانتهاء - الساعة", datetime.time(16, 0))
    
    # 5. الحقول النصية لباقي البيانات
    equipment_name = st.text_input("المعدة (اسم المعدة)")
    equipment_code = st.text_input("كود المعدة (إن وجد)")
    work_duration = st.text_input("الفترة (مدة العمل)")
    technicians_names = st.text_input("أسماء القائمين على العمل")
    shift_engineers = st.text_input("مهندسي الوردية")
    failure_description = st.text_input("تشخيص العطل (وصف دقيق للمشكلة)")
    spare_parts = st.text_input("قطع الغيار (المستخدمة أو المطلوبة)")
    problem_details = st.text_area("وصف دقيق للمشكلة") # حقل أكبر للوصف المفصل

    # زر إرسال النموذج
    submit_button = st.form_submit_button("إرسال أمر الصيانة")

# --- معالجة البيانات بعد الإرسال ---
if submit_button:
    # يمكنك هنا إضافة كود لحفظ البيانات في قاعدة بيانات أو ملف
    if not department or not maintenance_type or not equipment_name or not technicians_names:
        st.error("يرجى ملء الحقول الأساسية: القسم، نوع الصيانة، المعدة، وأسماء القائمين.")
    else:
        # مثال على كيفية تجميع البيانات
        full_work_order = {
            "Department": department,
            "Maintenance Type": maintenance_type,
            "Equipment": equipment_name,
            "Equipment Code": equipment_code,
            "Start Time": datetime.datetime.combine(start_date, start_time),
            "End Time": datetime.datetime.combine(end_date, end_time),
            "Duration": work_duration,
            "Technicians": technicians_names,
            "Shift Engineers": shift_engineers,
            "Failure Description": failure_description,
            "Spare Parts": spare_parts,
            "Problem Details": problem_details
        }
        
        st.success(f"تم إرسال أمر صيانة جديد للقسم: {department}، نوع: {maintenance_type}")
        # st.write(full_work_order) # إلغاء التعليق لرؤية البيانات بصيغة قاموس (Dictionary)

# --- تذييل الصفحة ---
st.write("---")
st.markdown("<p style='text-align: center; color: #6B7280;'>نظام إدارة صيانة مبسط © 2024</p>", unsafe_allow_config=True)
