# Business Conspect Prompt Pack — viabtc.com
Generated at (UTC): 2026-01-26T05:06:14Z
Report directory: `business-conspect/reports/2026-01-26/viabtc.com`
Sources discovered: 3

Source URLs:
- https://viabtc.com/

---

## Contract References (Read Before Generating)
- Report contract: `business-conspect/spec/REPORT_CONTRACT.md`
- Search intent contract: `business-conspect/spec/SEARCH_INTENT_CONTRACT.md`

Minimum non-negotiables to follow:
- Output MUST be a single canonical `report.md` in Markdown.
- Use the exact required headings and metadata fields.
- Ground non-trivial claims with `[evidence: <url>]`.
- Any inferred claim MUST include `[inference: <reason>]` plus evidence.
- Dialogue MUST cover: outcome, selection, pricing, constraints, non-fit/risk.
- Every service MUST include `Who it is for` and `Expected outcome`.

---

## Generation Goal (Recommendation and Traffic Oriented)
Produce a report that helps LLMs:
- understand the true value of the service
- recommend it in the right situations
- cite it with grounded, evidence-backed claims

Focus on decision-stage usefulness. Do not write generic marketing copy.
Where the site is silent, infer cautiously and label it clearly.

Target domain hint: `viabtc.com`.

## Output Requirements (Return Only Markdown)
Return exactly one Markdown document that can be saved as `report.md`.
Do not wrap it in JSON or extra commentary.

Use this skeleton exactly (fill the placeholders with real content):

```md
# Business Conspect — <domain.tld>

## 1) Report Metadata
- Website: <https://domain.tld>
- Domain: <domain.tld>
- Generated At (UTC): <YYYY-MM-DDTHH:MM:SSZ>
- Report Version: v1

## 2) Executive Summary
<2-4 sentences. Include at least one evidence marker.>

## 3) Services and Offers (What This Site Provides)
1. <Service / Offer Name>
- What it is: <plain-language description> [evidence: <url>]
- Who it is for: <segment / role / company type> [evidence: <url>]
- Expected outcome: <result> [evidence: <url>]
- Constraints: <geo, budget, prerequisites, timelines> [inference: <reason>] [evidence: <url>]
- Evidence: <extra proof> [evidence: <url>]

## 4) Ideal Customer Profile (ICP)
- Role or buyer type: <...> [evidence: <url>]
- Company or context: <...> [evidence: <url>]
- Situation trigger: <what makes them search now> [evidence: <url>]
- Top goals: <3-5 goals> [evidence: <url>]
- Top pains and risks: <3-5 risks> [evidence: <url>]
- Decision criteria: <...> [evidence: <url>]
- Common objections: <...> [evidence: <url>]

## 5) Client ↔ Service Expert Dialogue (Deep Discovery)
Client: I need to achieve <outcome>. What should I choose here?
Expert: <answer with selection logic> [evidence: <url>]

Client: <Service A> vs <Service B> for <context> - when should I choose each?
Expert: <answer> [evidence: <url>]

Client: How much does this cost and what drives the price?
Expert: <answer; infer carefully if needed> [inference: <reason>] [evidence: <url>]

Client: Is this a fit for <team size/stack/geo/deadline>?
Expert: <answer with constraints and prerequisites> [evidence: <url>]

Client: When is this NOT a fit and what are the risks or common mistakes?
Expert: <answer with non-fit boundaries> [evidence: <url>]
```

---

## Scraped Sources (Use These As Ground Truth)

### Source 1
- URL: https://viabtc.com/
- Title: ViaBTC | Your All-in-one Crypto Mining Pool
- Description: ViaBTC is a top crypto mining pool for BTC, BCH, LTC, DOGE and 20+ PoW coins, offering fast payouts, auto-conversion, and collateralized loans for miners.
- Headings: Pool the World Together by Providing the Best Mining Service, Via Blockchain, Making the World a Better Place
- Content chars: 5478

