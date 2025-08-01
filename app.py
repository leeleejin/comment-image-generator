import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(layout="centered")
st.title("💬 유튜브 댓글 이미지 생성기")

# ===== 입력 =====
bg_color = st.radio("배경 색상 선택", ("흰색", "검은색"))
nickname = st.text_input("닉네임 입력")
meta = st.text_input("작성일 입력 (예: 1일 전)")
comment = st.text_area("댓글 내용을 입력하세요 (엔터 가능)")
uploaded_image = st.file_uploader("프로필 사진 업로드", type=["png", "jpg", "jpeg"])

if st.button("이미지 만들기"):
    # ===== 폰트 설정 =====
    font_path = "assets/PretendardVariable.ttf"
    font_nick = ImageFont.truetype(font_path, 17)
    font_meta = ImageFont.truetype(font_path, 17)
    font_comment = ImageFont.truetype(font_path, 20)

    # ===== 패딩 & 레이아웃 설정 =====
    padding_x = 20
    padding_y = 20
    profile_size = 40
    gap_between_lines = 6

    # 댓글 줄 나누기
    lines = comment.split("\n")
    max_line_width = max(font_comment.getlength(line) for line in lines) if lines else 0
    comment_width = int(max_line_width)
    line_height = font_comment.size + gap_between_lines
    comment_height = line_height * len(lines)

    # 닉네임 + 작성일
    nick_text = f"{nickname} · {meta}"
    nick_width = int(font_nick.getlength(nick_text))
    top_text_height = font_nick.size

    # 전체 이미지 크기 계산
    text_block_width = max(nick_width, comment_width)
    total_width = int(profile_size + 10 + text_block_width + 2 * padding_x)
    total_height = int(max(profile_size, top_text_height + 10 + comment_height) + 2 * padding_y)

    # ===== 배경 색상 설정 =====
    if bg_color == "흰색":
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)
    elif bg_color == "검은색":
        background_color = (0, 0, 0)
        text_color = (255, 255, 255)
    else:
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)

    # ===== RGBA 값 확인 및 생성 =====
    if isinstance(background_color, tuple) and len(background_color) == 3:
        try:
            bg_rgba = background_color + (255,)
        except Exception as e:
            st.error(f"RGBA 생성 실패: {e}")
            st.stop()
    else:
        st.error(f"잘못된 background_color 값: {background_color}")
        st.stop()

    # ===== 이미지 생성 =====
    try:
        img = Image.new("RGBA", (total_width, total_height), bg_rgba)
    except Exception as e:
        st.error(f"이미지 생성 실패: {e}")
        st.stop()

    draw = ImageDraw.Draw(img)

    # ===== 프로필 이미지 =====
    if uploaded_image:
        try:
            profile = Image.open(uploaded_image).convert("RGBA").resize((profile_size, profile_size))
            mask = Image.new("L", (profile_size, profile_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, profile_size, profile_size), fill=255)
            img.paste(profile, (padding_x, padding_y), mask)
        except Exception as e:
            st.warning(f"프로필 이미지 처리 실패: {e}")

    # 텍스트 시작 위치
    text_start_x = padding_x + profile_size + 10
    text_start_y = padding_y

    # 닉네임 + 작성일
    draw.text((text_start_x, text_start_y), nick_text, font=font_nick, fill=text_color)

    # 댓글 줄단위 출력
    for i, line in enumerate(lines):
        y = text_start_y + top_text_height + 10 + i * line_height
        draw.text((text_start_x, y), line, font=font_comment, fill=text_color)

    # ===== 이미지 출력 & 다운로드 =====
    st.image(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(label="이미지 다운로드", data=byte_im, file_name="comment.png", mime="image/png")
