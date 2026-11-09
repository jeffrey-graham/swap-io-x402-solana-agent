#!/usr/bin/env python3
"""
Generates both multi-winner video + slide bundles in `kriptok-and-mozaikpay/`:
1. KriptoK 200 USDC Creator Challenge (10 Winners):
   - 4 1920x1080 PNG slides (`output/kriptok_slide_1.png` .. `output/kriptok_slide_4.png`)
   - 60-second 1080p MP4 video (`output/kriptok_creator_walkthrough.mp4`)
2. MozaikPay LatAm Cross-Border Video Challenge (6 Winners):
   - 4 1080x1920 vertical Spanish PNG slides (`output/mozaikpay_slide_1_es.png` .. `output/mozaikpay_slide_4_es.png`)
   - 45-second vertical 1080x1920 Spanish TikTok/Reel MP4 (`output/mozaikpay_remittance_reel_es.mp4`)
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT_DIR / "output"

KRIPTOK_VIDEO = OUT_DIR / "kriptok_creator_walkthrough.mp4"
MOZAIKPAY_VIDEO = OUT_DIR / "mozaikpay_remittance_reel_es.mp4"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def fnt(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


# ==============================================================================
# PART 1: KRIPTOK 1920x1080 LANDSCAPE SLIDES & 60s VIDEO
# ==============================================================================
def draw_kriptok_base(img: Image.Image, step: int, tag: str) -> ImageDraw.ImageDraw:
    w, h = 1920, 1080
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, h], fill=(11, 10, 24))
    for x in range(0, w, 60):
        draw.line([(x, 0), (x, h)], fill=(22, 18, 42), width=1)
    for y in range(0, h, 60):
        draw.line([(0, y), (w, y)], fill=(22, 18, 42), width=1)

    # Top neon gradient bar (Pink -> Violet -> Cyan)
    draw.rectangle([0, 0, 640, 8], fill=(244, 63, 94))
    draw.rectangle([640, 0, 1280, 8], fill=(168, 85, 247))
    draw.rectangle([1280, 0, w, 8], fill=(20, 241, 149))

    draw.rounded_rectangle([60, 36, 480, 86], radius=12, fill=(36, 16, 42), outline=(244, 63, 94), width=2)
    draw.text((84, 48), "KRIPTOK  •  ALL-IN-ONE SUPERAPP", font=fnt(FONT_BOLD, 21), fill=(255, 115, 145))

    draw.rounded_rectangle([505, 36, 1040, 86], radius=12, fill=(24, 18, 48), outline=(168, 85, 247), width=2)
    draw.text((530, 49), tag, font=fnt(FONT_MONO_BOLD, 19), fill=(220, 185, 255))

    draw.rounded_rectangle([1430, 36, 1860, 86], radius=12, fill=(14, 34, 34), outline=(20, 241, 149), width=2)
    draw.text((1455, 49), f"SLIDE 0{step} / 04  •  CREATOR CHALLENGE", font=fnt(FONT_MONO_BOLD, 18), fill=(20, 241, 149))

    draw.rectangle([0, 1015, w, h], fill=(8, 7, 18))
    draw.line([(0, 1015), (w, 1015)], fill=(48, 36, 82), width=2)
    draw.text(
        (60, 1033),
        "KriptoK Deep-Dive: Crypto Perps  •  Pre-IPO Markets  •  Tokenized Stocks  •  On-Chain Gacha Rewards",
        font=fnt(FONT_MONO, 19),
        fill=(165, 155, 200),
    )
    draw.text((1510, 1033), "Built on Solana  |  KriptoK Creator Challenge", font=fnt(FONT_BOLD, 19), fill=(244, 63, 94))
    return draw


def make_kriptok_slides() -> List[Tuple[Path, int]]:
    w, h = 1920, 1080

    # Slide 1: The Fragmentation Problem vs KriptoK SuperApp
    img1 = Image.new("RGB", (w, h))
    d1 = draw_kriptok_base(img1, 1, "4 ASSET CLASSES • 1 UNIFIED SOLANA WALLET")
    d1.text((60, 118), "Why KriptoK Is the Ultimate Consumer Trading SuperApp", font=fnt(FONT_BOLD, 46), fill=(255, 255, 255))
    d1.text((60, 180), "Trade Perpetuals, Pre-IPO Unicorns, Tokenized Equities, and Gacha Rewards from a single balance.", font=fnt(FONT_REG, 25), fill=(195, 190, 225))

    quads = [
        (60, 250, 930, 565, "1. HIGH-SPEED CRYPTO PERPS", (244, 63, 94), [
            "• Deep liquidity on SOL, BTC, ETH & trending pairs",
            "• Sub-second execution with customizable leverage",
            "• Zero CEX custody risk — self-custodial margin",
        ]),
        (990, 250, 1860, 565, "2. PRE-IPO UNICORN MARKETS", (168, 85, 247), [
            "• Access private tech giants before Wall Street IPOs",
            "• Long/short synthetic exposure to AI & space leaders",
            "• Democratizes venture-stage upside without $250k minimums",
        ]),
        (60, 595, 930, 910, "3. 24/7 TOKENIZED STOCKS (RWA)", (0, 194, 255), [
            "• Trade NVDA, TSLA, AAPL & SPY 24/7/365 on-chain",
            "• No brokerage wire delays or weekend market blackouts",
            "• Fractional sizing settled directly in stablecoins",
        ]),
        (990, 595, 1860, 910, "4. GAMIFIED GACHA REWARD ENGINE", (20, 241, 149), [
            "• Every trade & streak earns Gacha spins & loot boxes",
            "• Transparent on-chain odds with instant USDC/token drops",
            "• Turns passive volume into engaging consumer retention",
        ]),
    ]
    for x1, y1, x2, y2, title, col, lines in quads:
        d1.rounded_rectangle([x1, y1, x2, y2], radius=18, fill=(18, 16, 36), outline=col, width=3)
        d1.rounded_rectangle([x1 + 24, y1 + 22, x2 - 24, y1 + 74], radius=10, fill=(28, 24, 54))
        d1.text((x1 + 40, y1 + 35), title, font=fnt(FONT_BOLD, 22), fill=col)
        ly = y1 + 98
        for ln in lines:
            d1.text((x1 + 36, ly), ln, font=fnt(FONT_REG, 22), fill=(235, 235, 250))
            ly += 56

    d1.rounded_rectangle([60, 930, 1860, 992], radius=12, fill=(26, 20, 48), outline=(244, 63, 94), width=2)
    d1.text((95, 948), "ONE MARGIN ENGINE: Rotate profits from SOL Perps into Pre-IPO allocations or NVDA tokenized equities in 1 click.", font=fnt(FONT_BOLD, 22), fill=(255, 165, 185))
    p1 = OUT_DIR / "kriptok_slide_1.png"
    img1.save(p1)

    # Slide 2: Deep Dive — Perps + Pre-IPO Markets
    img2 = Image.new("RGB", (w, h))
    d2 = draw_kriptok_base(img2, 2, "PERPETUALS + PRE-IPO UNICORN ACCESS")
    d2.text((60, 118), "Institutional Perps Meet Permissionless Pre-IPO Markets", font=fnt(FONT_BOLD, 46), fill=(255, 255, 255))
    d2.text((60, 180), "How KriptoK bridges high-frequency crypto derivatives and pre-listing private market price discovery.", font=fnt(FONT_REG, 25), fill=(195, 190, 225))

    d2.rounded_rectangle([60, 248, 930, 895], radius=18, fill=(18, 16, 36), outline=(244, 63, 94), width=3)
    d2.text((95, 280), "CRYPTO PERPETUALS ENGINE", font=fnt(FONT_BOLD, 28), fill=(244, 63, 94))
    perp_rows = [
        ("Execution Latency", "< 400ms Solana Block Settlement"),
        ("Order Types", "Market, Limit, TP/SL, Trailing Stop"),
        ("Collateral Efficiency", "Unified USDC Margin Across Pairs"),
        ("Transparency", "100% Verifiable On-Chain Liquidation Logic"),
    ]
    py = 350
    for k, v in perp_rows:
        d2.rounded_rectangle([95, py, 895, py + 110], radius=12, fill=(26, 22, 48), outline=(85, 45, 75), width=1)
        d2.text((120, py + 18), k, font=fnt(FONT_MONO_BOLD, 19), fill=(255, 130, 155))
        d2.text((120, py + 56), v, font=fnt(FONT_BOLD, 23), fill=(255, 255, 255))
        py += 128

    d2.rounded_rectangle([990, 248, 1860, 895], radius=18, fill=(18, 16, 36), outline=(168, 85, 247), width=3)
    d2.text((1025, 280), "PRE-IPO UNICORN MARKETS", font=fnt(FONT_BOLD, 28), fill=(168, 85, 247))
    ipo_rows = [
        ("Legacy Accredited Gate", "$250k+ Minimums & 5-Year Lockups"),
        ("KriptoK Pre-IPO Access", "Start with $10 USDC — Instant Liquidity"),
        ("Directional Flexibility", "Go Long or Hedge Private Valuation Hype"),
        ("Price Discovery", "Real-Time 24/7 Valuation Oracle Feeds"),
    ]
    py = 350
    for k, v in ipo_rows:
        d2.rounded_rectangle([1025, py, 1825, py + 110], radius=12, fill=(26, 22, 48), outline=(85, 55, 125), width=1)
        d2.text((1050, py + 18), k, font=fnt(FONT_MONO_BOLD, 19), fill=(216, 180, 254))
        d2.text((1050, py + 56), v, font=fnt(FONT_BOLD, 23), fill=(255, 255, 255))
        py += 128

    d2.rounded_rectangle([60, 918, 1860, 990], radius=14, fill=(22, 32, 52), outline=(0, 194, 255), width=2)
    d2.text((95, 940), "CROSS-MARKET STRATEGY: Hedge high-beta AI token exposure against Pre-IPO valuations in a single interface.", font=fnt(FONT_BOLD, 23), fill=(0, 220, 255))
    p2 = OUT_DIR / "kriptok_slide_2.png"
    img2.save(p2)

    # Slide 3: Tokenized Stocks + Gacha Loop
    img3 = Image.new("RGB", (w, h))
    d3 = draw_kriptok_base(img3, 3, "TOKENIZED EQUITIES + GACHA FLYWHEEL")
    d3.text((60, 118), "24/7 Tokenized Stocks & The On-Chain Gacha Flywheel", font=fnt(FONT_BOLD, 46), fill=(255, 255, 255))
    d3.text((60, 180), "Why KriptoK's gamified Gacha reward loop turns active traders into long-term ecosystem stakeholders.", font=fnt(FONT_REG, 25), fill=(195, 190, 225))

    steps = [
        ("1. TRADE ANY MARKET", "Execute Perps, Pre-IPO, or 24/7 Tokenized Stocks.", (0, 194, 255)),
        ("2. EARN GACHA TICKETS", "Volume milestones & daily streaks unlock Gacha pulls.", (168, 85, 247)),
        ("3. SPIN ON-CHAIN GACHA", "Provably fair loot boxes drop USDC, fee rebates & boosts.", (244, 63, 94)),
        ("4. COMPOUND EDGE", "Re-deploy rewards into zero-fee Perp & Stock positions!", (20, 241, 149)),
    ]
    sx = 60
    for st, desc, col in steps:
        d3.rounded_rectangle([sx, 250, sx + 425, 560], radius=18, fill=(18, 16, 36), outline=col, width=3)
        d3.text((sx + 28, 285), st, font=fnt(FONT_BOLD, 25), fill=col)
        words = desc.split()
        lines, cur = [], ""
        for word in words:
            if len(cur + " " + word) <= 26:
                cur = (cur + " " + word).strip()
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        ly = 365
        for ln in lines:
            d3.text((sx + 28, ly), ln, font=fnt(FONT_REG, 24), fill=(235, 240, 255))
            ly += 40
        sx += 450

    d3.rounded_rectangle([60, 595, 1860, 980], radius=18, fill=(16, 22, 38), outline=(20, 241, 149), width=2)
    d3.text((95, 625), "WHY TOKENIZED STOCKS ON KRIPTOK BEAT TRADITIONAL BROKERS:", font=fnt(FONT_BOLD, 25), fill=(20, 241, 149))
    stock_cmp = [
        ("Weekend Earnings & Macro Catalysts", "TradFi closes Friday 4PM EST. KriptoK lets you trade tokenized equities 24/7."),
        ("Borderless Global Access", "No geographic brokerage restrictions or 5-day international SWIFT wire holds."),
        ("Unified Stablecoin Settlement", "Hold, trade, and harvest Gacha rewards in native USD stablecoins on Solana."),
    ]
    cy = 682
    for h_txt, b_txt in stock_cmp:
        d3.rounded_rectangle([95, cy, 1825, cy + 80], radius=12, fill=(24, 32, 56), outline=(50, 75, 115), width=1)
        d3.text((120, cy + 25), h_txt, font=fnt(FONT_BOLD, 21), fill=(0, 215, 255))
        d3.text((640, cy + 25), b_txt, font=fnt(FONT_REG, 21), fill=(235, 242, 255))
        cy += 94

    p3 = OUT_DIR / "kriptok_slide_3.png"
    img3.save(p3)

    # Slide 4: Comparison & Call To Action
    img4 = Image.new("RGB", (w, h))
    d4 = draw_kriptok_base(img4, 4, "COMPETITIVE MATRIX & QUICKSTART")
    d4.text((60, 118), "KriptoK vs. Legacy CEXs & TradFi Brokerages", font=fnt(FONT_BOLD, 46), fill=(255, 255, 255))
    d4.text((60, 180), "One self-custodial experience combining the best of decentralized perps, RWAs, and consumer gaming.", font=fnt(FONT_REG, 25), fill=(195, 190, 225))

    d4.rounded_rectangle([60, 248, 1860, 880], radius=18, fill=(16, 15, 34), outline=(168, 85, 247), width=3)
    cols = [95, 620, 1040, 1450]
    headers = ["FEATURE / MARKET", "TRADFI BROKERAGE", "STANDARD CRYPTO DEX", "KRIPTOK SUPERAPP"]
    d4.rounded_rectangle([80, 270, 1840, 335], radius=10, fill=(32, 24, 62))
    for cx, h_str in zip(cols, headers):
        d4.text((cx, 290), h_str, font=fnt(FONT_BOLD, 21), fill=(220, 190, 255))

    matrix = [
        ("Crypto Perpetuals", "Not Supported", "Yes (Crypto Only)", "Yes (Deep Liquidity + Low Fees)"),
        ("Pre-IPO Unicorn Markets", "Accredited $250k+ Only", "Not Supported", "Yes (Permissionless Fractional)"),
        ("24/7 Tokenized Stocks", "5 Days/Wk (Market Hours)", "Rare / Fragmented", "Yes (24/7/365 Unified Margin)"),
        ("On-Chain Gacha Rewards", "Zero Rewards", "Static Points Only", "Instant Gacha Spins & Loot Drops"),
        ("Custody & Settlement", "Centralized T+1 Clearing", "On-Chain Wallet", "Instant Solana Self-Custody"),
    ]
    ry = 365
    for feat, c1, c2, c3 in matrix:
        d4.line([(90, ry - 12), (1830, ry - 12)], fill=(38, 32, 68), width=1)
        d4.text((cols[0], ry), feat, font=fnt(FONT_BOLD, 22), fill=(255, 255, 255))
        d4.text((cols[1], ry), c1, font=fnt(FONT_REG, 21), fill=(255, 135, 145))
        d4.text((cols[2], ry), c2, font=fnt(FONT_REG, 21), fill=(245, 195, 110))
        d4.text((cols[3], ry), c3, font=fnt(FONT_BOLD, 21), fill=(20, 241, 149))
        ry += 98

    d4.rounded_rectangle([60, 910, 1860, 990], radius=14, fill=(36, 16, 42), outline=(244, 63, 94), width=2)
    d4.text((95, 936), "START TRADING ON KRIPTOK TODAY: Perps • Pre-IPO • Tokenized Stocks • Gacha Rewards!", font=fnt(FONT_BOLD, 25), fill=(255, 130, 160))
    p4 = OUT_DIR / "kriptok_slide_4.png"
    img4.save(p4)

    return [(p1, 15), (p2, 15), (p3, 15), (p4, 15)]


# ==============================================================================
# PART 2: MOZAIKPAY 1080x1920 VERTICAL SPANISH REEL SLIDES & 45s VIDEO
# ==============================================================================
def draw_mozaik_base(img: Image.Image, step: int, tag_es: str) -> ImageDraw.ImageDraw:
    w, h = 1080, 1920
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, h], fill=(8, 16, 28))
    for x in range(0, w, 60):
        draw.line([(x, 0), (x, h)], fill=(14, 28, 48), width=1)
    for y in range(0, h, 60):
        draw.line([(0, y), (w, y)], fill=(14, 28, 48), width=1)

    # Top accent bar: Chile/Colombia/Solana vibrant palette
    draw.rectangle([0, 0, 360, 12], fill=(20, 241, 149))
    draw.rectangle([360, 0, 720, 12], fill=(245, 158, 11))
    draw.rectangle([720, 0, w, 12], fill=(0, 194, 255))

    # Top badges
    draw.rounded_rectangle([55, 55, 650, 120], radius=16, fill=(14, 42, 48), outline=(20, 241, 149), width=3)
    draw.text((82, 73), "MOZAIKPAY  •  REMESAS LATAM", font=fnt(FONT_BOLD, 26), fill=(20, 241, 149))

    draw.rounded_rectangle([675, 55, 1025, 120], radius=16, fill=(22, 34, 58), outline=(0, 194, 255), width=2)
    draw.text((705, 75), f"PASO 0{step} / 04", font=fnt(FONT_MONO_BOLD, 24), fill=(0, 215, 255))

    draw.rounded_rectangle([55, 140, 1025, 200], radius=14, fill=(28, 26, 16), outline=(245, 158, 11), width=2)
    draw.text((82, 156), tag_es, font=fnt(FONT_MONO_BOLD, 22), fill=(255, 210, 90))

    # Bottom footer
    draw.rectangle([0, 1800, w, h], fill=(6, 11, 20))
    draw.line([(0, 1800), (w, 1800)], fill=(30, 58, 92), width=2)
    draw.text((55, 1828), "Chile 🇨🇱  ->  Colombia 🇨🇴  |  USDC Instantáneo en Solana", font=fnt(FONT_BOLD, 24), fill=(20, 241, 149))
    draw.text((55, 1868), "Sin comisiones ocultas  •  Tipo de cambio justo  •  24/7", font=fnt(FONT_REG, 21), fill=(165, 195, 225))
    return draw


def make_mozaikpay_slides() -> List[Tuple[Path, int]]:
    w, h = 1080, 1920

    # Slide 1: El Problema de Enviar Dinero de Chile a Colombia
    img1 = Image.new("RGB", (w, h))
    d1 = draw_mozaik_base(img1, 1, "CORREDOR CHILE -> COLOMBIA SIN FRICCIÓN")
    d1.text((55, 235), "¿Cansado de perder", font=fnt(FONT_BOLD, 56), fill=(255, 255, 255))
    d1.text((55, 305), "hasta 8% enviando", font=fnt(FONT_BOLD, 56), fill=(255, 125, 125))
    d1.text((55, 375), "dinero de Chile a", font=fnt(FONT_BOLD, 56), fill=(255, 255, 255))
    d1.text((55, 445), "Colombia?", font=fnt(FONT_BOLD, 58), fill=(20, 241, 149))

    # Problem Box
    d1.rounded_rectangle([55, 545, 1025, 1110], radius=24, fill=(32, 16, 26), outline=(239, 68, 68), width=3)
    d1.text((90, 580), "REMESADORAS Y BANCOS TRADICIONALES:", font=fnt(FONT_BOLD, 27), fill=(255, 130, 130))
    pains = [
        ("Comisiones del 5% al 8.5%", "Pierdes miles de pesos en cada envío familiar."),
        ("3 a 5 Días Hábiles de Espera", "Los fines de semana y festivos tu dinero queda congelado."),
        ("Spread Cambiario Oculto (CLP/COP)", "Te castigan el tipo de cambio frente al dólar real."),
        ("Filas y Trámites Presenciales", "Horarios limitados y papeleo innecesario."),
    ]
    py = 645
    for title, sub in pains:
        d1.rounded_rectangle([85, py, 995, py + 98], radius=14, fill=(46, 22, 34), outline=(105, 42, 58), width=1)
        d1.text((110, py + 15), f"[X] {title}", font=fnt(FONT_BOLD, 24), fill=(255, 155, 155))
        d1.text((110, py + 54), sub, font=fnt(FONT_REG, 20), fill=(225, 195, 205))
        py += 112

    # Solution Preview Box
    d1.rounded_rectangle([55, 1150, 1025, 1745], radius=24, fill=(12, 36, 44), outline=(20, 241, 149), width=3)
    d1.text((90, 1190), "LA SOLUCIÓN: MOZAIKPAY EN SOLANA", font=fnt(FONT_BOLD, 28), fill=(20, 241, 149))
    wins = [
        "• Carga Pesos Chilenos (CLP) en segundos",
        "• Convierte a USDC digital 1:1 con el dólar",
        "• Envía a Colombia al instante (< 5 segundos)",
        "• Retiro directo a cuenta bancaria o billetera en COP",
        "• Ahorra más del 85% en costos de envío cada mes",
    ]
    wy = 1265
    for w_line in wins:
        d1.text((95, wy), w_line, font=fnt(FONT_BOLD, 26), fill=(235, 255, 245))
        wy += 88

    p1 = OUT_DIR / "mozaikpay_slide_1_es.png"
    img1.save(p1)

    # Slide 2: Paso a Paso — Cómo Uso MozaikPay en 60 Segundos
    img2 = Image.new("RGB", (w, h))
    d2 = draw_mozaik_base(img2, 2, "TUTORIAL PASO A PASO EN TIEMPO REAL")
    d2.text((55, 235), "Cómo uso MozaikPay", font=fnt(FONT_BOLD, 54), fill=(255, 255, 255))
    d2.text((55, 305), "en 3 Simples Pasos", font=fnt(FONT_BOLD, 54), fill=(0, 215, 255))

    steps_es = [
        (
            "PASO 1: RECARGA EN CHILE (CLP -> USDC)",
            (0, 194, 255),
            [
                "Abro MozaikPay y deposito $200.000 CLP",
                "desde mi banco local en Chile.",
                "Mi saldo se acredita automáticamente en",
                "USDC sobre la red Solana sin fricción.",
            ],
        ),
        (
            "PASO 2: ENVÍO INSTANTÁNEO SIN FRONTERAS",
            (245, 158, 11),
            [
                "Selecciono el destinatario en Bogotá o",
                "Medellín y envío los USDC en un toque.",
                "Confirmación en Solana: menos de 2 segundos",
                "y costo de red menor a $0.001 USD.",
            ],
        ),
        (
            "PASO 3: RECIBE EN COLOMBIA (USDC -> COP)",
            (20, 241, 149),
            [
                "Mi familia en Colombia recibe los fondos",
                "al instante: puede mantenerlos en dólares",
                "digitales (USDC) para protegerse de la",
                "inflación o retirarlos directo en Pesos (COP).",
            ],
        ),
    ]
    sy = 410
    for st_title, col, lines in steps_es:
        d2.rounded_rectangle([55, sy, 1025, sy + 415], radius=22, fill=(14, 26, 46), outline=col, width=3)
        d2.rounded_rectangle([85, sy + 26, 995, sy + 92], radius=12, fill=(22, 38, 68))
        d2.text((108, sy + 44), st_title, font=fnt(FONT_BOLD, 25), fill=col)
        ly = sy + 125
        for ln in lines:
            d2.text((100, ly), ln, font=fnt(FONT_REG, 27), fill=(235, 242, 255))
            ly += 60
        sy += 450

    p2 = OUT_DIR / "mozaikpay_slide_2_es.png"
    img2.save(p2)

    # Slide 3: Comparativa Real — Envío de $200 USD (Chile -> Colombia)
    img3 = Image.new("RGB", (w, h))
    d3 = draw_mozaik_base(img3, 3, "COMPARATIVA REAL: ENVÍO DE $200 USD")
    d3.text((55, 235), "Números Reales:", font=fnt(FONT_BOLD, 54), fill=(255, 255, 255))
    d3.text((55, 305), "Enviando $200 USD", font=fnt(FONT_BOLD, 54), fill=(245, 158, 11))

    # Card A: Remesadora Tradicional
    d3.rounded_rectangle([55, 410, 1025, 1015], radius=22, fill=(32, 16, 26), outline=(239, 68, 68), width=3)
    d3.text((90, 445), "VÍA TRADICIONAL (BANCO / GIRO)", font=fnt(FONT_BOLD, 28), fill=(255, 130, 130))
    trad_rows = [
        ("Monto Enviado", "$200.00 USD equivalentes en CLP"),
        ("Comisión Fija + Spread", "-$14.80 USD (-7.4% perdido)"),
        ("Tiempo de Llegada", "3 a 4 días hábiles"),
        ("Recibido en Colombia", "$185.20 USD en COP"),
    ]
    ty = 520
    for k, v in trad_rows:
        d3.rounded_rectangle([85, ty, 995, ty + 102], radius=12, fill=(46, 22, 34))
        d3.text((110, ty + 16), k, font=fnt(FONT_MONO_BOLD, 20), fill=(255, 165, 165))
        d3.text((110, ty + 52), v, font=fnt(FONT_BOLD, 26), fill=(255, 255, 255))
        ty += 116

    # Card B: MozaikPay
    d3.rounded_rectangle([55, 1060, 1025, 1745], radius=22, fill=(12, 36, 44), outline=(20, 241, 149), width=3)
    d3.text((90, 1095), "CON MOZAIKPAY (USDC EN SOLANA)", font=fnt(FONT_BOLD, 28), fill=(20, 241, 149))
    moz_rows = [
        ("Monto Enviado", "200.00 USDC desde Chile"),
        ("Costo de Red Solana", "< $0.001 USD (Prácticamente $0)"),
        ("Tiempo de Llegada", "¡Menos de 5 segundos (24/7)!"),
        ("Ahorro Anual (12 envíos)", "+$170.00 USD extra para tu familia"),
    ]
    my = 1170
    for k, v in moz_rows:
        d3.rounded_rectangle([85, my, 995, my + 102], radius=12, fill=(18, 52, 58))
        d3.text((110, my + 16), k, font=fnt(FONT_MONO_BOLD, 20), fill=(110, 255, 195))
        d3.text((110, my + 52), v, font=fnt(FONT_BOLD, 26), fill=(255, 255, 255))
        my += 116

    p3 = OUT_DIR / "mozaikpay_slide_3_es.png"
    img3.save(p3)

    # Slide 4: Beneficios Clave & Llamado a la Acción
    img4 = Image.new("RGB", (w, h))
    d4 = draw_mozaik_base(img4, 4, "EL FUTURO DE LOS PAGOS EN LATINOAMÉRICA")
    d4.text((55, 235), "Por qué MozaikPay es", font=fnt(FONT_BOLD, 52), fill=(255, 255, 255))
    d4.text((55, 305), "mi App Favorita en", font=fnt(FONT_BOLD, 52), fill=(255, 255, 255))
    d4.text((55, 375), "Chile y Colombia", font=fnt(FONT_BOLD, 54), fill=(20, 241, 149))

    perks = [
        ("1. AHORRO EN DÓLARES DIGITALES (USDC)", "Protege tus ingresos de la devaluación del peso chileno o colombiano.", (20, 241, 149)),
        ("2. VELOCIDAD SOLANA SIN COMPLEJIDAD", "No necesitas ser experto en cripto: envías tan fácil como un chat.", (0, 194, 255)),
        ("3. IDEAL PARA FREELANCERS Y FAMILIas", "Cobra trabajos internacionales y envía remesas el mismo minuto.", (245, 158, 11)),
        ("4. TRANSPARENCIA TOTAL ANTES DE ENVIAR", "Ves exactamente cuántos pesos recibirá tu destinatario sin sorpresas.", (168, 85, 247)),
    ]
    py = 475
    for title, desc, col in perks:
        d4.rounded_rectangle([55, py, 1025, py + 240], radius=20, fill=(14, 26, 46), outline=col, width=3)
        d4.text((90, py + 32), title, font=fnt(FONT_BOLD, 26), fill=col)
        words = desc.split()
        lines, cur = [], ""
        for w_word in words:
            if len(cur + " " + w_word) <= 38:
                cur = (cur + " " + w_word).strip()
            else:
                lines.append(cur)
                cur = w_word
        if cur:
            lines.append(cur)
        ly = py + 95
        for ln in lines:
            d4.text((90, ly), ln, font=fnt(FONT_REG, 27), fill=(235, 242, 255))
            ly += 52
        py += 270

    d4.rounded_rectangle([55, 1575, 1025, 1745], radius=22, fill=(16, 56, 48), outline=(20, 241, 149), width=3)
    d4.text((90, 1612), "¡PRUEBA MOZAIKPAY HOY MISMO!", font=fnt(FONT_BOLD, 34), fill=(20, 241, 149))
    d4.text((90, 1672), "Conecta Chile 🇨🇱 y Colombia 🇨🇴 en segundos con Solana.", font=fnt(FONT_BOLD, 24), fill=(255, 255, 255))

    p4 = OUT_DIR / "mozaikpay_slide_4_es.png"
    img4.save(p4)

    return [(p1, 11), (p2, 12), (p3, 11), (p4, 11)]


def encode_mp4(slides: List[Tuple[Path, int]], output_mp4: Path, freq: float = 240.0) -> None:
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    concat_file = OUT_DIR / f"concat_{output_mp4.stem}.txt"
    lines = []
    for sp, dur in slides:
        lines.append(f"file '{sp.resolve()}'")
        lines.append(f"duration {dur}")
    lines.append(f"file '{slides[-1][0].resolve()}'")
    concat_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    total_sec = sum(d for _, d in slides)
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
        f"sine=frequency={freq}:sample_rate=44100:duration={total_sec}",
        "-filter_complex",
        f"[1:a]volume=0.03,afade=t=in:st=0:d=1.5,afade=t=out:st={total_sec - 1.5}:d=1.5[aout]",
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
    kriptok_slides = make_kriptok_slides()
    encode_mp4(kriptok_slides, KRIPTOK_VIDEO, freq=220.0)
    print(f"Generated KriptoK 60s 1080p MP4: {KRIPTOK_VIDEO} ({KRIPTOK_VIDEO.stat().st_size:,} bytes)")

    mozaik_slides = make_mozaikpay_slides()
    encode_mp4(mozaik_slides, MOZAIKPAY_VIDEO, freq=293.66)
    print(f"Generated MozaikPay 45s 1080x1920 ES Reel: {MOZAIKPAY_VIDEO} ({MOZAIKPAY_VIDEO.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
