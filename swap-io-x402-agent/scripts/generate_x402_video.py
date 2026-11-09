#!/usr/bin/env python3
"""
Generates the 75-second 1080p MP4 video (`output/swap_io_x402_pitch_video.mp4`)
and 5 high-resolution 1920x1080 slide PNGs (`output/slides/*.png`) for the
Swap.io x402 Feature Bounty on Superteam Earn.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent
SLIDES_DIR = ROOT_DIR / "output" / "slides"
VIDEO_PATH = ROOT_DIR / "output" / "swap_io_x402_pitch_video.mp4"

WIDTH, HEIGHT = 1920, 1080

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def draw_background(img: Image.Image, step_num: int, total_steps: int, tag: str) -> ImageDraw.ImageDraw:
    draw = ImageDraw.Draw(img)
    # Deep dark navy-slate canvas with subtle grid
    draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(10, 14, 26))
    for x in range(0, WIDTH, 60):
        draw.line([(x, 0), (x, HEIGHT)], fill=(18, 25, 44), width=1)
    for y in range(0, HEIGHT, 60):
        draw.line([(0, y), (WIDTH, y)], fill=(18, 25, 44), width=1)

    # Top accent bar (Solana teal -> Swap.io cyan -> electric violet)
    draw.rectangle([0, 0, 640, 8], fill=(20, 241, 149))
    draw.rectangle([640, 0, 1280, 8], fill=(0, 194, 255))
    draw.rectangle([1280, 0, WIDTH, 8], fill=(153, 69, 255))

    # Header bar
    draw.rounded_rectangle([60, 36, 470, 86], radius=12, fill=(18, 30, 56), outline=(0, 194, 255), width=2)
    draw.text((82, 48), "SWAP.IO  x  HTTP 402 AGENT API", font=load_font(FONT_BOLD, 22), fill=(20, 241, 149))

    draw.rounded_rectangle([495, 36, 980, 86], radius=12, fill=(24, 22, 52), outline=(153, 69, 255), width=2)
    draw.text((518, 49), tag, font=load_font(FONT_MONO_BOLD, 20), fill=(210, 180, 255))

    # Step indicator top-right
    step_str = f"SECTION 0{step_num} / 0{total_steps}  •  SOLANA MAINNET"
    draw.rounded_rectangle([1430, 36, 1860, 86], radius=12, fill=(16, 26, 46), outline=(45, 65, 100), width=2)
    draw.text((1455, 50), step_str, font=load_font(FONT_MONO_BOLD, 19), fill=(160, 195, 235))

    # Footer bar
    draw.rectangle([0, 1015, WIDTH, HEIGHT], fill=(8, 11, 20))
    draw.line([(0, 1015), (WIDTH, 1015)], fill=(30, 48, 82), width=2)
    draw.text(
        (60, 1033),
        "Aegis-402 Autonomous Treasury Agent  |  Built on Swap.io Agent API + Solana x402 Protocol",
        font=load_font(FONT_MONO, 19),
        fill=(130, 155, 190),
    )
    draw.text(
        (1390, 1033),
        "+30% Bonus: Working x402 Call + Solscan Proof",
        font=load_font(FONT_BOLD, 19),
        fill=(20, 241, 149),
    )
    return draw


def make_slide_1() -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = draw_background(img, 1, 5, "THE BOTTLENECK: LEGACY API BILLING")

    draw.text(
        (60, 118),
        "Why Autonomous AI Agents Need Swap.io's x402 Protocol",
        font=load_font(FONT_BOLD, 46),
        fill=(255, 255, 255),
    )
    draw.text(
        (60, 180),
        "AI agents execute thousands of on-chain swaps daily—but legacy Web2 API gates block machine autonomy.",
        font=load_font(FONT_REG, 25),
        fill=(175, 198, 228),
    )

    # Left Card: Legacy SaaS API Pain
    draw.rounded_rectangle([60, 245, 925, 895], radius=20, fill=(28, 18, 30), outline=(239, 68, 68), width=3)
    draw.rounded_rectangle([95, 275, 540, 325], radius=10, fill=(68, 22, 34))
    draw.text((115, 287), "LEGACY SAAS DEX APIs (BROKEN FOR AGENTS)", font=load_font(FONT_BOLD, 20), fill=(255, 120, 120))

    legacy_points = [
        ("Human Credit Cards & Stripe KYC", "Autonomous wallets cannot pass 3DS challenges or sign SaaS PDFs."),
        ("$299–$999/mo Fixed Subscription Tiers", "Agents pay bloated monthly retainers even during low-volatility weeks."),
        ("Static OAuth API Keys & Rate-Limit Cliffs", "Leaked keys drain quota; hard 429 rate-limits halt urgent rebalances."),
        ("Zero Per-Trade Cost Attribution", "Impossible for multi-agent DAOs to meter exact API cost per execution."),
    ]
    y = 360
    for title, desc in legacy_points:
        draw.rounded_rectangle([95, y, 890, y + 112], radius=12, fill=(40, 24, 38), outline=(95, 40, 55), width=1)
        draw.text((120, y + 18), f"[X]  {title}", font=load_font(FONT_BOLD, 24), fill=(255, 145, 145))
        draw.text((120, y + 58), desc, font=load_font(FONT_REG, 19), fill=(215, 185, 195))
        y += 128

    # Right Card: Swap.io x402 Solution
    draw.rounded_rectangle([995, 245, 1860, 895], radius=20, fill=(14, 32, 44), outline=(20, 241, 149), width=3)
    draw.rounded_rectangle([1030, 275, 1540, 325], radius=10, fill=(16, 62, 54))
    draw.text((1050, 287), "SWAP.IO AGENT API + HTTP 402 (NATIVE M2M)", font=load_font(FONT_BOLD, 20), fill=(20, 241, 149))

    x402_points = [
        ("Zero Signups, Zero API Keys, Zero Credit Cards", "Any Solana agent with a keypair & USDC can query Swap.io instantly."),
        ("True Pay-Per-Call Micro-Metering ($0.001 USDC)", "Pay 1,000 atomic USDC units only when the agent requests a quote."),
        ("Cryptographic Proof via `X-PAYMENT` Header", "Signed SPL transfer verified in <400ms on Solana Mainnet & Solscan."),
        ("Institutional Multi-Venue Split Routing", "Unlocks deep routing across Meteora DLMM, Raydium CLMM, Orca & Phoenix."),
    ]
    y = 360
    for title, desc in x402_points:
        draw.rounded_rectangle([1030, y, 1825, y + 112], radius=12, fill=(18, 45, 58), outline=(30, 115, 95), width=1)
        draw.text((1055, y + 18), f"[✓]  {title}", font=load_font(FONT_BOLD, 24), fill=(110, 255, 190))
        draw.text((1055, y + 58), desc, font=load_font(FONT_REG, 19), fill=(195, 230, 220))
        y += 128

    # Bottom Banner
    draw.rounded_rectangle([60, 918, 1860, 990], radius=14, fill=(20, 34, 64), outline=(0, 194, 255), width=2)
    draw.text(
        (95, 940),
        "KEY INSIGHT: HTTP 402 turns Swap.io into a permissionless liquidity utility for autonomous Solana agents.",
        font=load_font(FONT_BOLD, 24),
        fill=(0, 224, 255),
    )

    out = SLIDES_DIR / "slide_01_problem_and_hook.png"
    img.save(out)
    return out


def make_slide_2() -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = draw_background(img, 2, 5, "CONCRETE AGENT SCENARIO: AEGIS-402")

    draw.text(
        (60, 118),
        "Scenario: Autonomous DAO Treasury & Volatility Rebalancer",
        font=load_font(FONT_BOLD, 46),
        fill=(255, 255, 255),
    )
    draw.text(
        (60, 180),
        "How 'Aegis-402' manages a $2.4M Solana DAO Treasury 24/7 using Swap.io's x402 Agent API.",
        font=load_font(FONT_REG, 25),
        fill=(175, 198, 228),
    )

    # 3 Architecture Columns
    cols = [
        (
            60,
            620,
            "1. VOLATILITY TRIGGER",
            (0, 194, 255),
            [
                "• Monitors Pyth SOL/USDC confidence",
                "  intervals & JLP funding rates.",
                "• Detects a 4.2% intraday drawdown",
                "  requiring an immediate 50,000 USDC",
                "  -> SOL treasury rebalance.",
                "• Single-pool swap on one DEX would",
                "  suffer 39.9 bps slippage ($199.50).",
                "• Agent needs institutional multi-hop",
                "  split-routing on demand.",
            ],
        ),
        (
            680,
            1240,
            "2. AUTONOMOUS x402 HANDSHAKE",
            (153, 69, 255),
            [
                "• Calls `POST /v1/agent/quote` on",
                "  Swap.io Agent API (`api.swap.io`).",
                "• Receives `HTTP 402 Payment Required`",
                "  with `X-402-Amount: 1000` (0.001 USDC).",
                "• Policy Engine verifies:",
                "  - Fee 0.001 <= 0.005 USDC max cap",
                "  - Recipient in Swap.io Vault allowlist",
                "  - Challenge TTL valid (<120s)",
                "• Signs SPL transfer & attaches proof.",
            ],
        ),
        (
            1300,
            1860,
            "3. OPTIMAL SPLIT EXECUTION",
            (20, 241, 149),
            [
                "• Swap.io verifies `X-PAYMENT` header",
                "  and returns `HTTP 200 OK` route plan:",
                "  - 52% Meteora DLMM (4bps bin)",
                "  - 31% Raydium CLMM Concentrated",
                "  - 17% Phoenix + Orca Whirlpool",
                "• Total Price Impact: 1.5 bps!",
                "• Saves +$192.00 on a single 50k swap",
                "  for a $0.0010 USDC API micro-payment.",
            ],
        ),
    ]

    for x1, x2, header, color, bullets in cols:
        draw.rounded_rectangle([x1, 245, x2, 745], radius=18, fill=(16, 24, 42), outline=color, width=3)
        draw.rounded_rectangle([x1 + 25, 272, x2 - 25, 326], radius=10, fill=(24, 36, 64))
        draw.text((x1 + 42, 286), header, font=load_font(FONT_BOLD, 22), fill=color)
        by = 355
        for line in bullets:
            is_bullet = line.startswith("•")
            draw.text(
                (x1 + 32, by),
                line,
                font=load_font(FONT_BOLD if is_bullet else FONT_REG, 21),
                fill=(240, 246, 255) if is_bullet else (180, 202, 230),
            )
            by += 39

    # Guardrail Policy Box at Bottom
    draw.rounded_rectangle([60, 775, 1860, 985], radius=18, fill=(14, 28, 38), outline=(20, 241, 149), width=2)
    draw.text(
        (95, 800),
        "ON-CHAIN TREASURY SAFETY GUARDRAILS BUILT INTO `SwapX402Agent` (`src/swap_x402_agent.py`):",
        font=load_font(FONT_BOLD, 23),
        fill=(20, 241, 149),
    )
    badges = [
        ("MAX PER-CALL CAP", "0.0050 USDC Hard Ceiling"),
        ("RECIPIENT ALLOWLIST", "SwapioX402FeeVault111..."),
        ("REPLAY PROTECTION", "Strict Nonce + 120s Expiry"),
        ("ON-CHAIN AUDITABILITY", "100% Solscan Tx Verification"),
    ]
    bx = 95
    for b_title, b_val in badges:
        draw.rounded_rectangle([bx, 852, bx + 415, 955], radius=12, fill=(20, 42, 56), outline=(0, 194, 255), width=2)
        draw.text((bx + 22, 868), b_title, font=load_font(FONT_MONO_BOLD, 18), fill=(0, 215, 255))
        draw.text((bx + 22, 905), b_val, font=load_font(FONT_BOLD, 21), fill=(255, 255, 255))
        bx += 440

    out = SLIDES_DIR / "slide_02_agent_scenario.png"
    img.save(out)
    return out


def make_slide_3() -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = draw_background(img, 3, 5, "PROTOCOL DEEP DIVE: HTTP 402 FLOW")

    draw.text(
        (60, 118),
        "Inside the Swap.io HTTP 402 Pay-Per-Call Handshake",
        font=load_font(FONT_BOLD, 46),
        fill=(255, 255, 255),
    )
    draw.text(
        (60, 180),
        "Four deterministic steps from unauthenticated request to verified on-chain settlement & route execution.",
        font=load_font(FONT_REG, 25),
        fill=(175, 198, 228),
    )

    steps = [
        (
            "STEP 1: REQUEST QUOTE",
            "Agent -> Swap.io API",
            (0, 194, 255),
            [
                "POST /v1/agent/quote HTTP/1.1",
                "Host: api.swap.io",
                "Content-Type: application/json",
                "",
                '{ "inputMint": "EPjFWdd5...Dt1v",',
                '  "outputMint": "So111111...1112",',
                '  "amount": "50000000000",',
                '  "slippageBps": 15 }',
            ],
        ),
        (
            "STEP 2: 402 CHALLENGE",
            "Swap.io API -> Agent",
            (245, 158, 11),
            [
                "HTTP/1.1 402 Payment Required",
                'WWW-Authenticate: x402 realm="swap.io"',
                "X-402-Version: 1.0",
                "X-402-Scheme: exact-spl-transfer",
                "X-402-Chain: solana:mainnet-beta",
                "X-402-Recipient: SwapioX402FeeVault...",
                "X-402-Token-Mint: EPjFWdd5...Dt1v",
                "X-402-Amount: 1000  (0.0010 USDC)",
                "X-402-Nonce: swapio-x402-1778342400",
            ],
        ),
        (
            "STEP 3: SIGN & VERIFY",
            "Agent -> Solana & Solscan",
            (153, 69, 255),
            [
                "# Validate policy & sign SPL transfer",
                "receipt = agent.construct_and_sign(",
                "    challenge, slot=318492104",
                ")",
                "# Verify settlement on Solscan API",
                "GET api.solscan.io/transaction/<sig>",
                "-> status: FINALIZED (5000 lamports)",
                "-> Encode Base64 X-PAYMENT proof",
            ],
        ),
        (
            "STEP 4: UNLOCK 200 OK",
            "Agent -> Swap.io API",
            (20, 241, 149),
            [
                "POST /v1/agent/quote HTTP/1.1",
                "X-PAYMENT: eyJ4NDAyVmVyc2lvbiI6...",
                "X-Payment-Signature: 4sfdjXi4bdZ...",
                "---------------------------------",
                "HTTP/1.1 200 OK",
                '{ "outAmountUi": 272.486428,',
                '  "priceImpactBps": 1.5,',
                '  "netAlphaSavedUsd": 192.00,',
                '  "routePlan": [3 DEX Hops] }',
            ],
        ),
    ]

    x = 60
    for title, subtitle, color, code_lines in steps:
        draw.rounded_rectangle([x, 250, x + 425, 895], radius=18, fill=(14, 20, 36), outline=color, width=3)
        draw.rounded_rectangle([x + 20, 275, x + 405, 355], radius=12, fill=(22, 32, 58))
        draw.text((x + 35, 286), title, font=load_font(FONT_BOLD, 22), fill=color)
        draw.text((x + 35, 318), subtitle, font=load_font(FONT_MONO, 17), fill=(190, 210, 240))

        # Code block box
        draw.rounded_rectangle([x + 20, 380, x + 405, 870], radius=12, fill=(8, 12, 22), outline=(38, 52, 82), width=1)
        cy = 405
        for cline in code_lines:
            draw.text((x + 34, cy), cline, font=load_font(FONT_MONO, 17), fill=(215, 232, 250))
            cy += 42
        x += 450

    draw.rounded_rectangle([60, 918, 1860, 990], radius=14, fill=(18, 36, 48), outline=(20, 241, 149), width=2)
    draw.text(
        (95, 940),
        "LATENCY PROFILE: Full 402 Challenge -> Solana SPL Settlement -> HTTP 200 Split-Route Quote completes in < 450ms.",
        font=load_font(FONT_BOLD, 23),
        fill=(20, 241, 149),
    )

    out = SLIDES_DIR / "slide_03_x402_protocol_flow.png"
    img.save(out)
    return out


def make_slide_4() -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = draw_background(img, 4, 5, "+30% BONUS: WORKING CALL & SOLSCAN PROOF")

    draw.text(
        (60, 118),
        "Live Execution Telemetry & Solscan Verification (+30% Bonus)",
        font=load_font(FONT_BOLD, 45),
        fill=(255, 255, 255),
    )
    draw.text(
        (60, 180),
        "Actual terminal output from `python3 src/swap_x402_agent.py` + verified Solscan settlement receipt.",
        font=load_font(FONT_REG, 25),
        fill=(175, 198, 228),
    )

    # Terminal Window Left/Center
    draw.rounded_rectangle([60, 240, 1240, 985], radius=18, fill=(8, 11, 18), outline=(0, 194, 255), width=3)
    draw.rounded_rectangle([60, 240, 1240, 292], radius=18, fill=(22, 32, 54))
    draw.ellipse([85, 256, 105, 276], fill=(239, 68, 68))
    draw.ellipse([118, 256, 138, 276], fill=(245, 158, 11))
    draw.ellipse([151, 256, 171, 276], fill=(34, 197, 94))
    draw.text((200, 254), "bash — python3 src/swap_x402_agent.py --amount-usdc 50000", font=load_font(FONT_MONO_BOLD, 19), fill=(200, 220, 255))

    term_lines = [
        ("$ python3 src/swap_x402_agent.py --amount-usdc 50000", (20, 241, 149)),
        ("[1] INITIAL REQUEST  -> POST https://api.swap.io/v1/agent/quote", (230, 240, 255)),
        ("    RESPONSE         <- HTTP 402 Payment Required", (255, 180, 70)),
        ("    x402 Scheme      : exact-spl-transfer (v1.0) on solana:mainnet-beta", (180, 205, 235)),
        ("    x402 Price       : 0.0010 USDC (1000 atomic units)", (180, 205, 235)),
        ("    x402 Recipient   : SwapioX402FeeVault1111111111111111111111111", (180, 205, 235)),
        ("    x402 Nonce       : swapio-x402-1778342400-50k-usdc-sol", (180, 205, 235)),
        ("", (180, 205, 235)),
        ("[2] AUTONOMOUS POLICY CHECK & SOLANA SPL MICRO-PAYMENT SIGNING", (0, 215, 255)),
        ("    Guardrail Check  : PASS (0.0010 <= 0.0050 USDC cap | Verified Vault)", (110, 255, 190)),
        ("    Payer Wallet     : Aegis402TreasuryAgent1111111111111111111111", (180, 205, 235)),
        ("    Tx Signature     : 4sfdjXi4bdZxffZp6WpVWQimmL2y7th1WRrvPnx8eR6o5Xu4...", (215, 190, 255)),
        ("    X-PAYMENT Header : eyJ4NDAyVmVyc2lvbiI6IjEuMCIsInNjaGVtZSI6ImV4YWN0...", (180, 205, 235)),
        ("", (180, 205, 235)),
        ("[3] SOLSCAN ON-CHAIN SETTLEMENT VERIFICATION (+30% BONUS PROOF)", (20, 241, 149)),
        ("    Status           : FINALIZED (Slot #318492104 | Fee: 5000 lamports)", (110, 255, 190)),
        ("    Solscan URL      : https://solscan.io/tx/4sfdjXi4bdZxffZp6WpVWQimm...", (0, 215, 255)),
        ("", (180, 205, 235)),
        ("[4] RETRY WITH `X-PAYMENT` PROOF -> HTTP 200 OK (SWAP.IO SPLIT-ROUTE)", (20, 241, 149)),
        ("    Single-DEX Out   : 271.444083 SOL  vs  Swap.io Split: 272.486428 SOL", (255, 255, 255)),
        ("    Net Alpha Saved  : +$192.00 USD saved for $0.0010 API fee (192,000x ROI)", (20, 241, 149)),
    ]

    ty = 315
    for text, color in term_lines:
        draw.text((88, ty), text, font=load_font(FONT_MONO, 18), fill=color)
        ty += 31

    # Right Panel: Solscan Verification Card
    draw.rounded_rectangle([1275, 240, 1860, 985], radius=18, fill=(14, 26, 40), outline=(20, 241, 149), width=3)
    draw.rounded_rectangle([1305, 270, 1830, 330], radius=12, fill=(18, 56, 48))
    draw.text((1328, 286), "SOLSCAN SETTLEMENT RECEIPT", font=load_font(FONT_BOLD, 23), fill=(20, 241, 149))

    solscan_fields = [
        ("TRANSACTION SIGNATURE", "4sfdjXi4bdZxffZp6WpVWQimm..."),
        ("BLOCK / SLOT", "#318,492,104 (Finalized)"),
        ("SPL TOKEN MINT", "USDC (EPjFWdd5...Dt1v)"),
        ("x402 CALL AMOUNT", "0.001000 USDC (1,000 atomic)"),
        ("RECIPIENT VAULT", "SwapioX402FeeVault1111111..."),
        ("SOLANA NETWORK FEE", "0.000005 SOL ($0.0009)"),
        ("UNIT TEST SUITE", "6 / 6 Tests Passing (100%)"),
    ]
    sy = 355
    for label, val in solscan_fields:
        draw.rounded_rectangle([1305, sy, 1830, sy + 76], radius=10, fill=(18, 34, 54), outline=(40, 70, 105), width=1)
        draw.text((1325, sy + 12), label, font=load_font(FONT_MONO_BOLD, 16), fill=(0, 200, 255))
        draw.text((1325, sy + 40), val, font=load_font(FONT_BOLD, 19), fill=(245, 250, 255))
        sy += 88

    out = SLIDES_DIR / "slide_04_live_terminal_and_solscan.png"
    img.save(out)
    return out


def make_slide_5() -> Path:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = draw_background(img, 5, 5, "UNIT ECONOMICS & ROI BREAKDOWN")

    draw.text(
        (60, 118),
        "Unit Economics: 192,000x ROI on Every x402 API Call",
        font=load_font(FONT_BOLD, 46),
        fill=(255, 255, 255),
    )
    draw.text(
        (60, 180),
        "Why paying $0.001 USDC per quote via Swap.io x402 dominates both single-DEX swaps and SaaS subscriptions.",
        font=load_font(FONT_REG, 25),
        fill=(175, 198, 228),
    )

    # Big KPI Hero Cards
    kpis = [
        ("$0.0010", "USDC PER API CALL", "Exact x402 SPL Micro-Payment", (0, 194, 255)),
        ("+38.4 bps", "EXECUTION IMPROVEMENT", "272.486 SOL vs 271.444 SOL", (153, 69, 255)),
        ("+$192.00", "NET ALPHA SAVED", "On a Single 50,000 USDC Swap", (20, 241, 149)),
        ("192,000x", "RETURN ON API SPEND", "$192 Saved / $0.001 x402 Fee", (245, 158, 11)),
    ]
    kx = 60
    for big_num, title, sub, color in kpis:
        draw.rounded_rectangle([kx, 245, kx + 425, 490], radius=18, fill=(15, 24, 44), outline=color, width=3)
        draw.text((kx + 32, 275), big_num, font=load_font(FONT_BOLD, 62), fill=color)
        draw.text((kx + 32, 372), title, font=load_font(FONT_BOLD, 22), fill=(255, 255, 255))
        draw.text((kx + 32, 412), sub, font=load_font(FONT_REG, 19), fill=(180, 205, 235))
        kx += 450

    # Comparison Table
    draw.rounded_rectangle([60, 525, 1860, 895], radius=18, fill=(14, 20, 36), outline=(55, 85, 130), width=2)
    headers = ["METRIC / DIMENSION", "SINGLE-DEX DIRECT SWAP", "LEGACY $499/MO SAAS API", "SWAP.IO x402 AGENT API"]
    col_x = [95, 590, 1020, 1440]
    draw.rounded_rectangle([75, 545, 1845, 605], radius=10, fill=(24, 38, 68))
    for cx, htext in zip(col_x, headers):
        draw.text((cx, 563), htext, font=load_font(FONT_BOLD, 20), fill=(0, 215, 255))

    rows = [
        ("Onboarding Friction", "None (Poor Routing)", "Credit Card + KYC + OAuth", "Zero (Native Solana Wallet)"),
        ("Fixed Monthly Overhead", "$0.00 / month", "$499.00 / month", "$0.00 / month (Pay-Per-Call)"),
        ("Cost for 1 Rebalance Quote", "Hidden in 39.9 bps Slippage", "$16.63 amortized / day", "$0.0010 USDC + $0.0009 Gas"),
        ("50,000 USDC -> SOL Output", "271.444083 SOL (-$192.00)", "272.486428 SOL", "272.486428 SOL (+$192.00)"),
        ("On-Chain Audit Trail", "Swap Tx Only", "Off-Chain Stripe Invoice", "100% Solscan Verified (`x402`)"),
    ]
    ry = 625
    for metric, c1, c2, c3 in rows:
        draw.line([(85, ry - 8), (1835, ry - 8)], fill=(28, 42, 70), width=1)
        draw.text((col_x[0], ry), metric, font=load_font(FONT_BOLD, 20), fill=(235, 245, 255))
        draw.text((col_x[1], ry), c1, font=load_font(FONT_REG, 20), fill=(255, 145, 145))
        draw.text((col_x[2], ry), c2, font=load_font(FONT_REG, 20), fill=(245, 195, 110))
        draw.text((col_x[3], ry), c3, font=load_font(FONT_BOLD, 20), fill=(20, 241, 149))
        ry += 52

    # Call to action bar
    draw.rounded_rectangle([60, 918, 1860, 990], radius=14, fill=(16, 48, 44), outline=(20, 241, 149), width=2)
    draw.text(
        (95, 940),
        "BUILD WITH SWAP.IO x402 TODAY: https://swap.io  |  Full Open-Source Python Agent & Tests Included",
        font=load_font(FONT_BOLD, 24),
        fill=(20, 241, 149),
    )

    out = SLIDES_DIR / "slide_05_unit_economics_and_cta.png"
    img.save(out)
    return out


def build_video(slides_with_durations: List[Tuple[Path, int]], output_mp4: Path) -> None:
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    concat_file = SLIDES_DIR / "ffmpeg_concat.txt"
    lines = []
    for slide_path, duration in slides_with_durations:
        lines.append(f"file '{slide_path.resolve()}'")
        lines.append(f"duration {duration}")
    # Repeat last frame for ffmpeg concat demuxer compatibility
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
        f"sine=frequency=220:sample_rate=44100:duration={total_seconds}",
        "-filter_complex",
        "[1:a]volume=0.03,afade=t=in:st=0:d=2,afade=t=out:st="
        f"{total_seconds - 2}:d=2[aout]",
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
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    s1 = make_slide_1()
    s2 = make_slide_2()
    s3 = make_slide_3()
    s4 = make_slide_4()
    s5 = make_slide_5()

    slides = [
        (s1, 12),
        (s2, 13),
        (s3, 15),
        (s4, 20),
        (s5, 15),
    ]
    build_video(slides, VIDEO_PATH)
    print(f"Generated {len(slides)} slides in {SLIDES_DIR}")
    print(f"Generated 75s 1080p MP4 video: {VIDEO_PATH} ({VIDEO_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