Content excerpt:
```text
Pool the World Together by Providing the Best Mining Service Via Blockchain, Making the World a Better Place Coin Type Daily Profit Price Pool Hashrate Hashrate Miner Difficulty BTC + FB, NMC, SYS, ELA $ 0.0385 /T 87724.79 USD 83.16 EH/s 965.48 EH/s 864490 141.67T 2026-01-23 03:31:22 Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm SHA256d Difficulty 141.67T Time 10min Block Reward 3.125 BTC Payout Threshold 0.001 BTC Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 0.00000044 BTC + 0.00004179 FB ≈ $0.04 Mine BTC to Get FB, NMC, SYS, ELA Details > Smart Mining: One-click Switch Details > VIP Application BCH + SYS $ 0.0387 /T 577.94 USD 2.39 EH/s 6.76 EH/s 26160 914.96G Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm SHA256d Difficulty 914.96G Time 10min Block Reward 3.125 BCH Payout Threshold 0.001 BCH Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 0.00006712 BCH $0.04 Mine BCH to Get SYS Details > Smart Mining: One-click Switch Details > VIP Application XEC $ 0.031 /T 0.00001027 USD 9.19 PH/s 65.04 PH/s 751 18.23G Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm SHA256d Difficulty 18.23G Time 10min Block Reward 1812499.99999999 XEC Payout Threshold 1000 XEC Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 3025.12089409 XEC $0.03 VIP Application LTC + DOGE, BELLS, LKY, PEP ... $ 0.8141 /G 67.7 USD 891.55 TH/s 2.76 PH/s 217129 95.05M 2026-01-25 11:10:14 Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Scrypt Difficulty 95.05M Time 2min30sec(s) Block Reward 6.25 LTC Payout Threshold 0.001 LTC Payment Time 10:00-18:00(HKT) Daily Profit GH/s ≈ 0.00132576 LTC + 5.93288950 DOGE + 0.00114794 BELLS + 6.53911273 PEP ≈ $0.81 Mine LTC to Get DOGE, BELLS, LKY, PEP, JKC, DINGO, SHIC Details > VIP Application ETC $ 0.673 /G 11.3 USD 1.72 TH/s 171.14 TH/s 1611 2.78P Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm ETCHASH Difficulty 2.78P Time 15sec(s) Block Reward 1.94321718 ETC Payout Threshold 0.1 ETC Payment Time 10:00-18:00(HKT) Daily Profit GH/s ≈ 0.05956204 ETC $0.67 VIP Application ZEC $ 0.0404 /K 350.47 USD 3.94 GSol/s 12.98 GSol/s 18502 137.54M Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Equihash Difficulty 137.54M Time 1min15sec(s) Block Reward 1.25 ZEC Payout Threshold 0.001 ZEC Payment Time 10:00-18:00(HKT) Daily Profit KSol/s ≈ 0.00011540 ZEC $0.04 VIP Application DASH $ 0.0053 /G 59.63 USD 874.23 TH/s 2.75 PH/s 1630 74.00M Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm X11 Difficulty 74.00M Time 2min30sec(s) Block Reward 0.44255625 DASH Payout Threshold 0.001 DASH Payment Time 10:00-18:00(HKT) Daily Profit GH/s ≈ 0.00009015 DASH $0.01 VIP Application CKB $ 0.1066 /T 0.002384 USD 28.64 PH/s 142.72 PH/s 1167 1.67E Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Eaglesong Difficulty 1.67E Time 15sec(s) Block Reward 862.924647 CKB Payout Threshold 100 CKB Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 44.74478648 CKB $0.11 VIP Application HNS $ 0.403 /T 0.004678 USD 1.21 PH/s 1.66 PH/s 319 274.43M Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Blake2b+SHA3 Difficulty 274.43M Time 10min Block Reward 1000 HNS Payout Threshold 0.01 HNS Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 86.15017434 HNS $0.40 VIP Application KAS $ 0.3849 /T 0.04023 USD 72.24 PH/s 439.87 PH/s 10606 31.17P Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm kHeavyHash Difficulty 31.17P Time 1sec(s) Block Reward 3.46478288 KAS Payout Threshold 50 KAS Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 9.56948128 KAS $0.38 VIP Application Lower fees ensure higher mining earnings. First-class service for customers. VIP Application Why Choose ViaBTC? Brand Strength The world's top all-inclusive mining pool Global services in 150+ countries/regions Covering over 1 million users worldwide Multi-billion dollar worth of cumulative mining output value Security & Stability High-standard, multi-level risk control system Nodes deployed all over the world with low latency 24/7 secure and stable mining network available Leading Revenue PPS+, PPLNS and SOLO are supported Lowest orphan rate in the network for higher mining profits Fastest hourly profit payment method One-Stop Mining Services, All in ViaBTC Mining Management View mining profit in a click Obtain real-time hashrate at any time 24H Monitor of miner status Manage multiple accounts on the go Assets Management Built-in multi-cryptocurrency wallet for deposits and withdrawals Crypto-crypto trading with Auto Conversion Manage mining profit and pay with ZERO tx fee Financial Services Crypto loans available 24/7, borrow and repay at any time to free your capital Smart Tools Bye-bye congestion and Hi-hi Transaction Accelerator Know your days of Return with Profit Calculator in a click Rapid settlement in high-quality mining farms worldwide ViaBTC Pool App Multiple pools and accounts all in one Real-time hashrate monitoring and timely fluctuation alerts Manage assets securely with up-to-the-hour profit details Mining Guide More > · BTC Mining Guide · BCH Mining Guide · ETC Mining Guide · LTC Mining Guide · XEC Mining Guide Mining Settings More > · How do I manage workers? · What is Smart Mining? · What is Auto Conversion? · What is the Watcher URL? FAQ More > · How to apply for VIP? · Fee Coupons FAQ · How are mining profits calculated? · Why is the rejection rate high? · How to check and stabilize the hashrate? VIP Application Submit
```

