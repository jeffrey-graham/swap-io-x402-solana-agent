#!/usr/bin/env python3
"""
Generates 4 high-resolution infographic cards (`output/card_1_overview.png` .. `output/card_4_strategy.png`)
and a 45-second 1080p MP4 video walkthrough (`output/panta_nectarfi_reel.mp4`) for the
Panta x NectarFi Trading Competition Bounty (`#PantaMarkets`).
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT_DIR / "output"
VIDEO_PATH = OUT_DIR / "panta_nectarfi_reel.mp4"

WIDTH, HEIGHT = 1920, 1080

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def fnt(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def draw_frame(img: Image.Image, card_idx: int, badge_text: str) -> ImageDraw.ImageDraw:
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(9, 13, 22))
    for x in range(0, WIDTH, 64):
        draw.line([(x, 0), (x, HEIGHT)], fill=(17, 24, 39), width=1)
    for y in range(0, HEIGHT, 64):
        draw.line([(0, y), (WIDTH, y)], fill=(17, 24, 39), width=1)

    # Top accent bar: NectarFi Gold + Panta Emerald + Solana Purple
    draw.rectangle([0, 0, 640, 8], fill=(245, 158, 11))
    draw.rectangle([640, 0, 1280, 8], fill=(20, 241, 149))
    draw.rectangle([1280, 0, WIDTH, 8], fill=(153, 69, 255))

    # Top header pills
    draw.rounded_rectangle([60, 36, 510, 86], radius=12, fill=(28, 24, 14), outline=(245, 158, 11), width=2)
    draw.text((84, 48), "PANTA  x  NECTARFI  •  #PantaMarkets", font=fnt(FONT_BOLD, 21), fill=(255, 200, 75))

    draw.rounded_rectangle([535, 36, 1045, 86], radius=12, fill=(14, 34, 32), outline=(20, 241, 149), width=2)
    draw.text((560, 49), badge_text, font=fnt(FONT_MONO_BOLD, 19), fill=(20, 241, 149))

    draw.rounded_rectangle([1430, 36, 1860, 86], radius=12, fill=(22, 20, 44), outline=(153, 69, 255), width=2)
    draw.text((1455, 49), f"CARD 0{card_idx} / 04  •  500 USDG POOL", font=fnt(FONT_MONO_BOLD, 19), fill=(216, 180, 254))

    # Footer
    draw.rectangle([0, 1015, WIDTH, HEIGHT], fill=(7, 10, 18))
    draw.line([(0, 1015), (WIDTH, 1015)], fill=(38, 53, 84), width=2)
    draw.text(
        (60, 1033),
        "@PantaHQ  ×  @Nectar_finance  ×  @SuperteamNG   |   #PantaMarkets Trading Competition Strategy Pack",
        font=fnt(FONT_MONO, 19),
        fill=(148, 163, 184),
    )
    draw.text(
        (1450, 1033),
        "5 Winners × 100 USDG Equal Split",
        font=fnt(FONT_BOLD, 19),
        fill=(245, 158, 11),
    )
    return draw


def make_card_1() -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = draw_frame(img, 1, "THE CONVERGENCE: YIELD + PREDICTION MARKETS")

    draw.text(
        (60, 118),
        "Why Panta x NectarFi Changes On-Chain Prediction Markets",
        font=fnt(FONT_BOLD, 46),
        fill=(255, 255, 255),
    )
    draw.text(
        (60, 180),
        "Stop letting stablecoins sit idle between event catalysts. Combine NectarFi USDG yield with Panta conviction.",
        font=fnt(FONT_REG, 25),
        fill=(180, 200, 226),
    )

    # 3 Pillars
    pillars = [
        (
            60,
            620,
            "1. NECTARFI USDG YIELD BASE",
            (245, 158, 11),
            [
                "• Productive USDG Vaults:",
                "  Earn 14%–16.5% APY on core USDG",
                "  liquidity while waiting for setups.",
                "• Zero Idle Drag:",
                "  Traditional prediction traders suffer",
                "  0% yield on unallocated dry powder.",
                "• Instant Liquidity:",
                "  Rotate accrued USDG yield directly",
                "  into high-edge Panta event markets.",
            ],
        ),
        (
            680,
            1240,
            "2. PANTA PREDICTION MARKETS",
            (20, 241, 149),
            [
                "• Binary YES / NO Event Contracts:",
                "  Trade crypto, macro, cultural, and",
                "  Solana ecosystem outcomes ($0.01–$0.99).",
                "• Transparent Orderbook & Pricing:",
                "  Contract price = market-implied",
                "  probability (e.g., $0.42 = 42% odds).",
                "• Asymmetric Payoff Profile:",
                "  2.38x–3.50x payouts when your research",
                "  spots mispriced consensus odds.",
            ],
        ),
        (
            1300,
            1860,
            "3. THE USDG BARBELL EDGE",
            (0, 194, 255),
            [
                "• Yield-Financed Risk Taking:",
                "  Let NectarFi vault yield subsidize or",
                "  fully cover your Panta contract stakes.",
                "• Higher Sharpe Ratio:",
                "  Smooth out binary variance with steady",
                "  daily USDG yield accrual.",
                "• Competition Multiplier:",
                "  Maximize risk-adjusted ROI across the",
                "  Panta x NectarFi Trading Competition.",
            ],
        ),
    ]

    for x1, x2, title, color, lines in pillars:
        draw.rounded_rectangle([x1, 248, x2, 795], radius=18, fill=(16, 24, 40), outline=color, width=3)
        draw.rounded_rectangle([x1 + 24, 274, x2 - 24, 330], radius=10, fill=(24, 36, 60))
        draw.text((x1 + 40, 288), title, font=fnt(FONT_BOLD, 22), fill=color)
        ly = 362
        for line in lines:
            bold = line.startswith("•")
            draw.text(
                (x1 + 32, ly),
                line,
                font=fnt(FONT_BOLD if bold else FONT_REG, 21),
                fill=(245, 248, 255) if bold else (185, 205, 230),
            )
            ly += 42

    draw.rounded_rectangle([60, 825, 1860, 985], radius=16, fill=(20, 32, 54), outline=(245, 158, 11), width=2)
    draw.text(
        (95, 852),
        "CORE THESIS: NectarFi turns your USDG bankroll into a yield-generating engine; Panta turns your information",
        font=fnt(FONT_BOLD, 24),
        fill=(255, 215, 110),
    )
    draw.text(
        (95, 892),
        "edge into asymmetric upside. Together, they form the ultimate Solana prediction-market barbell.",
        font=fnt(FONT_BOLD, 24),
        fill=(20, 241, 149),
    )
    draw.text(
        (95, 936),
        "Interactive Calculator Included: `panta_nectarfi_dashboard.html`  |  Tag @PantaHQ @Nectar_finance @SuperteamNG #PantaMarkets",
        font=fnt(FONT_MONO, 19),
        fill=(180, 210, 245),
    )

    out = OUT_DIR / "card_1_overview.png"
    img.save(out)
    return out


def make_card_2() -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = draw_frame(img, 2, "QUANTITATIVE EV & KELLY SIZING FRAMEWORK")

    draw.text(
        (60, 118),
        "How Smart Traders Price Edge on #PantaMarkets",
        font=fnt(FONT_BOLD, 46),
        fill=(255, 255, 255),
    )
    draw.text(
        (60, 180),
        "Expected Value (EV) math + Half-Kelly position sizing on a $2,500 USDG competition bankroll.",
        font=fnt(FONT_REG, 25),
        fill=(180, 200, 226),
    )

    # Left Box: The Math
    draw.rounded_rectangle([60, 248, 930, 895], radius=18, fill=(14, 22, 38), outline=(0, 194, 255), width=3)
    draw.rounded_rectangle([90, 276, 900, 332], radius=10, fill=(20, 38, 66))
    draw.text((112, 290), "BINARY CONTRACT EXPECTED VALUE & KELLY FORMULA", font=fnt(FONT_BOLD, 22), fill=(0, 215, 255))

    math_blocks = [
        ("1. Market-Implied Probability (c):", "Contract Price = $0.42  ->  Implied Odds = 42.0%"),
        ("2. Subjective Research Probability (p):", "On-chain data & catalyst model estimates p = 60.0% (+18% Edge)"),
        ("3. Expected Value per $1.00 Contract:", "EV = (p / c) - 1 = (0.60 / 0.42) - 1 = +42.86% ROI per trade"),
        ("4. Full Kelly Fraction (f*):", "f* = (p - c) / (1 - c) = (0.60 - 0.42) / 0.58 = 31.03% of bankroll"),
        ("5. Competition Barbell Allocation:", "75% NectarFi USDG Vault ($1,875) + 25% Panta YES ($625)"),
    ]
    my = 360
    for m_title, m_val in math_blocks:
        draw.rounded_rectangle([90, my, 900, my + 90], radius=12, fill=(18, 30, 52), outline=(45, 75, 115), width=1)
        draw.text((112, my + 14), m_title, font=fnt(FONT_BOLD, 20), fill=(20, 241, 149))
        draw.text((112, my + 48), m_val, font=fnt(FONT_MONO, 19), fill=(235, 242, 255))
        my += 104

    # Right Box: Worked $2,500 USDG Portfolio Payoff Table
    draw.rounded_rectangle([970, 248, 1860, 895], radius=18, fill=(16, 24, 40), outline=(20, 241, 149), width=3)
    draw.rounded_rectangle([1000, 276, 1830, 332], radius=10, fill=(18, 52, 46))
    draw.text((1022, 290), "$2,500 USDG BARBELL PAYOFF MATRIX (30-DAY WINDOW)", font=fnt(FONT_BOLD, 22), fill=(20, 241, 149))

    cards_right = [
        ("IF PANTA MARKET RESOLVES YES ($1.00)", "+$886.21 USDG (+35.4% Total Return)", "NectarFi Vault: $1,898.12  +  Panta Payout: $1,488.10", (20, 241, 149)),
        ("PORTFOLIO EXPECTED VALUE (AT p = 60%)", "+$291.19 USDG (+11.65% 30-Day EV)", "NectarFi Yield: +$23.12  +  Panta EV: +$268.07", (0, 215, 255)),
        ("IF PANTA MARKET RESOLVES NO ($0.00)", "NectarFi Yield Softens Drawdown", "$1,898.12 Preserved ($1,875 Principal + $23.12 USDG Yield)", (245, 158, 11)),
    ]
    ry = 365
    for r_title, r_big, r_sub, col in cards_right:
        draw.rounded_rectangle([1000, ry, 1830, ry + 155], radius=14, fill=(20, 32, 54), outline=col, width=2)
        draw.text((1025, ry + 18), r_title, font=fnt(FONT_MONO_BOLD, 18), fill=col)
        draw.text((1025, ry + 55), r_big, font=fnt(FONT_BOLD, 30), fill=(255, 255, 255))
        draw.text((1025, ry + 105), r_sub, font=fnt(FONT_REG, 20), fill=(185, 205, 235))
        ry += 172

    draw.rounded_rectangle([60, 918, 1860, 990], radius=14, fill=(22, 34, 58), outline=(0, 194, 255), width=2)
    draw.text(
        (95, 940),
        "PRO TIP: Never go 100% all-in on a single binary contract. Half-Kelly + NectarFi USDG yield keeps you in the game.",
        font=fnt(FONT_BOLD, 23),
        fill=(0, 224, 255),
    )

    out = OUT_DIR / "card_2_ev_math.png"
    img.save(out)
    return out


def make_card_3() -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = draw_frame(img, 3, "ZERO-LOSS PRINCIPAL GUARD STRATEGY")

    draw.text(
        (60, 118),
        "The 'House-Money' Loop: 100% Principal-Protected Bets",
        font=fnt(FONT_BOLD, 46),
        fill=(255, 255, 255),
    )
    draw.text(
        (60, 180),
        "How conservative treasuries & whales trade on @PantaHQ with zero principal risk using @Nectar_finance.",
        font=fnt(FONT_REG, 25),
        fill=(180, 200, 226),
    )

    # 4 Step Horizontal Flow
    flow = [
        ("STEP 1: DEPOSIT", "$5,000 USDG", "Lock core capital in NectarFi USDG Yield Vault at 16.5% APY.", (245, 158, 11)),
        ("STEP 2: HARVEST", "+$101.71 USDG", "Accrue 45 days of risk-adjusted USDG yield automatically.", (0, 194, 255)),
        ("STEP 3: DEPLOY", "290.6 YES Shares", "Route ONLY the $101.71 yield into a $0.35 Panta catalyst market.", (153, 69, 255)),
        ("STEP 4: SETTLE", "$5,000 Floor", "If NO: keep 100% of $5,000. If YES: collect $5,290.60 (+5.81%)!", (20, 241, 149)),
    ]
    fx = 60
    for st, big, desc, col in flow:
        draw.rounded_rectangle([fx, 250, fx + 425, 575], radius=18, fill=(15, 24, 42), outline=col, width=3)
        draw.text((fx + 30, 280), st, font=fnt(FONT_MONO_BOLD, 20), fill=col)
        draw.text((fx + 30, 330), big, font=fnt(FONT_BOLD, 44), fill=(255, 255, 255))
        # wrap desc manually
        words = desc.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) <= 28:
                cur = (cur + " " + w).strip()
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        dy = 415
        for ln in lines:
            draw.text((fx + 30, dy), ln, font=fnt(FONT_REG, 22), fill=(195, 215, 240))
            dy += 34
        fx += 450

    # Comparison Banner
    draw.rounded_rectangle([60, 610, 1860, 980], radius=18, fill=(14, 22, 38), outline=(20, 241, 149), width=2)
    draw.text(
        (95, 638),
        "WHY THIS WINS THE PANTA x NECTARFI TRADING COMPETITION:",
        font=fnt(FONT_BOLD, 25),
        fill=(20, 241, 149),
    )
    reasons = [
        ("1. Asymmetric Psychological Edge:", "Traders using yield-financed 'house money' never panic-sell during noisy intraday odds swings."),
        ("2. Continuous Shot Generation:", "Every epoch of NectarFi USDG yield reloads your Panta prediction market ammo automatically."),
        ("3. Composable Solana DeFi UX:", "Both NectarFi and Panta settle natively in USDG with sub-second finality and near-zero gas fees."),
    ]
    ry = 695
    for r_head, r_body in reasons:
        draw.rounded_rectangle([95, ry, 1825, ry + 76], radius=12, fill=(20, 34, 58), outline=(45, 75, 115), width=1)
        draw.text((120, ry + 14), r_head, font=fnt(FONT_BOLD, 21), fill=(245, 158, 11))
        draw.text((525, ry + 14), r_body, font=fnt(FONT_REG, 21), fill=(230, 240, 255))
        ry += 90

    out = OUT_DIR / "card_3_zero_loss_loop.png"
    img.save(out)
    return out


def make_card_4() -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = draw_frame(img, 4, "COMPETITION PLAYBOOK & DASHBOARD WALKTHROUGH")

    draw.text(
        (60, 118),
        "3-Step Competition Playbook + Interactive EV Calculator",
        font=fnt(FONT_BOLD, 46),
        fill=(255, 255, 255),
    )
    draw.text(
        (60, 180),
        "How to climb the Panta x NectarFi leaderboard and claim your share of the 500 USDG prize pool.",
        font=fnt(FONT_REG, 25),
        fill=(180, 200, 226),
    )

    # Left: Interactive Dashboard Preview Box
    draw.rounded_rectangle([60, 245, 1140, 900], radius=18, fill=(12, 18, 32), outline=(0, 194, 255), width=3)
    draw.rounded_rectangle([60, 245, 1140, 300], radius=18, fill=(22, 34, 60))
    draw.ellipse([85, 263, 105, 283], fill=(239, 68, 68))
    draw.ellipse([118, 263, 138, 283], fill=(245, 158, 11))
    draw.ellipse([151, 263, 171, 283], fill=(34, 197, 94))
    draw.text((200, 260), "panta_nectarfi_dashboard.html — Live EV & Kelly Simulator", font=fnt(FONT_MONO_BOLD, 19), fill=(210, 230, 255))

    sim_items = [
        ("Selected Strategy Preset", "Balanced Yield + Alpha (75% NectarFi / 25% Panta)", (0, 215, 255)),
        ("Total Competition Bankroll", "$2,500.00 USDG  (NectarFi: $1,875 | Panta: $625)", (255, 255, 255)),
        ("Panta Contract Setup", "1,488.1 YES Shares @ $0.42 (True Prob p = 60%)", (245, 158, 11)),
        ("30-Day NectarFi Yield Cushion", "+$23.12 USDG Guaranteed Vault Yield", (20, 241, 149)),
        ("Combined Portfolio EV", "+$291.19 USDG (+11.65% 30-Day Expected Return)", (20, 241, 149)),
        ("Upside If YES Resolves ($1.00)", "+$886.21 USDG Net Profit (+35.4% Total ROI)", (20, 241, 149)),
        ("Optimal Half-Kelly Allocation", "15.5% Safe Sizing (Full Kelly = 31.0%)", (216, 180, 254)),
    ]
    sy = 325
    for k, v, col in sim_items:
        draw.rounded_rectangle([90, sy, 1110, sy + 68], radius=10, fill=(18, 28, 48), outline=(40, 62, 98), width=1)
        draw.text((115, sy + 20), k, font=fnt(FONT_BOLD, 19), fill=(180, 200, 230))
        draw.text((510, sy + 20), v, font=fnt(FONT_MONO_BOLD, 19), fill=col)
        sy += 78

    # Right: Competition Checklist
    draw.rounded_rectangle([1180, 245, 1860, 900], radius=18, fill=(16, 26, 42), outline=(245, 158, 11), width=3)
    draw.rounded_rectangle([1210, 275, 1830, 332], radius=10, fill=(48, 34, 14))
    draw.text((1232, 290), "TRADING COMPETITION CHECKLIST", font=fnt(FONT_BOLD, 22), fill=(255, 200, 75))

    check_items = [
        ("1. Fund USDG on NectarFi", "Park 70%–90% of your USDG in @Nectar_finance to lock in baseline APY."),
        ("2. Hunt Mispriced Panta Odds", "Look for @PantaHQ markets where your research probability beats price by >=12%."),
        ("3. Size with Half-Kelly", "Use our HTML5 calculator (`panta_nectarfi_dashboard.html`) to avoid over-betting."),
        ("4. Share Proof & Tag", "Post your thesis, PnL cards & video with #PantaMarkets tagging @PantaHQ @Nectar_finance @SuperteamNG."),
    ]
    cy = 360
    for c_head, c_desc in check_items:
        draw.rounded_rectangle([1210, cy, 1830, cy + 118], radius=12, fill=(22, 34, 56), outline=(65, 85, 120), width=1)
        draw.text((1232, cy + 16), c_head, font=fnt(FONT_BOLD, 21), fill=(20, 241, 149))
        # wrap c_desc
        words = c_desc.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) <= 38:
                cur = (cur + " " + w).strip()
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        ly = cy + 50
        for ln in lines:
            draw.text((1232, ly), ln, font=fnt(FONT_REG, 18), fill=(215, 230, 250))
            ly += 26
        cy += 132

    draw.rounded_rectangle([60, 920, 1860, 990], radius=14, fill=(18, 44, 40), outline=(20, 241, 149), width=2)
    draw.text(
        (95, 942),
        "JOIN THE COMPETITION NOW: Trade on @PantaHQ + Earn on @Nectar_finance + Tag @SuperteamNG #PantaMarkets",
        font=fnt(FONT_BOLD, 23),
        fill=(20, 241, 149),
    )

    out = OUT_DIR / "card_4_strategy.png"
    img.save(out)
    return out


def build_video(slides_with_durations: List[Tuple[Path, int]], output_mp4: Path) -> None:
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    concat_file = OUT_DIR / "ffmpeg_concat.txt"
    lines = []
    for slide_path, duration in slides_with_durations:
        lines.append(f"file '{slide_path.resolve()}'")
        lines.append(f"duration {duration}")
    lines.append(f"file '{slides_with_durations[-1][0].resolve()}'")
    concat_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    total_seconds = sum(d for _, d in slides_with_durations)
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=261.63:sample_rate=44100:duration={total_seconds}",
        "-filter_complex",
        f"[1:a]volume=0.03,afade=t=in:st=0:d=1.5,afade=t=out:st={total_seconds - 1.5}:d=1.5[aout]",
        "-map",
        "0:v",
        "-map",
        "[aout]",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-shortest",
        str(output_mp4),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    c1 = make_card_1()
    c2 = make_card_2()
    c3 = make_card_3()
    c4 = make_card_4()

    slides = [
        (c1, 11),
        (c2, 12),
        (c3, 11),
        (c4, 11),
    ]
    build_video(slides, VIDEO_PATH)
    print(f"Generated 4 infographic cards in {OUT_DIR}")
    print(f"Generated 45s 1080p MP4 video: {VIDEO_PATH} ({VIDEO_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
