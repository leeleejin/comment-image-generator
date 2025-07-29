import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(layout="centered")
st.title("💬 댓글 이미지 자동 생성기")

# 입력
bg_color = st.radio("배경 색상 선택", ("흰색", "검은색"))
nickname = st.text_input("닉네임을 입력하세요", value="닉네임")
meta = st.text_input("닉네임 옆에 붙는 설명", value="1일 전")
comment = st.text_area("댓글 내용을 입력하세요 (엔터 가능)")
uploaded_image = st.file_uploader("프로필 사진 업로드", type=["png", "jpg", "jpeg"])

if st.button("이미지 만들기"):
    # 폰트 설정
    font_path = "assets/PretendardVariable.ttf"
    font_nick = ImageFont.truetype(font_path, 17)
    font_meta = ImageFont.truetype(font_path, 17)
    font_comment = ImageFont.truetype(font_path, 20)

    # 패딩 설정
    padding_x = 20
    padding_y = 20
    profile_size = 40
    gap_between_lines = 6

    # 댓글 줄 단위 나누기
    lines = comment.split("\n")
    max_line_width = max(font_comment.getlength(line) for line in lines)
    comment_width = int(max_line_width)
    line_height = font_comment.size + gap_between_lines
    comment_height = line_height * len(lines)

    # 닉네임과 메타 정보
    nick_text = f"{nickname} · {meta}"
    nick_width = font_nick.getlength(nick_text)
    top_text_height = font_nick.size

    # 전체 이미지 크기 계산
    text_block_width = max(nick_width, comment_width)
    total_width = profile_size + 10 + text_block_width + 2 * padding_x
    total_height = max(profile_size, top_text_height + 10 + comment_height) + 2 * padding_y

    # 배경색 설정
    if bg_color == "흰색":
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)
    else:
        background_color = (0, 0, 0)
        text_color = (255, 255, 255)

    # 이미지 생성
    img = Image.new("RGBA", (total_width, total_height), background_color)
    draw = ImageDraw.Draw(img)

    # 프로필 그리기
    if uploaded_image:
        profile = Image.open(uploaded_image).convert("RGBA").resize((profile_size, profile_size))
        mask = Image.new("L", (profile_size, profile_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, profile_size, profile_size), fill=255)
        img.paste(profile, (padding_x, padding_y), mask)

    # 텍스트 블럭 위치
    text_start_x = padding_x + profile_size + 10
    text_start_y = padding_y

    # 닉네임 + 메타 정보
    draw.text((text_start_x, text_start_y), nick_text, font=font_nick, fill=text_color)

    # 댓글
    for i, line in enumerate(lines):
        y = text_start_y + top_text_height + 10 + i * line_height
        draw.text((text_start_x, y), line, font=font_comment, fill=text_color)

    # 출력 및 다운로드
    st.image(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(label="이미지 다운로드", data=byte_im, file_name="comment.png", mime="image/png")
