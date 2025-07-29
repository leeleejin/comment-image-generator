import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(layout="centered")
st.title("💬 댓글 이미지 자동 생성기")

# 입력 받기
bg_color = st.radio("배경 색상 선택", ("흰색", "검은색"))
nickname = st.text_input("닉네임을 입력하세요")
comment = st.text_area("댓글 내용을 입력하세요 (엔터 가능)")
uploaded_image = st.file_uploader("프로필 사진 업로드", type=["png", "jpg", "jpeg"])

if st.button("이미지 만들기"):
    # 글꼴 설정
    font_path = "assets/PretendardVariable.ttf"
    font_nick = ImageFont.truetype(font_path, 20)  # ✅ 여기 크기 20으로 변경
    font_comment = ImageFont.truetype(font_path, 20)

    # 여백 설정
    padding = 20  # 상하좌우 동일 여백
    profile_size = 40
    spacing = 10  # 닉네임과 댓글 사이

    # 색상 설정
    if bg_color == "흰색":
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)
    else:
        background_color = (0, 0, 0)
        text_color = (255, 255, 255)

    # 텍스트 줄 나누기
    lines = comment.split("\n")
    comment_line_height = font_comment.size + 6
    comment_height = len(lines) * comment_line_height

    max_line_width = max(font_comment.getlength(line) for line in lines)
    text_block_width = int(max(max_line_width, font_nick.getlength(nickname)))

    content_width = profile_size + spacing + text_block_width
    total_width = padding * 2 + content_width
    total_height = padding * 2 + max(profile_size, font_nick.size + spacing + comment_height)

    # 이미지 생성
    img = Image.new("RGBA", (total_width, total_height), background_color)
    draw = ImageDraw.Draw(img)

    # 프로필 이미지
    if uploaded_image:
        profile = Image.open(uploaded_image).convert("RGBA").resize((profile_size, profile_size))
        mask = Image.new("L", (profile_size, profile_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, profile_size, profile_size), fill=255)
        img.paste(profile, (padding, padding), mask)

    # 텍스트 위치 기준점
    text_x = padding + profile_size + spacing
    text_y = padding

    # 닉네임
    draw.text((text_x, text_y), nickname, font=font_nick, fill=text_color)

    # 댓글 텍스트
    for i, line in enumerate(lines):
        line_y = text_y + font_nick.size + spacing + i * comment_line_height
        draw.text((text_x, line_y), line, font=font_comment, fill=text_color)

    # 출력 및 다운로드
    st.image(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.download_button(label="이미지 다운로드", data=buf.getvalue(), file_name="comment.png", mime="image/png")