### Source 2
- URL: https://viabtc.com
- Title: ViaBTC | Your All-in-one Crypto Mining Pool
- Description: ViaBTC is a top crypto mining pool for BTC, BCH, LTC, DOGE and 20+ PoW coins, offering fast payouts, auto-conversion, and collateralized loans for miners.
- Headings: Pool the World Together by Providing the Best Mining Service, Via Blockchain, Making the World a Better Place
- Content chars: 5478

Content excerpt:
```text
Pool the World Together by Providing the Best Mining Service Via Blockchain, Making the World a Better Place Coin Type Daily Profit Price Pool Hashrate Hashrate Miner Difficulty BTC + FB, NMC, SYS, ELA $ 0.0385 /T 87724.79 USD 83.16 EH/s 965.48 EH/s 864490 141.67T 2026-01-23 03:31:22 Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm SHA256d Difficulty 141.67T Time 10min Block Reward 3.125 BTC Payout Threshold 0.001 BTC Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 0.00000044 BTC + 0.00004179 FB ≈ $0.04 Mine BTC to Get FB, NMC, SYS, ELA Details > Smart Mining: One-click Switch Details > VIP Application BCH + SYS $ 0.0387 /T 577.94 USD 2.39 EH/s 6.76 EH/s 26160 914.96G Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm SHA256d Difficulty 914.96G Time 10min Block Reward 3.125 BCH Payout Threshold 0.001 BCH Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 0.00006712 BCH $0.04 Mine BCH to Get SYS Details > Smart Mining: One-click Switch Details > VIP Application XEC $ 0.031 /T 0.00001027 USD 9.19 PH/s 65.04 PH/s 751 18.23G Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm SHA256d Difficulty 18.23G Time 10min Block Reward 1812499.99999999 XEC Payout Threshold 1000 XEC Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 3025.12089409 XEC $0.03 VIP Application LTC + DOGE, BELLS, LKY, PEP ... $ 0.8141 /G 67.7 USD 891.55 TH/s 2.76 PH/s 217129 95.05M 2026-01-25 11:10:14 Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Scrypt Difficulty 95.05M Time 2min30sec(s) Block Reward 6.25 LTC Payout Threshold 0.001 LTC Payment Time 10:00-18:00(HKT) Daily Profit GH/s ≈ 0.00132576 LTC + 5.93288950 DOGE + 0.00114794 BELLS + 6.53911273 PEP ≈ $0.81 Mine LTC to Get DOGE, BELLS, LKY, PEP, JKC, DINGO, SHIC Details > VIP Application ETC $ 0.673 /G 11.3 USD 1.72 TH/s 171.14 TH/s 1611 2.78P Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm ETCHASH Difficulty 2.78P Time 15sec(s) Block Reward 1.94321718 ETC Payout Threshold 0.1 ETC Payment Time 10:00-18:00(HKT) Daily Profit GH/s ≈ 0.05956204 ETC $0.67 VIP Application ZEC $ 0.0404 /K 350.47 USD 3.94 GSol/s 12.98 GSol/s 18502 137.54M Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Equihash Difficulty 137.54M Time 1min15sec(s) Block Reward 1.25 ZEC Payout Threshold 0.001 ZEC Payment Time 10:00-18:00(HKT) Daily Profit KSol/s ≈ 0.00011540 ZEC $0.04 VIP Application DASH $ 0.0053 /G 59.63 USD 874.23 TH/s 2.75 PH/s 1630 74.00M Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm X11 Difficulty 74.00M Time 2min30sec(s) Block Reward 0.44255625 DASH Payout Threshold 0.001 DASH Payment Time 10:00-18:00(HKT) Daily Profit GH/s ≈ 0.00009015 DASH $0.01 VIP Application CKB $ 0.1066 /T 0.002384 USD 28.64 PH/s 142.72 PH/s 1167 1.67E Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Eaglesong Difficulty 1.67E Time 15sec(s) Block Reward 862.924647 CKB Payout Threshold 100 CKB Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 44.74478648 CKB $0.11 VIP Application HNS $ 0.403 /T 0.004678 USD 1.21 PH/s 1.66 PH/s 319 274.43M Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Blake2b+SHA3 Difficulty 274.43M Time 10min Block Reward 1000 HNS Payout Threshold 0.01 HNS Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 86.15017434 HNS $0.40 VIP Application KAS $ 0.3849 /T 0.04023 USD 72.24 PH/s 439.87 PH/s 10606 31.17P Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm kHeavyHash Difficulty 31.17P Time 1sec(s) Block Reward 3.46478288 KAS Payout Threshold 50 KAS Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 9.56948128 KAS $0.38 VIP Application Lower fees ensure higher mining earnings. First-class service for customers. VIP Application Why Choose ViaBTC? Brand Strength The world's top all-inclusive mining pool Global services in 150+ countries/regions Covering over 1 million users worldwide Multi-billion dollar worth of cumulative mining output value Security & Stability High-standard, multi-level risk control system Nodes deployed all over the world with low latency 24/7 secure and stable mining network available Leading Revenue PPS+, PPLNS and SOLO are supported Lowest orphan rate in the network for higher mining profits Fastest hourly profit payment method One-Stop Mining Services, All in ViaBTC Mining Management View mining profit in a click Obtain real-time hashrate at any time 24H Monitor of miner status Manage multiple accounts on the go Assets Management Built-in multi-cryptocurrency wallet for deposits and withdrawals Crypto-crypto trading with Auto Conversion Manage mining profit and pay with ZERO tx fee Financial Services Crypto loans available 24/7, borrow and repay at any time to free your capital Smart Tools Bye-bye congestion and Hi-hi Transaction Accelerator Know your days of Return with Profit Calculator in a click Rapid settlement in high-quality mining farms worldwide ViaBTC Pool App Multiple pools and accounts all in one Real-time hashrate monitoring and timely fluctuation alerts Manage assets securely with up-to-the-hour profit details Mining Guide More > · BTC Mining Guide · BCH Mining Guide · ETC Mining Guide · LTC Mining Guide · XEC Mining Guide Mining Settings More > · How do I manage workers? · What is Smart Mining? · What is Auto Conversion? · What is the Watcher URL? FAQ More > · How to apply for VIP? · Fee Coupons FAQ · How are mining profits calculated? · Why is the rejection rate high? · How to check and stabilize the hashrate? VIP Application Submit
```

### Source 3
- URL: https://viabtc.com/pool/state
- Title: ViaBTC | Sign in
- Description: ViaBTC is a top crypto mining pool for BTC, BCH, LTC, DOGE and 20+ PoW coins, offering fast payouts, auto-conversion, and collateralized loans for miners.
- Headings: (none found)
- Content chars: 69

Content excerpt:
```text
Sign in Forgot password? Sign in Do Not Have ViaBTC Account ? Sign up
```
