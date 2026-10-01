import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _list(name: str, default: str) -> list[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]


@dataclass(frozen=True)
class Config:
    anthropic_model: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
    ig_user_id: str = os.getenv("IG_USER_ID", "")
    ig_token: str = os.getenv("IG_ACCESS_TOKEN", "")
    graph_version: str = os.getenv("GRAPH_VERSION", "v23.0")
    media_dir: str = os.getenv("MEDIA_DIR", "data/public")
    public_base_url: str = os.getenv("PUBLIC_MEDIA_BASE_URL", "").rstrip("/")
    db_path: str = os.getenv("DB_PATH", "data/robo.db")
    nome: str = os.getenv("ADVOGADO_NOME", "Lucas Palhares")
    oab: str = os.getenv("ADVOGADO_OAB", "OAB/RO 11.037")
    cidade: str = os.getenv("CIDADE", "Ji-Paraná/RO")
    areas: list[str] = field(default_factory=lambda: _list(
        "AREAS", "saúde,previdenciário,consumidor e bancário,civil e imobiliário,trabalhista,tributário"))
    post_hours: list[int] = field(default_factory=lambda: [int(h) for h in _list("POST_HOURS", "11,19")])
    timezone: str = os.getenv("TIMEZONE", "America/Porto_Velho")
    brand_bg: str = os.getenv("BRAND_BG", "#0F1B2D")
    brand_fg: str = os.getenv("BRAND_FG", "#F5F1E8")
    brand_accent: str = os.getenv("BRAND_ACCENT", "#C9A24B")
    logo_path: str = os.getenv("LOGO_PATH", "assets/logo.png")
    font_bold: str = os.getenv("FONT_BOLD", "")
    font_regular: str = os.getenv("FONT_REGULAR", "")
    telegram_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat: str = os.getenv("TELEGRAM_CHAT_ID", "")

    app_secret: str = os.getenv("META_APP_SECRET", "")
    verify_token: str = os.getenv("WEBHOOK_VERIFY_TOKEN", "")
    whatsapp_url: str = os.getenv("WHATSAPP_URL", "")
    max_bot_replies: int = int(os.getenv("MAX_BOT_REPLIES", "10"))

    eleven_key: str = os.getenv("ELEVENLABS_API_KEY", "")
    eleven_voice: str = os.getenv("ELEVENLABS_VOICE_ID", "")
    heygen_key: str = os.getenv("HEYGEN_API_KEY", "")
    heygen_avatar: str = os.getenv("HEYGEN_AVATAR_ID", "")

    week_mix: str = os.getenv("WEEK_MIX", "carousel:3,reel:2,story:7")
    feed_per_day: int = int(os.getenv("FEED_PER_DAY", "1"))
    stories_per_day: int = int(os.getenv("STORIES_PER_DAY", "2"))
    window_start: int = int(os.getenv("WINDOW_START", "7"))
    window_end: int = int(os.getenv("WINDOW_END", "22"))
    explore: float = float(os.getenv("EXPLORE", "0.2"))
    review_all: bool = os.getenv("REVIEW_ALL", "true").strip().lower() != "false"

    @property
    def mix(self) -> dict[str, int]:
        return {k.strip(): int(v) for k, v in (x.split(":") for x in self.week_mix.split(",") if ":" in x)}

    @property
    def footer(self) -> str:
        return f"{self.nome} | {self.oab} | {self.cidade}"
