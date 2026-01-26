# Business Conspect Prompt Pack — viabtc.com
        Generated at (UTC): 2026-01-26T05:40:37Z
        Report directory: `business-conspect/reports/2026-01-26/viabtc.com`
        Sources discovered: 4

        Source URLs:
        - https://viabtc.com/
- https://viabtc.com/aboutus
- https://viabtc.com/wallet
- https://viabtc.com/en/finance/loan

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
- Content chars: 5483

Content excerpt:
```text
Pool the World Together by Providing the Best Mining Service Via Blockchain, Making the World a Better Place Coin Type Daily Profit Price Pool Hashrate Hashrate Miner Difficulty BTC + FB, NMC, SYS, ELA $ 0.0386 /T 87836.3 USD 86.91 EH/s 965.48 EH/s 899269 141.67T 2026-01-23 03:31:22 Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm SHA256d Difficulty 141.67T Time 10min Block Reward 3.125 BTC Payout Threshold 0.001 BTC Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 0.00000044 BTC + 0.00004207 FB ≈ $0.04 Mine BTC to Get FB, NMC, SYS, ELA Details > Smart Mining: One-click Switch Details > VIP Application BCH + SYS $ 0.0388 /T 578.14 USD 2.42 EH/s 6.76 EH/s 26017 913.74G Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm SHA256d Difficulty 913.74G Time 10min Block Reward 3.125 BCH Payout Threshold 0.001 BCH Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 0.00006716 BCH $0.04 Mine BCH to Get SYS Details > Smart Mining: One-click Switch Details > VIP Application XEC $ 0.0309 /T 0.00001027 USD 10.06 PH/s 65.04 PH/s 765 9.12G Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm SHA256d Difficulty 9.12G Time 10min Block Reward 1812499.99999999 XEC Payout Threshold 1000 XEC Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 3013.96589624 XEC $0.03 VIP Application LTC + DOGE, BELLS, LKY, PEP ... $ 0.8065 /G 67.71 USD 856.72 TH/s 2.76 PH/s 216156 95.05M 2026-01-25 11:10:14 Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Scrypt Difficulty 95.05M Time 2min30sec(s) Block Reward 6.25 LTC Payout Threshold 0.001 LTC Payment Time 10:00-18:00(HKT) Daily Profit GH/s ≈ 0.00132577 LTC + 5.87982206 DOGE + 0.00114839 BELLS + 6.46130374 PEP ≈ $0.81 Mine LTC to Get DOGE, BELLS, LKY, PEP, JKC, DINGO, SHIC Details > VIP Application ETC $ 0.6753 /G 11.31 USD 1.68 TH/s 171.14 TH/s 1663 2.77P Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm ETCHASH Difficulty 2.77P Time 15sec(s) Block Reward 1.94321718 ETC Payout Threshold 0.1 ETC Payment Time 10:00-18:00(HKT) Daily Profit GH/s ≈ 0.05971585 ETC $0.68 VIP Application ZEC $ 0.0402 /K 351.18 USD 3.93 GSol/s 12.98 GSol/s 18503 122.24M Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Equihash Difficulty 122.24M Time 1min15sec(s) Block Reward 1.25 ZEC Payout Threshold 0.001 ZEC Payment Time 10:00-18:00(HKT) Daily Profit KSol/s ≈ 0.00011463 ZEC $0.04 VIP Application DASH $ 0.0054 /G 59.76 USD 879.45 TH/s 2.75 PH/s 1606 84.69M Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm X11 Difficulty 84.69M Time 2min30sec(s) Block Reward 0.44255625 DASH Payout Threshold 0.001 DASH Payment Time 10:00-18:00(HKT) Daily Profit GH/s ≈ 0.00009084 DASH $0.01 VIP Application CKB $ 0.1063 /T 0.002376 USD 28.51 PH/s 142.72 PH/s 1140 1.67E Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Eaglesong Difficulty 1.67E Time 15sec(s) Block Reward 862.92449056 CKB Payout Threshold 100 CKB Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 44.74507966 CKB $0.11 VIP Application HNS $ 0.3995 /T 0.004639 USD 1.22 PH/s 1.66 PH/s 319 272.28M Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm Blake2b+SHA3 Difficulty 272.28M Time 10min Block Reward 1000 HNS Payout Threshold 0.01 HNS Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 86.13107564 HNS $0.40 VIP Application KAS $ 0.3839 /T 0.04024 USD 82.83 PH/s 439.87 PH/s 14368 33.84P Guide 30-Day Hashrate Chart Hashrate Pool Hashrate Algorithm kHeavyHash Difficulty 33.84P Time 1sec(s) Block Reward 3.46478288 KAS Payout Threshold 50 KAS Payment Time 10:00-18:00(HKT) Daily Profit TH/s ≈ 9.54188497 KAS $0.38 VIP Application Lower fees ensure higher mining earnings. First-class service for customers. VIP Application Why Choose ViaBTC? Brand Strength The world's top all-inclusive mining pool Global services in 150+ countries/regions Covering over 1 million users worldwide Multi-billion dollar worth of cumulative mining output value Security & Stability High-standard, multi-level risk control system Nodes deployed all over the world with low latency 24/7 secure and stable mining network available Leading Revenue PPS+, PPLNS and SOLO are supported Lowest orphan rate in the network for higher mining profits Fastest hourly profit payment method One-Stop Mining Services, All in ViaBTC Mining Management View mining profit in a click Obtain real-time hashrate at any time 24H Monitor of miner status Manage multiple accounts on the go Assets Management Built-in multi-cryptocurrency wallet for deposits and withdrawals Crypto-crypto trading with Auto Conversion Manage mining profit and pay with ZERO tx fee Financial Services Crypto loans available 24/7, borrow and repay at any time to free your capital Smart Tools Bye-bye congestion and Hi-hi Transaction Accelerator Know your days of Return with Profit Calculator in a click Rapid settlement in high-quality mining farms worldwide ViaBTC Pool App Multiple pools and accounts all in one Real-time hashrate monitoring and timely fluctuation alerts Manage assets securely with up-to-the-hour profit details Mining Guide More > · BTC Mining Guide · BCH Mining Guide · ETC Mining Guide · LTC Mining Guide · XEC Mining Guide Mining Settings More > · How do I manage workers? · What is Smart Mining? · What is Auto Conversion? · What is the Watcher URL? FAQ More > · How to apply for VIP? · Fee Coupons FAQ · How are mining profits calculated? · Why is the rejection rate high? · How to check and stabilize the hashrate? VIP Application Submit
```

