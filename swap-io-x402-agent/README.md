# Swap.io `x402` Autonomous Solana DeFi Execution Agent (`Aegis-402`)

Submission repository for the **Swap.io — Make a video about our x402 Feature** bounty on Superteam Earn (`https://earn.superteam.fun/listings/bounty/make-a-video-about-our-x402-feature`).

## Repository Structure

- `src/swap_x402_agent.py`: Autonomous Solana DeFi Execution & Route Intelligence Agent implementing the HTTP `402 Payment Required` (`x402`) handshake with Swap.io's Agent API, autonomous policy guardrails, SPL micro-payment signing, `X-PAYMENT` Base64 proof header construction, and Solscan transaction verification (`+30% Bonus`).
- `tests/test_x402_agent.py`: 6-test unit suite verifying 402 header/JSON parsing, policy guardrails, signature & header injection, and route optimization invariants.
- `scripts/generate_x402_video.py`: Generates 5 high-resolution 1080p slide PNGs (`output/slides/*.png`) and the 75-second 1080p MP4 video (`output/swap_io_x402_pitch_video.mp4`).
- `MEDIUM_ARTICLE.md`: Publication-ready Medium technical deep-dive article.
- `X_THREAD_AND_SUBMISSION.md`: X video thread, timed voiceover script, and Superteam Earn submission fields.

## Quickstart

```bash
# Run unit tests
python3 tests/test_x402_agent.py

# Run live console telemetry & JSON output
python3 src/swap_x402_agent.py --amount-usdc 50000 --json

# Regenerate 1080p slides & 75s MP4 video
python3 scripts/generate_x402_video.py
```
