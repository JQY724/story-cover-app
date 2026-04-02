import os
import json
import zipfile
from io import BytesIO

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

st.set_page_config(page_title="商业实用版剧情封面编辑器", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================
# 字体
# =========================
def load_font(size=40, font_name="楷体"):
    font_map = {
        "楷体": [
            os.path.join(BASE_DIR, "fonts", "STKAITI.TTF"),
            os.path.join(BASE_DIR, "fonts", "stkaiti.ttf"),
        ],
        "黑体": [
            os.path.join(BASE_DIR, "fonts", "simhei.ttf"),
            os.path.join(BASE_DIR, "fonts", "SIMHEI.TTF"),
        ],
        "宋体": [
            os.path.join(BASE_DIR, "fonts", "simsun.ttc"),
            os.path.join(BASE_DIR, "fonts", "SIMSUN.TTC"),
        ],
        "默认": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
    }

    candidates = font_map.get(font_name, []) + [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]

    for fp in candidates:
        try:
            return ImageFont.truetype(fp, size=size)
        except:
            continue
    return ImageFont.load_default()


# =========================
# 模板
# =========================
def get_template_config(template_name):
    templates = {
        "经典剧情": {
            "canvas_w": 1080,
            "canvas_h": 1440,
            "top_x": 100,
            "top_y": 110,
            "top_max_width": 860,
            "top_font_size": 68,
            "subtitle_x": 100,
            "subtitle_y": 250,
            "subtitle_max_width": 860,
            "subtitle_font_size": 32,
            "bottom_x": 100,
            "bottom_y": 1120,
            "bottom_max_width": 860,
            "bottom_font_size": 48,
            "center_size": 620,
            "center_x": 230,
            "center_y": 330,
            "center_radius": 20,
            "center_feather": 40,
            "overlay_alpha": 55,
            "bg_blur": 0,
            "bg_brightness": 0.95,
            "avatar_size": 110,
            "avatar_x": 900,
            "avatar_y": 40,
        },
        "电影海报": {
            "canvas_w": 1080,
            "canvas_h": 1440,
            "top_x": 80,
            "top_y": 90,
            "top_max_width": 920,
            "top_font_size": 82,
            "subtitle_x": 80,
            "subtitle_y": 220,
            "subtitle_max_width": 920,
            "subtitle_font_size": 30,
            "bottom_x": 100,
            "bottom_y": 1180,
            "bottom_max_width": 860,
            "bottom_font_size": 40,
            "center_size": 700,
            "center_x": 190,
            "center_y": 300,
            "center_radius": 8,
            "center_feather": 28,
            "overlay_alpha": 95,
            "bg_blur": 1,
            "bg_brightness": 0.88,
            "avatar_size": 100,
            "avatar_x": 920,
            "avatar_y": 50,
        },
        "小红书爆款": {
            "canvas_w": 1080,
            "canvas_h": 1440,
            "top_x": 70,
            "top_y": 85,
            "top_max_width": 940,
            "top_font_size": 76,
            "subtitle_x": 75,
            "subtitle_y": 220,
            "subtitle_max_width": 930,
            "subtitle_font_size": 34,
            "bottom_x": 70,
            "bottom_y": 1140,
            "bottom_max_width": 940,
            "bottom_font_size": 52,
            "center_size": 660,
            "center_x": 210,
            "center_y": 305,
            "center_radius": 28,
            "center_feather": 36,
            "overlay_alpha": 65,
            "bg_blur": 0,
            "bg_brightness": 0.93,
            "avatar_size": 120,
            "avatar_x": 900,
            "avatar_y": 45,
        },
        "极简文艺": {
            "canvas_w": 1080,
            "canvas_h": 1440,
            "top_x": 120,
            "top_y": 150,
            "top_max_width": 780,
            "top_font_size": 58,
            "subtitle_x": 120,
            "subtitle_y": 250,
            "subtitle_max_width": 780,
            "subtitle_font_size": 28,
            "bottom_x": 120,
            "bottom_y": 1160,
            "bottom_max_width": 780,
            "bottom_font_size": 38,
            "center_size": 560,
            "center_x": 260,
            "center_y": 360,
            "center_radius": 36,
            "center_feather": 42,
            "overlay_alpha": 35,
            "bg_blur": 0,
            "bg_brightness": 1.0,
            "avatar_size": 96,
            "avatar_x": 920,
            "avatar_y": 52,
        },
    }
    return templates[template_name]


# =========================
# 默认配置
# =========================
def build_default_config(template_name="经典剧情"):
    tpl = get_template_config(template_name)
    return {
        "template_name": template_name,
        "use_template_size": True,
        "canvas_w": tpl["canvas_w"],
        "canvas_h": tpl["canvas_h"],

        "top_text": "她明明已经离开，却又出现在我的梦里",
        "subtitle_text": "悬疑 / 情感 / 反转",
        "bottom_text": "所有的真相，都藏在那张旧照片里。",

        "top_font_name": "楷体",
        "top_font_size": tpl["top_font_size"],
        "top_color": "#FFFFFF",
        "top_stroke_color": "#000000",
        "top_stroke_width": 3,
        "top_align": "left",
        "top_shadow": True,
        "top_x": tpl["top_x"],
        "top_y": tpl["top_y"],
        "top_max_width": tpl["top_max_width"],

        "show_subtitle": True,
        "subtitle_font_name": "黑体",
        "subtitle_font_size": tpl["subtitle_font_size"],
        "subtitle_color": "#F5E7C6",
        "subtitle_stroke_color": "#000000",
        "subtitle_stroke_width": 2,
        "subtitle_align": "left",
        "subtitle_shadow": False,
        "subtitle_x": tpl["subtitle_x"],
        "subtitle_y": tpl["subtitle_y"],
        "subtitle_max_width": tpl["subtitle_max_width"],

        "bottom_font_name": "黑体",
        "bottom_font_size": tpl["bottom_font_size"],
        "bottom_color": "#FFFFFF",
        "bottom_stroke_color": "#000000",
        "bottom_stroke_width": 2,
        "bottom_align": "left",
        "bottom_shadow": False,
        "bottom_x": tpl["bottom_x"],
        "bottom_y": tpl["bottom_y"],
        "bottom_max_width": tpl["bottom_max_width"],

        "show_avatar": True,
        "avatar_size": tpl["avatar_size"],
        "avatar_x": tpl["avatar_x"],
        "avatar_y": tpl["avatar_y"],
        "avatar_border_width": 4,
        "avatar_border_color": "#FFFFFF",
        "avatar_opacity": 255,

        "show_center": True,
        "center_size": tpl["center_size"],
        "center_x": tpl["center_x"],
        "center_y": tpl["center_y"],
        "center_feather": tpl["center_feather"],
        "center_radius": tpl["center_radius"],
        "center_shadow": True,
        "center_stroke_width": 0,
        "center_stroke_color": "#FFFFFF",

        "overlay_alpha": tpl["overlay_alpha"],
        "bg_blur": tpl["bg_blur"],
        "bg_brightness": tpl["bg_brightness"],

        "bottom_gradient": True,
        "bottom_gradient_height": 360,
        "bottom_gradient_alpha": 180,

        "badge_text": "剧情封面",
        "badge_x": 40,
        "badge_y": 40,
        "badge_bg_color": "#E53935",
        "badge_text_color": "#FFFFFF",

        "frame_width": 0,
        "frame_color": "#FFFFFF",
    }


# =========================
# 配置导出/导入
# =========================
def export_config_json(config):
    return json.dumps(config, ensure_ascii=False, indent=2)


def load_config_json(uploaded_file):
    content = uploaded_file.read().decode("utf-8")
    return json.loads(content)


# =========================
# 图像工具
# =========================
def crop_to_fill(img, target_size):
    tw, th = target_size
    w, h = img.size
    scale = max(tw / w, th / h)
    nw, nh = int(w * scale), int(h * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def add_overlay(img, alpha):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def add_blur(img, radius):
    if radius <= 0:
        return img
    return img.filter(ImageFilter.GaussianBlur(radius))


def adjust_brightness(img, factor):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def create_rounded_rectangle_mask(size, radius):
    w, h = size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    return mask


def create_shadow(size, radius=24, opacity=100, offset=(10, 12)):
    w, h = size
    shadow_w = w + abs(offset[0]) * 2 + radius * 2
    shadow_h = h + abs(offset[1]) * 2 + radius * 2
    shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))

    box = Image.new("RGBA", (w, h), (0, 0, 0, opacity))
    paste_x = radius + max(offset[0], 0)
    paste_y = radius + max(offset[1], 0)
    shadow.paste(box, (paste_x, paste_y))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius))
    return shadow


