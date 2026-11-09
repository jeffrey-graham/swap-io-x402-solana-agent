#!/usr/bin/env python3
"""
Unit test suite for Swap.io x402 Autonomous Solana DeFi Execution Agent.
Verifies HTTP 402 challenge parsing, policy guardrails, SPL micro-payment signing,
header injection, Solscan verification, and multi-hop route optimization invariants.
"""

import base64
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from swap_x402_agent import (  # noqa: E402
    USDC_MAINNET_MINT,
    WSOL_MAINNET_MINT,
    SwapX402Agent,
    X402Challenge,
    X402PolicyViolationError,
    X402ProtocolError,
    format_console_telemetry,
)


class TestSwapX402Agent(unittest.TestCase):
    def setUp(self) -> None:
        self.now_ts = 1778342400
        self.agent = SwapX402Agent(
            agent_id="test-aegis-402",
            payer_pubkey="Aegis402TreasuryAgent1111111111111111111111",
            signing_secret="unit-test-secret-seed",
            max_per_call_usdc=0.005,
        )
        self.valid_headers = {
            "X-402-Version": "1.0",
            "X-402-Scheme": "exact-spl-transfer",
            "X-402-Chain": "solana:mainnet-beta",
            "X-402-Recipient": "SwapioX402FeeVault1111111111111111111111111",
            "X-402-Token-Mint": USDC_MAINNET_MINT,
            "X-402-Amount": "1000",
            "X-402-Decimals": "6",
            "X-402-Nonce": "nonce-test-001",
            "X-402-Expiry": str(self.now_ts + 120),
        }

    def test_parse_402_challenge_headers(self) -> None:
        challenge = X402Challenge.from_http_response(
            headers=self.valid_headers, resource_uri="/v1/agent/quote"
        )
        self.assertEqual(challenge.version, "1.0")
        self.assertEqual(challenge.scheme, "exact-spl-transfer")
        self.assertEqual(challenge.recipient, "SwapioX402FeeVault1111111111111111111111111")
        self.assertEqual(challenge.token_mint, USDC_MAINNET_MINT)
        self.assertEqual(challenge.amount_atomic, 1000)
        self.assertAlmostEqual(challenge.amount_ui, 0.001)
        self.assertFalse(challenge.is_expired(now_ts=self.now_ts))

    def test_parse_402_challenge_from_json_body(self) -> None:
        body = {
            "paymentRequirements": {
                "version": "1.0",
                "scheme": "exact-spl-transfer",
                "chain": "solana:mainnet-beta",
                "recipient": "SwapioX402FeeVault1111111111111111111111111",
                "tokenMint": USDC_MAINNET_MINT,
                "amountAtomic": 2500,
                "decimals": 6,
                "nonce": "nonce-json-002",
                "expiresAt": self.now_ts + 90,
            }
        }
        challenge = X402Challenge.from_http_response(headers={}, body=body)
        self.assertEqual(challenge.amount_atomic, 2500)
        self.assertAlmostEqual(challenge.amount_ui, 0.0025)
        self.assertEqual(challenge.nonce, "nonce-json-002")

    def test_reject_malformed_402_challenge(self) -> None:
        with self.assertRaises(X402ProtocolError):
            X402Challenge.from_http_response(headers={"X-402-Amount": "1000"})

        bad_amount = dict(self.valid_headers)
        bad_amount["X-402-Amount"] = "0"
        with self.assertRaises(X402ProtocolError):
            X402Challenge.from_http_response(headers=bad_amount)

    def test_policy_guardrails_reject_excessive_fee_or_bad_recipient(self) -> None:
        # 1. Excessive fee (0.02 USDC > 0.005 USDC cap)
        high_fee_headers = dict(self.valid_headers)
        high_fee_headers["X-402-Amount"] = "20000"
        high_fee_challenge = X402Challenge.from_http_response(high_fee_headers)
        with self.assertRaises(X402PolicyViolationError):
            self.agent.validate_challenge_policy(high_fee_challenge, now_ts=self.now_ts)

        # 2. Untrusted recipient address
        rogue_headers = dict(self.valid_headers)
        rogue_headers["X-402-Recipient"] = "RogueAttackerVault1111111111111111111111111"
        rogue_challenge = X402Challenge.from_http_response(rogue_headers)
        with self.assertRaises(X402PolicyViolationError):
            self.agent.validate_challenge_policy(rogue_challenge, now_ts=self.now_ts)

        # 3. Expired challenge
        expired_headers = dict(self.valid_headers)
        expired_headers["X-402-Expiry"] = str(self.now_ts - 5)
        expired_challenge = X402Challenge.from_http_response(expired_headers)
        with self.assertRaises(X402PolicyViolationError):
            self.agent.validate_challenge_policy(expired_challenge, now_ts=self.now_ts)

    def test_payment_signing_and_header_injection(self) -> None:
        challenge = X402Challenge.from_http_response(self.valid_headers)
        receipt = self.agent.construct_and_sign_x402_payment(
            challenge=challenge, slot=318_492_104, timestamp=self.now_ts
        )
        headers = receipt.to_request_headers()
        self.assertIn("X-PAYMENT", headers)
        self.assertIn("X-Payment-Signature", headers)
        self.assertEqual(headers["X-Payment-Nonce"], "nonce-test-001")

        decoded = json.loads(
            base64.b64decode(headers["X-PAYMENT"].encode("ascii")).decode("utf-8")
        )
        self.assertEqual(decoded["x402Version"], "1.0")
        self.assertEqual(decoded["payload"]["recipient"], challenge.recipient)
        self.assertEqual(decoded["payload"]["amount"], "1000")
        self.assertTrue(receipt.solscan_url.startswith("https://solscan.io/tx/"))

    def test_end_to_end_x402_quote_flow_and_solscan_verification(self) -> None:
        challenge, receipt, verification, quote = self.agent.execute_x402_quote_flow(
            input_mint=USDC_MAINNET_MINT,
            output_mint=WSOL_MAINNET_MINT,
            in_amount_atomic=50_000_000_000,
            now_ts=self.now_ts,
        )
        self.assertTrue(verification.verified)
        self.assertEqual(verification.confirmation_status, "finalized")
        self.assertGreater(quote.out_amount_ui, quote.baseline_single_dex_out_ui)
        self.assertGreater(quote.net_alpha_saved_usd, 100.0)
        self.assertGreater(quote.roi_multiple, 10000.0)

        total_pct = sum(hop.allocation_pct for hop in quote.route_plan)
        self.assertAlmostEqual(total_pct, 100.0, places=4)

        telemetry = format_console_telemetry(challenge, receipt, verification, quote)
        self.assertIn("HTTP 402 Payment Required", telemetry)
        self.assertIn("SOLSCAN ON-CHAIN SETTLEMENT VERIFICATION", telemetry)


if __name__ == "__main__":
    unittest.main(verbosity=2)
