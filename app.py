
# #1. QUẢN LÝ ĐIỂM SINH VIÊN - STREAMLIT WEB APP

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình trang web
st.set_page_config(
    page_title="QUẢN LÝ ĐIỂM SINH VIÊN",
    page_icon="📊",
    layout="wide"
)

# THAY HAI GIÁ TRỊ DƯỚI ĐÂY BẰNG THÔNG TIN CỦA BẠN
TEN_NGUOI_TAO = "Điền họ tên của bạn"
MSSV = "Điền mã số sinh viên của bạn"


# #2. TẠO DATAFRAME GỒM 10 SINH VIÊN
data = {
    "Ho_ten": [
        "Nguyễn Minh Anh",
        "Trần Gia Huy",
        "Lê Hoàng Yến",
        "Phạm Tuấn Kiệt",
        "Võ Ngọc Hà",
        "Đặng Quốc Bảo",
        "Bùi Khánh Linh",
        "Phan Đức Long",
        "Đỗ Mai Phương",
        "Hoàng Nhật Nam"
    ],
    "Chuyen_can": [9.0, 7.5, 8.0, 6.0, 9.5, 5.5, 8.5, 4.0, 7.0, 6.5],
    "Giua_ky":    [8.5, 8.0, 7.0, 5.0, 9.0, 6.5, 8.0, 5.5, 6.5, 7.5],
    "Cuoi_ky":    [9.2, 7.0, 8.5, 4.5, 8.8, 7.0, 8.0, 6.0, 6.8, 8.1]
}

df = pd.DataFrame(data)


# #3. TÍNH ĐIỂM TỔNG KẾT
df["Tong_ket"] = (
    df["Chuyen_can"] * 0.2
    + df["Giua_ky"] * 0.3
    + df["Cuoi_ky"] * 0.5
).round(2)


# #4. XẾP LOẠI SINH VIÊN
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)


# #5. TIÊU ĐỀ VÀ BẢNG ĐIỂM
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write(
    "Ứng dụng quản lý điểm, tính điểm tổng kết, "
    "xếp loại và thống kê kết quả học tập."
)

st.subheader("Bảng điểm của 10 sinh viên")

ten_cot = {
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
}

df_hien_thi = df.rename(columns=ten_cot)

st.dataframe(
    df_hien_thi.style.format({
        "Chuyên cần": "{:.1f}",
        "Giữa kỳ": "{:.1f}",
        "Cuối kỳ": "{:.1f}",
        "Tổng kết": "{:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)


# #6. THỐNG KÊ KẾT QUẢ CỦA LỚP
diem_trung_binh = df["Tong_ket"].mean()
sv_cao_nhat = df.loc[df["Tong_ket"].idxmax()]
sv_thap_nhat = df.loc[df["Tong_ket"].idxmin()]
so_sinh_vien_dat = (df["Tong_ket"] >= 5).sum()

st.subheader("Thống kê kết quả học tập")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Điểm trung bình lớp", f"{diem_trung_binh:.2f}")

with col2:
    st.metric("Điểm cao nhất", f"{sv_cao_nhat['Tong_ket']:.2f}")
    st.caption(sv_cao_nhat["Ho_ten"])

with col3:
    st.metric("Điểm thấp nhất", f"{sv_thap_nhat['Tong_ket']:.2f}")
    st.caption(sv_thap_nhat["Ho_ten"])

with col4:
    st.metric("Số sinh viên đạt (>= 5)", f"{so_sinh_vien_dat}/10")


# #7. SELECTBOX TRA CỨU MỘT SINH VIÊN
st.subheader("Tra cứu điểm từng sinh viên")

ten_duoc_chon = st.selectbox(
    "Chọn một sinh viên:",
    df["Ho_ten"].tolist()
)

sv = df.loc[df["Ho_ten"] == ten_duoc_chon].iloc[0]

st.write(f"**Họ và tên:** {sv['Ho_ten']}")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Chuyên cần", f"{sv['Chuyen_can']:.2f}")

with col2:
    st.metric("Giữa kỳ", f"{sv['Giua_ky']:.2f}")

with col3:
    st.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.2f}")

with col4:
    st.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")

with col5:
    st.metric("Xếp loại", sv["Xep_loai"])


# #8. VẼ BIỂU ĐỒ CỘT BẰNG MATPLOTLIB
st.subheader("Biểu đồ điểm tổng kết của 10 sinh viên")

fig, ax = plt.subplots(figsize=(12, 5))

cot = ax.bar(df["Ho_ten"], df["Tong_ket"])

ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", rotation=40)

for nhan in ax.get_xticklabels():
    nhan.set_ha("right")

ax.bar_label(cot, fmt="%.2f", padding=3)
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)


# #9. HIỂN THỊ THÔNG TIN NGƯỜI TẠO Ở CUỐI TRANG
st.markdown("---")

st.markdown(
    f"<div style='text-align:center; font-size:12px; color:gray;'>"
    f"Người tạo ứng dụng: {TEN_NGUOI_TAO} | MSSV: {MSSV}"
    f"</div>",
    unsafe_allow_html=True
)