### Source 2
- URL: https://viabtc.com/aboutus
- Title: ViaBTC | About Us
- Description: ViaBTC is a top crypto mining pool for BTC, BCH, LTC, DOGE and 20+ PoW coins, offering fast payouts, auto-conversion, and collateralized loans for miners.
- Headings: Brand Strength, Secure & Stable, Leading Revenue, Mining Pool, Exchange, Investment, Wallet, Multi-Sig Wallet, Explorer, Public Chain
- Content chars: 3804

Content excerpt:
```text
About Us Founded in May 2016, ViaBTC is an innovation-driven blockchain service provider that boasts abundant experience, extensive investments, secure and reliable products, and a global user base. Relying on the advanced Fintech, we aim to catalyze progress in the blockchain industry, build a better future for the blockchain, and fulfil our mission - “Via Blockchain, Making The World A Better Place”. Team ViaBTC has a top-notch multinational team with members all over the world. They used to work for world-leading Internet and financial companies, and many of them stepped into the cryptocurrency market in the earliest days as practitioners, pioneers, and investors. At present, the product team and the R&D team account for more than 60% of ViaBTC's workforce, supporting the company with rich development experience and strong technical capacity. ViaBTC aspires to gather more highly educated, high-calibre talents as its brainpower to provide secure and stable one-stop mining services for over 1 million users across 150+ countries/regions and to drive the technological innovation and development in the blockchain industry. Milestones 2025 2024 2023 2022 2021 2020 2019 2018 2017 2016 Why ViaBTC Brand Strength The world's top all-inclusive mining pool Global services in 150+ countries/regions Covering over 1 million users worldwide Multi-billion dollar worth of cumulative mining output value Secure & Stable High-standard, multi-level risk control system Nodes deployed all over the world with low latency 24/7 secure and stable mining network available Leading Revenue PPS+, PPLNS and SOLO are supported Lowest orphan rate in the network for higher mining profits Fastest hourly profit payment method Ecosystem Mining Pool ViaBTC - A comprehensive global cryptocurrency pool serving over 1,000,000 users in over 150 countries/regions with professional, efficient, stable and secure mining service. Exchange CoinEx - Founded in 2017, a global cryptocurrency trading platform with a “user first” brand ethos, offers an array of products and services including Spot, Futures, Margin Trading, Crypto Loans, and Strategic Trading. Investment ViaBTC Capital - The investment arm of ViaBTC Group, manages a $100 million portfolio that includes over 50 blockchain projects and acts as a LP in prestigious funds. The firm actively expands its presence in key ecosystems like Bitcoin, Solana, Sui, and emerging areas such as LSD/ReStaking, DePIN, and AI. Wallet CoinEx Wallet - CoinEx decentralized multi-chain wallet offers integrated and seamless features to enhance the Web3 experience – supporting 53+ mainstream blockchains and 1M+ tokens. Multi-Sig Wallet By combining multi-signature with cold wallet mode and integrating mechanisms such as off-chain approval, three-end mutually distrusting framework, and transaction monitoring, we provide a secure, flexible, and efficient asset management solution for individuals and teams. Explorer CoinEx Explorer - A multi-cryptocurrency blockchain explorer created by CoinEx. It provides encrypted data information such as block data, network hashrate, transactions, mining, and active addresses, supports tools like transaction acceleration. Public Chain CoinEx Smart Chain - A decentralized, permissionless, high-efficiency smart contract chain tailored for DeFi applications. It offers developers a user-friendly environment for smart contract deployment and enriches the DeFi experience for users. Contact Us Asia-Pacific Paphy Cai [email protected] Logan Li [email protected] Americas Region Phillip Wang [email protected] CIS-EU-Middle East Anton Tsarenok [email protected] Alina Kakicheva [email protected] Africa Jingyang [email protected] Media Cooperation [email protected] Customer Service [email protected] or Submit Request Partners
```

