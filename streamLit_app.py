import streamlit as st
import datetime
import pandas as pd
import io

# إعدادات الصفحة
st.set_page_config(page_title="نظام إدارة الصيانة الاحترافية", page_icon="🛠️", layout="wide")

# تهيئة مخزن البيانات في الجلسة للحفاظ على الجدول
if 'maintenance_records' not in st.session_state:
    st.session_state['maintenance_records'] = []

# تصميم الواجهة - العناوين الرئيسية
st.markdown("<h1 style='text-align: right; color: #1E3A8A;'>⚙️ لوحة تحكم مهندس الصيانة والتشغيل</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: right; color: #4B5563;'>أهلاً بك يا هندسة، نظام مبسط لمتابعة أوامر الصيانة والمعدات</h3>", unsafe_allow_html=True)
st.write("---")

# تقسيم الصفحة إلى جزئين: اليمين للنموذج واليسار لعرض الجدول وزر الإكسيل
col_form, col_data = st.columns([1, 1])

with col_form:
    st.markdown("<h2 style='text-align: right; color: #10B981;'>📝 إنشاء أمر صيانة جديد</h2>", unsafe_allow_html=True)

    # نموذج إدخال البيانات (الرسمة الخاصة بك)
    with st.form("main_form", clear_on_submit=True):
        
        department_options = ["الصيانة الميكانيكية", "الصيانة الكهربائية", "الجودة"]
        department = st.selectbox("القسم 🔽", department_options, index=None, placeholder="اختر القسم...")
        
        maintenance_type_options = ["PM (Preventive Maintenance)", "CM (Corrective Maintenance)", "Break Down"]
        maintenance_type = st.selectbox("نوع الصيانة 🔽", maintenance_type_options, index=None, placeholder="اختر نوع الصيانة...")
        
        c1, c2 = st.columns(2)
        with c1:
            start_date = st.date_input("وقت العمل - من تاريخ", datetime.date.today())
        with c2:
            start_time = st.time_input("وقت العمل - من ساعة", datetime.time(8, 0))
        
        c3, c4 = st.columns(2)
        with c3:
            end_date = st.date_input("وقت الانتهاء - إلى تاريخ", datetime.date.today())
        with c4:
            end_time = st.time_input("وقت الانتهاء - إلى ساعة", datetime.time(16, 0))
        
        equipment_name = st.text_input("المعدة")
        technicians_names = st.text_input("أسماء القائمين على العمل")
        shift_engineers = st.text_input("مهندسي الوردية")
        failure_description = st.text_input("تشخيص العطل")
        spare_parts = st.text_input("قطع الغيار")

        submit_button = st.form_submit_button("إرسال أمر الصيانة")

    # عند الضغط على إرسال، يتم حساب الفترة تلقائياً وحفظ البيانات
    if submit_button:
        if not department or not maintenance_type or not equipment_name or not technicians_names:
            st.error("يرجى ملء الحقول الأساسية: القسم، نوع الصيانة، المعدة، وأسماء القائمين.")
        else:
            # دمج التاريخ والوقت
            start_datetime = datetime.datetime.combine(start_date, start_time)
            end_datetime = datetime.datetime.combine(end_date, end_time)
            
            # حساب الفرق
            time_difference = end_datetime - start_datetime
            
            if time_difference.total_seconds() < 0:
                st.error("❌ خطأ: وقت الانتهاء لا يمكن أن يكون قبل وقت بدء العمل!")
            else:
                total_seconds = int(time_difference.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                work_duration = f"{hours} ساعة و {minutes} دقيقة" if hours > 0 else f"{minutes} دقيقة"
                
                # إضافة السجل الجديد
                new_record = {
                    "القسم": department,
                    "نوع الصيانة": maintenance_type,
                    "المعدة": equipment_name,
                    "وقت البدء": start_datetime.strftime("%Y-%m-%d %H:%M"),
                    "وقت الانتهاء": end_datetime.strftime("%Y-%m-%d %H:%M"),
                    "الفترة (محسوبة آلياً)": work_duration,
                    "القائمين بالعمل": technicians_names,
                    "مهندس الوردية": shift_engineers,
                    "تشخيص العطل": failure_description,
                    "قطع الغيار": spare_parts
                }
                st.session_state['maintenance_records'].append(new_record)
                st.success(f"✅ تم تسجيل أمر الصيانة بنجاح للمعدة: {equipment_name}")
                st.rerun()

with col_data:
    st.markdown("<h2 style='text-align: right; color: #3B82F6;'>📊 الأوامر المسجلة وتصدير Excel</h2>", unsafe_allow_html=True)
    
    if len(st.session_state['maintenance_records']) == 0:
        st.info("لا توجد أوامر صيانة مسجلة حالياً. قم بملء النموذج على اليمين للبدء.")
    else:
        df = pd.DataFrame(st.session_state['maintenance_records'])
        
        # عرض الجدول تفاعلياً
        st.dataframe(df, use_container_width=True)
        
        # تصدير إلى شيت Excel حقيقي ونظيف
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='أوامر الصيانة')
        buffer.seek(0)
        
        # زرار سحب الإكسيل الحقيقي (.xlsx)
        st.download_button(
            label="📥 تحميل البيانات كـ ملف Excel",
            data=buffer,
            file_name=f"maintenance_report_{datetime.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        if st.button("🗑️ مسح الجدول الحالي"):
            st.session_state['maintenance_records'] = []
            st.rerun()

# --- تذييل الصفحة ---
st.write("---")
st.markdown("<p style='text-align: center; color: #6B7280;'>نظام إدارة صيانة مبسط © 2026</p>", unsafe_allow_html=True)
