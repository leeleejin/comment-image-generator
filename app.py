import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(layout="centered")
st.title("💬 댓글 이미지 자동 생성기")

# 입력
bg_color = st.radio("배경 색상 선택", ("흰색", "검은색"))
nickname = st.text_input("닉네임을 입력하세요")
comment = st.text_area("댓글 내용을 입력하세요 (엔터 가능)")
uploaded_image = st.file_uploader("프로필 사진 업로드", type=["png", "jpg", "jpeg"])

if st.button("이미지 만들기"):
    font_path = "assets/PretendardVariable.ttf"
    font_nick = ImageFont.truetype(font_path, 22)
    font_comment = ImageFont.truetype(font_path, 20)
    padding = 10
    left_margin = 60  # 프로필 포함 왼쪽 여백
    right_margin = 20

    # 색상 설정
    if bg_color == "흰색":
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)
    else:
        background_color = (0, 0, 0)
        text_color = (255, 255, 255)

    # 댓글 줄 처리
    lines = comment.split("\n")
    max_line_width = max(font_comment.getlength(line) for line in lines)
    text_width = int(max_line_width + padding * 2)

    line_height = font_comment.size + 6
    comment_box_height = line_height * len(lines) + padding * 2
    total_height = max(60 + comment_box_height, 80)
    total_width = left_margin + text_width + right_margin

    # 배경 이미지 생성
    img = Image.new("RGBA", (total_width, total_height), background_color)
    draw = ImageDraw.Draw(img)

    # 프로필
    if uploaded_image:
        profile = Image.open(uploaded_image).convert("RGBA").resize((40, 40))
        mask = Image.new("L", (40, 40), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 40, 40), fill=255)
        img.paste(profile, (10, 10), mask)

    # 닉네임
    draw.text((left_margin, 10), nickname, font=font_nick, fill=text_color)

    # 댓글 텍스트
    for i, line in enumerate(lines):
        draw.text((left_margin + padding, 40 + padding + i * line_height), line, font=font_comment, fill=text_color)

    # 출력 및 다운로드
    st.image(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(label="이미지 다운로드", data=byte_im, file_name="comment.png", mime="image/png")
