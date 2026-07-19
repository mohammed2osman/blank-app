import streamlit as st
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="منظومة إدارة الصيانة الاحترافية", layout="wide")

# عنوان التطبيق
st.title("⚙️ لوحة تحكم مهندس الصيانة والتشغيل")
st.write("أهلاً بك يا هندسة. نظام مبسط لمتابعة أوامر الصيانة والمعدات.")

# قائمة جانبية للتنقل
menu = ["الرئيسية", "إدارة المعدات (CMMS)", "أوامر الصيانة (WO)"]
choice = st.sidebar.selectbox("القائمة الرئيسية", menu)

# القسم الأول: الرئيسية
if choice == "الرئيسية":
    st.subheader("📊 نظرة عامة على محطة الصيانة")
    
    # مؤشرات أداء سريعة (KPIs)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="إجمالي المعدات المسجلة", value="12 معدة")
    with col2:
        st.metric(label="أوامر صيانة مفتوحة", value="3 أوامر")
    with col3:
        st.metric(label="نسبة الاعتمادية المستهدفة (CMRP)", value="95%")

# القسم الثاني: إدارة المعدات
elif choice == "إدارة المعدات (CMMS)":
    st.subheader("📋 سجل المعدات والآلات")
    
    # بيانات افتراضية للمعدات
    equipment_data = {
        "اسم المعدة": ["مضخة طرد مركزي 1", "ضواغط هواء A", "غسالة خط إنتاج رئيسي"],
        "الحالة": ["تعمل بكفاءة", "تحتاج صيانة وقائية", "متوقفة - عطل كهربائي"],
        "تاريخ آخر فحص": ["2026-07-10", "2026-07-15", "2026-07-19"]
    }
    df = pd.DataFrame(equipment_data)
    st.table(df)

# القسم الثالث: أوامر الصيانة
elif choice == "أوامر الصيانة (WO)":
    st.subheader("🛠️ إنشاء أمر صيانة جديد")
    
    with st.form("work_order_form"):
        wo_title = st.text_input("عنوان أمر الصيانة / العطل")
        wo_type = st.selectbox("نوع الصيانة", ["صيانة وقائية (PM)", "صيانة تصحيحية/طارئة (CM)", "فحص دوري"])
        wo_desc = st.text_area("وصف دقيق للمشكلة (مثال: فحص العزل، قياس الفولت بالأفووميتر، اهتزاز في العضو الدوار)")
        
        submitted = st.form_submit_button("تسجيل أمر الصيانة")
        if submitted:
            st.success(f"✔️ تم حفظ أمر الصيانة بنجاح: {wo_title} ({wo_type})")