def add_bottom_gradient(img, height=360, max_alpha=180):
    img = img.convert("RGBA")
    w, h = img.size
    gradient = Image.new("L", (w, h), 0)
    px = gradient.load()
    start_y = max(0, h - height)

    for y in range(start_y, h):
        ratio = (y - start_y) / max(1, height)
        alpha = int(max_alpha * ratio)
        for x in range(w):
            px[x, y] = alpha

    black_layer = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    black_layer.putalpha(gradient)
    return Image.alpha_composite(img, black_layer)


def add_border(img, border_width=0, border_color="#FFFFFF"):
    if border_width <= 0:
        return img
    w, h = img.size
    canvas = Image.new("RGBA", (w + border_width * 2, h + border_width * 2), border_color)
    canvas.paste(img, (border_width, border_width), img)
    return canvas


# =========================
# 文本
# =========================
def wrap_text(draw, text, font, max_width):
    if not text:
        return []

    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch

    if current:
        lines.append(current)
    return lines


def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_multiline_text(
    draw,
    text,
    x,
    y,
    font,
    max_width,
    fill,
    stroke_fill,
    stroke_width,
    line_spacing=10,
    align="left",
    shadow=False,
    shadow_color=(0, 0, 0, 180),
    shadow_offset=(3, 3),
):
    if not text:
        return

    lines = wrap_text(draw, text, font, max_width)
    current_y = y

    for line in lines:
        line_w, line_h = get_text_size(draw, line, font)

        if align == "center":
            draw_x = x + (max_width - line_w) // 2
        elif align == "right":
            draw_x = x + max_width - line_w
        else:
            draw_x = x

        if shadow:
            draw.text(
                (draw_x + shadow_offset[0], current_y + shadow_offset[1]),
                line,
                font=font,
                fill=shadow_color,
            )

        draw.text(
            (draw_x, current_y),
            line,
            font=font,
            fill=fill,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )

        current_y += line_h + line_spacing