### Source 3
- URL: https://viabtc.com/wallet
- Title: ViaBTC | Sign in
- Description: ViaBTC is a top crypto mining pool for BTC, BCH, LTC, DOGE and 20+ PoW coins, offering fast payouts, auto-conversion, and collateralized loans for miners.
- Headings: (none found)
- Content chars: 69

Content excerpt:
```text
Sign in Forgot password? Sign in Do Not Have ViaBTC Account ? Sign up
```

### Source 4
- URL: https://viabtc.com/en/finance/loan
- Title: ViaBTC | Collateral-Pledged Loans
- Description: ViaBTC is a top crypto mining pool for BTC, BCH, LTC, DOGE and 20+ PoW coins, offering fast payouts, auto-conversion, and collateralized loans for miners.
- Headings: (none found)
- Content chars: 904

Content excerpt:
```text
Switch Account Switch Now Collateral-Pledged Loans Flexible Funding. Lightning Approval. Borrow & Repay Anytime Borrow Introduction to Collateral-Pledged Loans "Collateral-Pledged Loans" is a financial service designed for miners, offering flexible liquidity solutions. It’s ideal for those who hold cryptocurrencies for long-term value but still need funds to cover operating expenses like electricity and miner maintenance. Miners can pledge their crypto assets to borrow from ViaBTC. Once the loan is fully repaid, the collateral will be returned to them. Loan Process 01 Add Collateral 02 Apply for Loan 03 Receive Loan 04 Repay Loan 05 Redeem Collateral Borrow No Data Collateral Assets No Data Loan Details (null) Repay FAQ More ※ All the above contents are for ViaBTC Collateral-Pledged Loans introduction only and not represent any investment advice. About Collateral-Pledged Loans Add Collateral
```
