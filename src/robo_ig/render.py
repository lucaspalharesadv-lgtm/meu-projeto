import os

from PIL import Image, ImageDraw, ImageFont

from .config import Config

W, H = 1080, 1350
MARGIN = 90


def _font(path: str, fallback: str, size: int) -> ImageFont.FreeTypeFont:
    for candidate in (path, fallback):
        if candidate:
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                continue
    return ImageFont.load_default(size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line] if line else lines


def _draw_block(draw, text, font, y, fill, max_w=W - 2 * MARGIN, spacing=1.25) -> int:
    for line in _wrap(draw, text, font, max_w):
        draw.text((MARGIN, y), line, font=font, fill=fill)
        y += int(font.size * spacing)
    return y


def render_post(cfg: Config, post_id: int, hook: str, slides: list[dict], fmt: str) -> list[str]:
    bold = lambda s: _font(cfg.font_bold, "DejaVuSans-Bold.ttf", s)
    regular = lambda s: _font(cfg.font_regular, "DejaVuSans.ttf", s)
    logo = Image.open(cfg.logo_path).convert("RGBA") if os.path.exists(cfg.logo_path) else None
    if logo:
        logo.thumbnail((200, 120))

    pages = [{"title": hook, "body": "", "cover": True}] if fmt == "carousel" else []
    pages += slides
    if fmt == "carousel":
        pages.append({"title": "Gostou? Salve e compartilhe.", "body": cfg.footer, "closing": True})

    out_dir = os.path.join(cfg.media_dir, f"post_{post_id}")
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, page in enumerate(pages, 1):
        img = Image.new("RGB", (W, H), cfg.brand_bg)
        d = ImageDraw.Draw(img)
        d.rectangle([MARGIN, 120, MARGIN + 90, 128], fill=cfg.brand_accent)
        title_size = 78 if page.get("cover") else 56
        y = _draw_block(d, page["title"], bold(title_size), 190 if not page.get("cover") else 420, cfg.brand_accent
                        if page.get("cover") else cfg.brand_fg)
        if page["body"]:
            _draw_block(d, page["body"], regular(40), y + 40, cfg.brand_fg)
        d.text((MARGIN, H - 110), f"{i}/{len(pages)}", font=regular(30), fill=cfg.brand_accent)
        if logo:
            img.paste(logo, (W - MARGIN - logo.width, H - 130), logo)
        path = os.path.join(out_dir, f"{i:02d}.jpg")
        img.save(path, "JPEG", quality=92)
        paths.append(path)
    return paths


SW, SH = 1080, 1920
SAFE_TOP, SAFE_BOTTOM = 260, 360


def render_story(cfg: Config, post_id: int, frames: list[dict]) -> list[str]:
    """Stories 9:16 respeitando as zonas de interface do app; identificação do advogado em cada quadro."""
    bold = lambda s: _font(cfg.font_bold, "DejaVuSans-Bold.ttf", s)
    regular = lambda s: _font(cfg.font_regular, "DejaVuSans.ttf", s)
    logo = Image.open(cfg.logo_path).convert("RGBA") if os.path.exists(cfg.logo_path) else None
    if logo:
        logo.thumbnail((220, 130))
    out_dir = os.path.join(cfg.media_dir, f"post_{post_id}")
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, fr in enumerate(frames, 1):
        img = Image.new("RGB", (SW, SH), cfg.brand_bg)
        d = ImageDraw.Draw(img)
        d.rectangle([MARGIN, SAFE_TOP, MARGIN + 100, SAFE_TOP + 10], fill=cfg.brand_accent)
        y = _draw_block(d, fr["title"], bold(76), SAFE_TOP + 90, cfg.brand_accent, max_w=SW - 2 * MARGIN)
        if fr.get("body"):
            _draw_block(d, fr["body"], regular(46), y + 50, cfg.brand_fg, max_w=SW - 2 * MARGIN)
        d.text((MARGIN, SH - SAFE_BOTTOM + 40), cfg.footer, font=regular(30), fill=cfg.brand_accent)
        if logo:
            img.paste(logo, (SW - MARGIN - logo.width, SAFE_TOP - 40), logo)
        path = os.path.join(out_dir, f"story_{i:02d}.jpg")
        img.save(path, "JPEG", quality=92)
        paths.append(path)
    return paths