# =========================
# 头像
# =========================
def make_circle_avatar(img, size, border_width=4, border_color="white", opacity=255):
    img = crop_to_fill(img.convert("RGBA"), (size, size))

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)

    avatar = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    avatar.paste(img, (0, 0), mask)

    if opacity < 255:
        alpha = avatar.getchannel("A")
        alpha = alpha.point(lambda p: int(p * opacity / 255))
        avatar.putalpha(alpha)

    if border_width > 0:
        outer_size = size + border_width * 2
        border_canvas = Image.new("RGBA", (outer_size, outer_size), (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(border_canvas)
        border_draw.ellipse((0, 0, outer_size - 1, outer_size - 1), fill=border_color)
        border_canvas.paste(avatar, (border_width, border_width), avatar)
        return border_canvas

    return avatar


# =========================
# 中间主图
# =========================
def create_soft_square_image(img, size, feather=40, radius=0):
    square = crop_to_fill(img.convert("RGBA"), (size, size))

    if radius > 0:
        rounded_mask = create_rounded_rectangle_mask((size, size), radius)
    else:
        rounded_mask = Image.new("L", (size, size), 255)

    edge_mask = Image.new("L", (size, size), 255)
    px = edge_mask.load()

    for y in range(size):
        for x in range(size):
            dist_left = x
            dist_right = size - 1 - x
            dist_top = y
            dist_bottom = size - 1 - y
            edge_dist = min(dist_left, dist_right, dist_top, dist_bottom)

            if edge_dist < feather:
                alpha = int(255 * (edge_dist / feather))
                if alpha < px[x, y]:
                    px[x, y] = alpha

    edge_mask = edge_mask.filter(ImageFilter.GaussianBlur(radius=feather / 3))

    final_mask = Image.new("L", (size, size), 0)
    for y in range(size):
        for x in range(size):
            final_mask.putpixel(
                (x, y),
                min(rounded_mask.getpixel((x, y)), edge_mask.getpixel((x, y)))
            )

    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(square, (0, 0), final_mask)
    return result


def add_rect_stroke(img, stroke_width=0, stroke_color="#FFFFFF", radius=0):
    if stroke_width <= 0:
        return img

    w, h = img.size
    canvas = Image.new("RGBA", (w + stroke_width * 2, h + stroke_width * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (0, 0, w + stroke_width * 2 - 1, h + stroke_width * 2 - 1),
        radius=radius + stroke_width,
        outline=stroke_color,
        width=stroke_width
    )
    canvas.paste(img, (stroke_width, stroke_width), img)
    return canvas


# =========================
# 角标
# =========================
def draw_badge(draw, text, x, y, font, bg_color, text_color, padding_x=18, padding_y=10, radius=16):
    if not text:
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    box = (x, y, x + tw + padding_x * 2, y + th + padding_y * 2)
    draw.rounded_rectangle(box, radius=radius, fill=bg_color)
    draw.text((x + padding_x, y + padding_y - 2), text, font=font, fill=text_color)


# =========================
# 生成封面
# =========================
def generate_cover(bg_img, avatar_img, center_img, cfg):
    canvas_w = cfg["canvas_w"]
    canvas_h = cfg["canvas_h"]

    bg = crop_to_fill(bg_img.convert("RGBA"), (canvas_w, canvas_h))
    bg = add_blur(bg, cfg["bg_blur"])
    bg = adjust_brightness(bg, cfg["bg_brightness"])
    bg = add_overlay(bg, cfg["overlay_alpha"])

    if cfg["bottom_gradient"]:
        bg = add_bottom_gradient(bg, cfg["bottom_gradient_height"], cfg["bottom_gradient_alpha"])

    canvas = bg.copy()
    draw = ImageDraw.Draw(canvas)

    if cfg["show_center"] and center_img is not None:
        if cfg["center_shadow"]:
            shadow = create_shadow((cfg["center_size"], cfg["center_size"]), radius=28, opacity=110, offset=(10, 12))
            canvas.alpha_composite(shadow, (cfg["center_x"] - 28, cfg["center_y"] - 28))

        center_square = create_soft_square_image(
            center_img,
            cfg["center_size"],
            feather=cfg["center_feather"],
            radius=cfg["center_radius"]
        )

        if cfg["center_stroke_width"] > 0:
            center_square = add_rect_stroke(
                center_square,
                stroke_width=cfg["center_stroke_width"],
                stroke_color=cfg["center_stroke_color"],
                radius=cfg["center_radius"]
            )
            paste_x = cfg["center_x"] - cfg["center_stroke_width"]
            paste_y = cfg["center_y"] - cfg["center_stroke_width"]
        else:
            paste_x = cfg["center_x"]
            paste_y = cfg["center_y"]

        canvas.paste(center_square, (paste_x, paste_y), center_square)

    if cfg["show_avatar"] and avatar_img is not None:
        avatar = make_circle_avatar(
            avatar_img,
            size=cfg["avatar_size"],
            border_width=cfg["avatar_border_width"],
            border_color=cfg["avatar_border_color"],
            opacity=cfg["avatar_opacity"]
        )
        canvas.paste(avatar, (cfg["avatar_x"], cfg["avatar_y"]), avatar)

    top_font = load_font(cfg["top_font_size"], cfg["top_font_name"])
    subtitle_font = load_font(cfg["subtitle_font_size"], cfg["subtitle_font_name"])
    bottom_font = load_font(cfg["bottom_font_size"], cfg["bottom_font_name"])
    badge_font = load_font(26, "黑体")

    draw_multiline_text(
        draw=draw,
        text=cfg["top_text"],
        x=cfg["top_x"],
        y=cfg["top_y"],
        font=top_font,
        max_width=cfg["top_max_width"],
        fill=cfg["top_color"],
        stroke_fill=cfg["top_stroke_color"],
        stroke_width=cfg["top_stroke_width"],
        line_spacing=10,
        align=cfg["top_align"],
        shadow=cfg["top_shadow"],
    )

    if cfg["show_subtitle"]:
        draw_multiline_text(
            draw=draw,
            text=cfg["subtitle_text"],
            x=cfg["subtitle_x"],
            y=cfg["subtitle_y"],
            font=subtitle_font,
            max_width=cfg["subtitle_max_width"],
            fill=cfg["subtitle_color"],
            stroke_fill=cfg["subtitle_stroke_color"],
            stroke_width=cfg["subtitle_stroke_width"],
            line_spacing=8,
            align=cfg["subtitle_align"],
            shadow=cfg["subtitle_shadow"],
        )

    draw_multiline_text(
        draw=draw,
        text=cfg["bottom_text"],
        x=cfg["bottom_x"],
        y=cfg["bottom_y"],
        font=bottom_font,
        max_width=cfg["bottom_max_width"],
        fill=cfg["bottom_color"],
        stroke_fill=cfg["bottom_stroke_color"],
        stroke_width=cfg["bottom_stroke_width"],
        line_spacing=10,
        align=cfg["bottom_align"],
        shadow=cfg["bottom_shadow"],
    )

    if cfg["badge_text"]:
        draw_badge(
            draw,
            cfg["badge_text"],
            cfg["badge_x"],
            cfg["badge_y"],
            badge_font,
            cfg["badge_bg_color"],
            cfg["badge_text_color"]
        )

    canvas = add_border(canvas, cfg["frame_width"], cfg["frame_color"])
    return canvas


# =========================
# 工具函数
# =========================
def safe_open_image(uploaded_file):
    return Image.open(uploaded_file).convert("RGBA")


def image_to_png_bytes(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def build_output_filename(uploaded_name, prefix="cover"):
    if not uploaded_name:
        return f"{prefix}.png"
    base = os.path.splitext(os.path.basename(uploaded_name))[0]
    return f"{prefix}_{base}.png"


# =========================
# Session State 初始化
# =========================
if "config" not in st.session_state:
    st.session_state.config = build_default_config("经典剧情")

st.title("商业实用版剧情封面编辑器")
st.write("支持模板、配置保存/导入、批量生成、ZIP 打包下载。")

# =========================
# 导入配置
# =========================
st.sidebar.header("0. 配置导入 / 导出")
config_upload = st.sidebar.file_uploader("导入 JSON 配置", type=["json"])
if config_upload is not None:
    try:
        st.session_state.config = load_config_json(config_upload)
        st.sidebar.success("配置导入成功")
    except Exception as e:
        st.sidebar.error(f"配置导入失败：{e}")

cfg = st.session_state.config

template_name = st.sidebar.selectbox(
    "选择模板",
    ["经典剧情", "电影海报", "小红书爆款", "极简文艺"],
    index=["经典剧情", "电影海报", "小红书爆款", "极简文艺"].index(cfg.get("template_name", "经典剧情"))
)

if template_name != cfg.get("template_name"):
    st.session_state.config = build_default_config(template_name)
    cfg = st.session_state.config

config_json = export_config_json(cfg)
st.sidebar.download_button(
    label="下载当前配置 JSON",
    data=config_json.encode("utf-8"),
    file_name="cover_config.json",
    mime="application/json"
)

# =========================
# 上传素材
# =========================
st.sidebar.header("1. 上传素材")
bg_file = st.sidebar.file_uploader("上传背景图", type=["png", "jpg", "jpeg"])
avatar_file = st.sidebar.file_uploader("上传头像（可选）", type=["png", "jpg", "jpeg"])
center_files = st.sidebar.file_uploader(
    "上传中间主图（可多选，支持批量）",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# =========================
# 基础设置
# =========================
st.sidebar.header("2. 基础设置")
cfg["use_template_size"] = st.sidebar.checkbox("使用模板默认尺寸", value=cfg["use_template_size"])
if cfg["use_template_size"]:
    tpl = get_template_config(template_name)
    cfg["canvas_w"] = tpl["canvas_w"]
    cfg["canvas_h"] = tpl["canvas_h"]
else:
    cfg["canvas_w"] = st.sidebar.number_input("宽度", 400, 3000, int(cfg["canvas_w"]), 10)
    cfg["canvas_h"] = st.sidebar.number_input("高度", 400, 3000, int(cfg["canvas_h"]), 10)

# =========================
# 文本内容
# =========================
st.sidebar.header("3. 文本内容")
cfg["top_text"] = st.sidebar.text_area("主标题", value=cfg["top_text"])
cfg["show_subtitle"] = st.sidebar.checkbox("显示副标题", value=cfg["show_subtitle"])
cfg["subtitle_text"] = st.sidebar.text_area("副标题", value=cfg["subtitle_text"])
cfg["bottom_text"] = st.sidebar.text_area("底部文案", value=cfg["bottom_text"])

font_options = ["楷体", "黑体", "宋体", "默认"]

# =========================
# 主标题设置
# =========================
st.sidebar.header("4. 主标题设置")
cfg["top_font_name"] = st.sidebar.selectbox("主标题字体", font_options, index=font_options.index(cfg["top_font_name"]))
cfg["top_font_size"] = st.sidebar.slider("主标题字号", 20, 150, int(cfg["top_font_size"]))
cfg["top_color"] = st.sidebar.color_picker("主标题颜色", cfg["top_color"])
cfg["top_stroke_color"] = st.sidebar.color_picker("主标题描边颜色", cfg["top_stroke_color"])
cfg["top_stroke_width"] = st.sidebar.slider("主标题描边粗细", 0, 10, int(cfg["top_stroke_width"]))
cfg["top_align"] = st.sidebar.selectbox("主标题对齐", ["left", "center", "right"], index=["left", "center", "right"].index(cfg["top_align"]))
cfg["top_shadow"] = st.sidebar.checkbox("主标题阴影", value=cfg["top_shadow"])
cfg["top_x"] = st.sidebar.slider("主标题 X", 0, int(cfg["canvas_w"]), int(cfg["top_x"]))
cfg["top_y"] = st.sidebar.slider("主标题 Y", 0, int(cfg["canvas_h"]), int(cfg["top_y"]))
cfg["top_max_width"] = st.sidebar.slider("主标题最大宽度", 100, int(cfg["canvas_w"]), int(cfg["top_max_width"]))

# =========================
# 副标题设置
# =========================
st.sidebar.header("5. 副标题设置")
cfg["subtitle_font_name"] = st.sidebar.selectbox("副标题字体", font_options, index=font_options.index(cfg["subtitle_font_name"]))
cfg["subtitle_font_size"] = st.sidebar.slider("副标题字号", 16, 100, int(cfg["subtitle_font_size"]))
cfg["subtitle_color"] = st.sidebar.color_picker("副标题颜色", cfg["subtitle_color"])
cfg["subtitle_stroke_color"] = st.sidebar.color_picker("副标题描边颜色", cfg["subtitle_stroke_color"])
cfg["subtitle_stroke_width"] = st.sidebar.slider("副标题描边粗细", 0, 10, int(cfg["subtitle_stroke_width"]))
cfg["subtitle_align"] = st.sidebar.selectbox("副标题对齐", ["left", "center", "right"], index=["left", "center", "right"].index(cfg["subtitle_align"]))
cfg["subtitle_shadow"] = st.sidebar.checkbox("副标题阴影", value=cfg["subtitle_shadow"])
cfg["subtitle_x"] = st.sidebar.slider("副标题 X", 0, int(cfg["canvas_w"]), int(cfg["subtitle_x"]))
cfg["subtitle_y"] = st.sidebar.slider("副标题 Y", 0, int(cfg["canvas_h"]), int(cfg["subtitle_y"]))
cfg["subtitle_max_width"] = st.sidebar.slider("副标题最大宽度", 100, int(cfg["canvas_w"]), int(cfg["subtitle_max_width"]))

# =========================
# 底部文案设置
# =========================
st.sidebar.header("6. 底部文案设置")
cfg["bottom_font_name"] = st.sidebar.selectbox("底部字体", font_options, index=font_options.index(cfg["bottom_font_name"]))
cfg["bottom_font_size"] = st.sidebar.slider("底部字号", 20, 150, int(cfg["bottom_font_size"]))
cfg["bottom_color"] = st.sidebar.color_picker("底部颜色", cfg["bottom_color"])
cfg["bottom_stroke_color"] = st.sidebar.color_picker("底部描边颜色", cfg["bottom_stroke_color"])
cfg["bottom_stroke_width"] = st.sidebar.slider("底部描边粗细", 0, 10, int(cfg["bottom_stroke_width"]))
cfg["bottom_align"] = st.sidebar.selectbox("底部对齐", ["left", "center", "right"], index=["left", "center", "right"].index(cfg["bottom_align"]))
cfg["bottom_shadow"] = st.sidebar.checkbox("底部阴影", value=cfg["bottom_shadow"])
cfg["bottom_x"] = st.sidebar.slider("底部 X", 0, int(cfg["canvas_w"]), int(cfg["bottom_x"]))
cfg["bottom_y"] = st.sidebar.slider("底部 Y", 0, int(cfg["canvas_h"]), int(cfg["bottom_y"]))
cfg["bottom_max_width"] = st.sidebar.slider("底部最大宽度", 100, int(cfg["canvas_w"]), int(cfg["bottom_max_width"]))

# =========================
# 头像设置
# =========================
st.sidebar.header("7. 头像设置")
cfg["show_avatar"] = st.sidebar.checkbox("显示头像", value=cfg["show_avatar"])
cfg["avatar_size"] = st.sidebar.slider("头像大小", 50, 300, int(cfg["avatar_size"]))
cfg["avatar_x"] = st.sidebar.slider("头像 X", 0, int(cfg["canvas_w"]), int(cfg["avatar_x"]))
cfg["avatar_y"] = st.sidebar.slider("头像 Y", 0, int(cfg["canvas_h"]), int(cfg["avatar_y"]))
cfg["avatar_border_width"] = st.sidebar.slider("头像边框粗细", 0, 20, int(cfg["avatar_border_width"]))
cfg["avatar_border_color"] = st.sidebar.color_picker("头像边框颜色", cfg["avatar_border_color"])
cfg["avatar_opacity"] = st.sidebar.slider("头像透明度", 50, 255, int(cfg["avatar_opacity"]))

# =========================
# 主图设置
# =========================
st.sidebar.header("8. 主图设置")
cfg["show_center"] = st.sidebar.checkbox("显示主图", value=cfg["show_center"])
cfg["center_size"] = st.sidebar.slider("主图大小", 200, min(int(cfg["canvas_w"]), int(cfg["canvas_h"])), int(cfg["center_size"]))
cfg["center_x"] = st.sidebar.slider("主图 X", 0, int(cfg["canvas_w"]), int(cfg["center_x"]))
cfg["center_y"] = st.sidebar.slider("主图 Y", 0, int(cfg["canvas_h"]), int(cfg["center_y"]))
cfg["center_feather"] = st.sidebar.slider("边缘融入程度", 5, 120, int(cfg["center_feather"]))
cfg["center_radius"] = st.sidebar.slider("主图圆角", 0, 120, int(cfg["center_radius"]))
cfg["center_shadow"] = st.sidebar.checkbox("主图阴影", value=cfg["center_shadow"])
cfg["center_stroke_width"] = st.sidebar.slider("主图描边粗细", 0, 20, int(cfg["center_stroke_width"]))
cfg["center_stroke_color"] = st.sidebar.color_picker("主图描边颜色", cfg["center_stroke_color"])

# =========================
# 背景设置
# =========================
st.sidebar.header("9. 背景设置")
cfg["overlay_alpha"] = st.sidebar.slider("背景压暗程度", 0, 200, int(cfg["overlay_alpha"]))
cfg["bg_blur"] = st.sidebar.slider("背景模糊", 0, 10, int(cfg["bg_blur"]))
cfg["bg_brightness"] = st.sidebar.slider("背景亮度", 0.3, 1.5, float(cfg["bg_brightness"]), 0.05)

# =========================
# 渐变、角标、外框
# =========================
st.sidebar.header("10. 底部渐变")
cfg["bottom_gradient"] = st.sidebar.checkbox("启用底部渐变", value=cfg["bottom_gradient"])
cfg["bottom_gradient_height"] = st.sidebar.slider("渐变高度", 100, int(cfg["canvas_h"]), int(cfg["bottom_gradient_height"]))
cfg["bottom_gradient_alpha"] = st.sidebar.slider("渐变最深透明度", 0, 255, int(cfg["bottom_gradient_alpha"]))

st.sidebar.header("11. 角标设置")
cfg["badge_text"] = st.sidebar.text_input("角标文字", value=cfg["badge_text"])
cfg["badge_x"] = st.sidebar.slider("角标 X", 0, int(cfg["canvas_w"]), int(cfg["badge_x"]))
cfg["badge_y"] = st.sidebar.slider("角标 Y", 0, int(cfg["canvas_h"]), int(cfg["badge_y"]))
cfg["badge_bg_color"] = st.sidebar.color_picker("角标背景色", cfg["badge_bg_color"])
cfg["badge_text_color"] = st.sidebar.color_picker("角标文字色", cfg["badge_text_color"])

st.sidebar.header("12. 外框设置")
cfg["frame_width"] = st.sidebar.slider("外框粗细", 0, 50, int(cfg["frame_width"]))
cfg["frame_color"] = st.sidebar.color_picker("外框颜色", cfg["frame_color"])

# 同步模板名
cfg["template_name"] = template_name
st.session_state.config = cfg

# =========================
# 生成逻辑
# =========================
bg_img = safe_open_image(bg_file) if bg_file is not None else None
avatar_img = safe_open_image(avatar_file) if avatar_file is not None else None

preview_center_img = None
if center_files and len(center_files) > 0:
    preview_center_img = safe_open_image(center_files[0])

if bg_img is not None and preview_center_img is not None:
    preview_result = generate_cover(bg_img, avatar_img, preview_center_img, cfg)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("素材预览")
        st.image(bg_img, caption="背景图", use_container_width=True)
        st.image(preview_center_img, caption="主图预览（第一张）", use_container_width=True)
        if avatar_img is not None:
            st.image(avatar_img, caption="头像", use_container_width=True)

    with col2:
        st.subheader("封面预览")
        st.image(preview_result, use_container_width=True)

    st.subheader("导出")
    single_png = image_to_png_bytes(preview_result)
    st.download_button(
        label="下载当前预览 PNG",
        data=single_png,
        file_name="preview_cover.png",
        mime="image/png"
    )

    if center_files:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for i, cfile in enumerate(center_files, start=1):
                try:
                    cimg = Image.open(cfile).convert("RGBA")
                    result = generate_cover(bg_img, avatar_img, cimg, cfg)
                    png_bytes = image_to_png_bytes(result)
                    output_name = build_output_filename(cfile.name, prefix=f"cover_{i}")
                    zf.writestr(output_name, png_bytes)
                except Exception as e:
                    error_name = f"error_{i}.txt"
                    zf.writestr(error_name, f"{cfile.name} 生成失败：{e}")

        st.download_button(
            label="批量下载 ZIP",
            data=zip_buffer.getvalue(),
            file_name="batch_covers.zip",
            mime="application/zip"
        )

        st.success(f"已准备 {len(center_files)} 张主图的批量导出 ZIP。")
else:
    st.info("请至少上传 1 张背景图和 1 张主图。头像可选。")