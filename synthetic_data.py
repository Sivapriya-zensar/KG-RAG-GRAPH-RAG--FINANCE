"""
synthetic_data.py
-----------------
Comprehensive synthetic financial corpus and KG triples.
Extended dataset: 10 firms, 200+ documents, 150+ relationships.
All entities are anonymized for academic research purposes.
No real company names or identifiable entities are used.
"""

# ─────────────────────────────────────────────
# 200+ Synthetic Financial Documents
# ─────────────────────────────────────────────
DOCUMENTS = [
    # Firm_A
    "Firm_A reported revenue of 120M USD in Year 1, representing a 15% increase over the prior period.",
    "Firm_A acquired Firm_B in Year 1 for a total consideration of 45M USD, expanding its market presence.",
    "Firm_A holds Equity_X as its primary listed instrument with a market capitalization of 500M USD.",
    "Firm_A disclosed a net profit of 30M USD for Year 1, reflecting 25% profit margin.",
    "Firm_A's total assets reached 450M USD, with liabilities of 150M USD in Year 1.",
    "Firm_A expanded into three new markets in Year 1, driving 18% growth in customer base.",
    "Firm_A's R&D spending increased to 18M USD, up 22% from previous year.",
    "Firm_A issued Bond_A with 5.5% coupon rate, raising 80M USD in capital.",
    "Firm_A announced dividend payout of 8M USD to shareholders in Year 1.",
    "Firm_A achieved ROE of 25% and ROA of 12%, outperforming sector benchmarks.",
    
    # Firm_B
    "Firm_B carries a high price-to-earnings ratio of 28x, indicating strong growth expectations.",
    "Firm_B was acquired by Firm_A in Year 1 for 45M USD, marking strategic consolidation.",
    "Firm_B reported Year 1 revenue of 95M USD with 32% YoY growth rate.",
    "Firm_B's operating profit reached 22M USD, with EBITDA margin of 28%.",
    "Firm_B has 200 employees across five regional offices.",
    "Firm_B invested 12M USD in technology infrastructure in Year 1.",
    "Firm_B's customer retention rate improved to 92%, up from 85% in prior year.",
    "Firm_B issued Equity_B with 3M shares outstanding at 15 USD per share.",
    "Firm_B maintains debt-to-equity ratio of 0.45, indicating healthy leverage.",
    "Firm_B's market share grew to 15% in its core segment.",
    
    # Firm_C
    "Firm_C reported revenue of 80M USD and profit of 12M USD in Year 1.",
    "Firm_C issued Bond_Y with 6% coupon rate, maturing in Year 5.",
    "Firm_C's net profit margin of 15% demonstrates operational efficiency.",
    "Firm_C operates 12 manufacturing facilities across four countries.",
    "Firm_C's supply chain optimization reduced costs by 8M USD in Year 1.",
    "Firm_C achieved asset turnover ratio of 1.8, indicating efficient asset utilization.",
    "Firm_C invested 6M USD in sustainability initiatives.",
    "Firm_C's customer base grew to 500+ enterprise clients.",
    "Firm_C's working capital improvement freed up 5M USD in cash flow.",
    
    # Firm_D
    "Firm_D reported Year 1 revenue of 150M USD with 12% growth rate.",
    "Firm_D's net income reached 25M USD, reflecting 16.7% profit margin.",
    "Firm_D acquired Firm_E in Year 1 for 35M USD in cash and stock.",
    "Firm_D issued Equity_D with 5M shares at 20 USD per share.",
    "Firm_D maintains 250M USD in total assets and 100M USD in liabilities.",
    "Firm_D's quick ratio of 1.5 indicates strong short-term liquidity.",
    "Firm_D expanded warranty services, generating additional 5M USD revenue.",
    "Firm_D's effective tax rate was 24% in Year 1.",
    "Firm_D obtained credit facility of 50M USD for strategic investments.",
    
    # Firm_E
    "Firm_E pre-acquisition revenue totaled 35M USD in Year 1.",
    "Firm_E was acquired by Firm_D for 35M USD, comprising 20M cash and 15M stock.",
    "Firm_E achieved 28% YoY revenue growth prior to acquisition.",
    "Firm_E had 85 employees focused on software development.",
    "Firm_E's monthly recurring revenue reached 2.8M USD at acquisition.",
    "Firm_E operates SaaS platform serving 150+ customers.",
    "Firm_E's gross margin stood at 72%, typical for software business.",
    "Firm_E required 8M USD for contingent liabilities post-acquisition.",
    
    # Firm_F
    "Firm_F reported revenue of 200M USD, making it the sector leader.",
    "Firm_F issued Bond_F with 4.8% coupon rate, raising 120M USD.",
    "Firm_F maintains industry-leading ROE of 32% and ROA of 18%.",
    "Firm_F has 1200+ employees across 15 countries.",
    "Firm_F's total assets exceed 600M USD with debt of 200M USD.",
    "Firm_F invested 30M USD in R&D and innovation initiatives.",
    "Firm_F acquired three companies in Year 1 for combined 80M USD.",
    "Firm_F's operating cash flow reached 65M USD.",
    "Firm_F declared special dividend of 10M USD plus regular 8M USD.",
    "Firm_F achieved Equity_F valuation of 1.2B USD.",
    
    # Firm_G
    "Firm_G reported Year 1 revenue of 110M USD with steady 8% growth.",
    "Firm_G holds strategic investments in five emerging market firms.",
    "Firm_G issued convertible Bond_G at 4.5% coupon with 3 USD conversion price.",
    "Firm_G maintains 300M USD in assets and 120M USD in liabilities.",
    "Firm_G's segment A contributed 50M USD revenue, segment B 35M USD, segment C 25M USD.",
    "Firm_G achieved order backlog of 40M USD for next two years.",
    "Firm_G invested 15M USD in facility expansions.",
    "Firm_G's customer concentration is limited with top 5 customers at 25% of revenue.",
    
    # Firm_H
    "Firm_H reported revenue of 90M USD with 6% YoY growth.",
    "Firm_H issued Equity_H with 2M shares, raising 40M USD at 20 USD per share.",
    "Firm_H maintains strong balance sheet with 180M USD in assets.",
    "Firm_H's debt obligations total 60M USD, with maturity schedule well-distributed.",
    "Firm_H achieved gross margin of 42%, operational improvement of 2%.",
    "Firm_H invested 10M USD in marketing and brand building.",
    "Firm_H's capital expenditure budget is 12M USD for Year 2.",
    "Firm_H maintains partnership with 50+ distribution partners.",
    
    # Firm_I
    "Firm_I reported revenue of 85M USD, primarily from product sales.",
    "Firm_I issued Bond_I at 5.2% coupon maturing in Year 7.",
    "Firm_I maintains 200M USD in total assets and 70M USD in liabilities.",
    "Firm_I achieved EBITDA of 15M USD with 17.6% EBITDA margin.",
    "Firm_I invested 8M USD in technology and infrastructure upgrades.",
    "Firm_I purchased two smaller competitors for combined 22M USD.",
    "Firm_I's customer acquisition cost decreased 15% through efficiency gains.",
    "Firm_I's inventory turnover improved to 4.2x annually.",
    
    # Firm_J
    "Firm_J reported Year 1 revenue of 105M USD with 10% growth rate.",
    "Firm_J issued Equity_J with 1.5M shares at 28 USD per share.",
    "Firm_J maintains 280M USD in assets and 90M USD in liabilities.",
    "Firm_J achieved net profit of 18M USD, reflecting 17.1% margin.",
    "Firm_J invested 14M USD in employee training and development.",
    "Firm_J established joint venture with international partner.",
    "Firm_J's operating cash flow reached 22M USD.",
    "Firm_J maintains strong credit rating with interest coverage of 8.2x.",
    
    # Cross-firm Relationships
    "Diversification across asset classes including Equity_X and Bond_Y reduces portfolio risk.",
    "Strategic partnerships between Firm_A and Firm_F generated 5M USD in joint revenue.",
    "Supply chain collaboration between Firm_C and Firm_D reduced costs by 3M USD.",
    "Joint venture between Firm_B and Firm_I targets emerging markets.",
    "Technology licensing agreement between Firm_E and Firm_H worth 2M USD annually.",
    "Distribution agreement between Firm_A and Firm_G expanded reach to 50 new customers.",
    "Firm_D and Firm_J formed consortium for infrastructure project valued at 30M USD.",
    "Cross-licensing agreement between Firm_F and Firm_C reduces R&D spending.",
    "Firm_H became authorized reseller for Firm_A products in region X.",
    "Firm_I supplied components to Firm_D with 8M USD annual contract.",
    
    # Financial Metrics & Analysis
    "Sector average PE ratio is 18x, with Firm_F trading at 22x reflecting premium valuation.",
    "Dividend yield across the sector averages 2.5%, with Firm_A at 3.2% providing above-average income.",
    "Debt-to-equity ratios vary from 0.3x (Firm_A) to 0.8x (Firm_C).",
    "Revenue growth rates range from 6% (Firm_H) to 32% (Firm_B).",
    "Profit margins vary from 12% (Firm_C) to 25% (Firm_A).",
    "ROE varies from 15% (Firm_H) to 32% (Firm_F).",
    "Asset turnover ratios range from 1.4x (Firm_F) to 2.1x (Firm_I).",
    "Current ratios indicate strong liquidity across all firms, averaging 1.6x.",
    "Interest coverage ratios exceed 5x for all firms, indicating low default risk.",
    "Working capital as percentage of revenue ranges from 8% to 15%.",
    
    # Market Events
    "Sector saw 5 major M&A transactions in Year 1 totaling 200M USD.",
    "Three IPOs occurred in related sectors, raising 150M USD combined.",
    "Industry consolidation trend accelerated with 15 acquisitions in Year 1.",
    "Regulatory changes improved profitability for sector by estimated 2-3%.",
    "New market entrant disrupted pricing in segment B by 15%.",
    "Commodity price inflation increased input costs by 8% across sector.",
    "Currency fluctuations impacted exporters' margins by 1-2%.",
    "Interest rate rise to 4.5% increased financing costs for leveraged firms.",
    "Technology disruption created new growth opportunities worth 500M USD market.",
    "Pandemic recovery drove demand surge of 20% in certain segments.",
    
    # Operational Metrics
    "Average employee productivity increased 12% through automation initiatives.",
    "Customer satisfaction scores improved from 78 to 85 across all firms.",
    "Cycle time reduction initiatives delivered 3M USD in efficiency gains.",
    "Supply chain resilience improved through multi-sourcing strategy.",
    "Digital transformation initiatives generated 25M USD in combined net benefits.",
    "Sustainability investments contributed to 5% cost reduction through efficiency.",
    "Quality improvement programs reduced defect rates by 40%.",
    "On-time delivery performance improved to 96% across the sector.",
    "inventory carrying costs reduced 15% through optimization.",
    "Order fulfillment time decreased from 14 days to 10 days average.",
    
    # Investment & Growth
    "Venture capital funding in adjacent sectors reached 300M USD in Year 1.",
    "Private equity firms acquired 2 sector companies for 120M USD combined.",
    "Strategic investors increased stakes in 6 companies.",
    "Infrastructure investments totaled 80M USD for capacity expansion.",
    "Technology investments reached 60M USD across all firms.",
    "Working capital optimization freed up 25M USD in cash.",
    "Dividend payments totaled 50M USD across all firms in Year 1.",
    "Share buyback programs repurchased 15M USD of stock.",
    "Earn-out payments for prior M&A totaled 18M USD.",
    
    # Risk & Compliance
    "All firms maintain compliance with new regulatory framework.",
    "Cybersecurity incidents affected 2 firms with 5M USD aggregate impact.",
    "Credit default swap spreads narrowed by 50 bps for sector leaders.",
    "Litigation exposure remains modest at 8M USD aggregate.",
    "Insurance coverage includes 250M USD umbrella policy.",
    "Revenue concentration risk identified at 3 major firms.",
    "Geographic concentration in region Y represents 40% of sector revenue.",
    "Currency risk hedged for 60% of expected foreign currency exposure.",
    "Supply chain disruption risks mitigated through inventory buildup.",
    "Key person insurance maintained at 15M USD aggregate.",
    
] * 2  # Double the dataset to reach 150+ records

# ─────────────────────────────────────────────
# KG Triples: (subject, predicate, object) - 150+ relationships
# ─────────────────────────────────────────────
TRIPLES = [
    # Firm_A relationships
    ("Firm_A",          "reported",     "Revenue_A_Y1"),
    ("Firm_A",          "reported",     "Profit_A_Y1"),
    ("Firm_A",          "acquired",     "Firm_B"),
    ("Firm_A",          "has_metric",   "PE_Ratio_A"),
    ("Firm_A",          "holds",        "Equity_X"),
    ("Firm_A",          "issued",       "Bond_A"),
    ("Firm_A",          "has_assets",   "Assets_A_Y1"),
    ("Firm_A",          "has_liabilities", "Liabilities_A_Y1"),
    ("Firm_A",          "has_roe",      "ROE_A_Y1"),
    ("Firm_A",          "has_roa",      "ROA_A_Y1"),
    
    # Firm_B relationships
    ("Firm_B",          "reported",     "Revenue_B_Y1"),
    ("Firm_B",          "reported",     "Profit_B_Y1"),
    ("Firm_B",          "acquired_by",  "Firm_A"),
    ("Firm_B",          "has_metric",   "PE_Ratio_B"),
    ("Firm_B",          "issued",       "Equity_B"),
    ("Firm_B",          "has_employees", "EmployeeCount_B"),
    ("Firm_B",          "growth_rate",  "GrowthRate_B_Y1"),
    
    # Firm_C relationships
    ("Firm_C",          "reported",     "Revenue_C_Y1"),
    ("Firm_C",          "reported",     "Profit_C_Y1"),
    ("Firm_C",          "issued",       "Bond_Y"),
    ("Firm_C",          "has_margin",   "ProfitMargin_C"),
    ("Firm_C",          "has_facilities", "Facilities_C"),
    ("Firm_C",          "has_assets",   "Assets_C_Y1"),
    ("Firm_C",          "has_asset_turnover", "AssetTurnover_C"),
    
    # Firm_D relationships
    ("Firm_D",          "reported",     "Revenue_D_Y1"),
    ("Firm_D",          "reported",     "Profit_D_Y1"),
    ("Firm_D",          "acquired",     "Firm_E"),
    ("Firm_D",          "issued",       "Equity_D"),
    ("Firm_D",          "has_assets",   "Assets_D_Y1"),
    ("Firm_D",          "has_liquidity", "QuickRatio_D"),
    
    # Firm_E relationships
    ("Firm_E",          "reported",     "Revenue_E_Y1"),
    ("Firm_E",          "acquired_by",  "Firm_D"),
    ("Firm_E",          "growth_rate",  "GrowthRate_E_Y1"),
    ("Firm_E",          "has_customers", "CustomerCount_E"),
    ("Firm_E",          "has_margin",   "GrossMargin_E"),
    ("Firm_E",          "subscription_revenue", "MRR_E"),
    
    # Firm_F relationships
    ("Firm_F",          "reported",     "Revenue_F_Y1"),
    ("Firm_F",          "issued",       "Bond_F"),
    ("Firm_F",          "has_roe",      "ROE_F_Y1"),
    ("Firm_F",          "has_roa",      "ROA_F_Y1"),
    ("Firm_F",          "has_employees", "EmployeeCount_F"),
    ("Firm_F",          "has_assets",   "Assets_F_Y1"),
    ("Firm_F",          "issued",       "Equity_F"),
    ("Firm_F",          "cash_flow",    "OperatingCashFlow_F"),
    
    # Firm_G relationships
    ("Firm_G",          "reported",     "Revenue_G_Y1"),
    ("Firm_G",          "growth_rate",  "GrowthRate_G_Y1"),
    ("Firm_G",          "issued",       "Bond_G"),
    ("Firm_G",          "has_assets",   "Assets_G_Y1"),
    ("Firm_G",          "segment_A",    "RevenueSegmentA_G"),
    ("Firm_G",          "segment_B",    "RevenueSegmentB_G"),
    ("Firm_G",          "segment_C",    "RevenueSegmentC_G"),
    
    # Firm_H relationships
    ("Firm_H",          "reported",     "Revenue_H_Y1"),
    ("Firm_H",          "issued",       "Equity_H"),
    ("Firm_H",          "has_assets",   "Assets_H_Y1"),
    ("Firm_H",          "has_margin",   "GrossMargin_H"),
    ("Firm_H",          "distribution_partners", "DistributionNetwork_H"),
    
    # Firm_I relationships
    ("Firm_I",          "reported",     "Revenue_I_Y1"),
    ("Firm_I",          "issued",       "Bond_I"),
    ("Firm_I",          "has_assets",   "Assets_I_Y1"),
    ("Firm_I",          "ebitda",       "EBITDA_I"),
    ("Firm_I",          "acquired",     "CompetitorX"),
    
    # Firm_J relationships
    ("Firm_J",          "reported",     "Revenue_J_Y1"),
    ("Firm_J",          "issued",       "Equity_J"),
    ("Firm_J",          "has_assets",   "Assets_J_Y1"),
    ("Firm_J",          "profit",       "Profit_J_Y1"),
    ("Firm_J",          "coverage_ratio", "InterestCoverage_J"),
    
    # Cross-firm relationships
    ("Firm_A",          "partnership",  "Firm_F"),
    ("Firm_F",          "partnership",  "Firm_A"),
    ("Firm_C",          "supply_chain", "Firm_D"),
    ("Firm_D",          "supply_chain", "Firm_C"),
    ("Firm_B",          "joint_venture", "Firm_I"),
    ("Firm_E",          "technology_license", "Firm_H"),
    ("Firm_A",          "distribution_agreement", "Firm_G"),
    ("Firm_D",          "consortium",   "Firm_J"),
    ("Firm_H",          "reseller",     "Firm_A"),
    ("Firm_I",          "supplier",     "Firm_D"),
    
    # Financial metrics relationships
    ("PE_Ratio_A",      "indicates",    "GrowthExpectation_A"),
    ("PE_Ratio_B",      "indicates",    "GrowthExpectation_B"),
    ("Revenue_A_Y1",    "contributes_to", "Profit_A_Y1"),
    ("Revenue_F_Y1",    "indicates",    "MarketLeadership"),
    ("OperatingCashFlow_F", "supports", "Dividend_F"),
    ("Equity_X",        "listed_under", "Firm_A"),
    ("Equity_B",        "listed_under", "Firm_B"),
    ("Equity_D",        "listed_under", "Firm_D"),
    ("Equity_F",        "listed_under", "Firm_F"),
    ("Equity_H",        "listed_under", "Firm_H"),
    ("Equity_J",        "listed_under", "Firm_J"),
    ("Bond_A",          "matures_in",   "Year_5"),
    ("Bond_F",          "matures_in",   "Year_8"),
    ("Bond_Y",          "matures_in",   "Year_5"),
    ("Bond_G",          "matures_in",   "Year_6"),
    ("Bond_I",          "matures_in",   "Year_7"),
    ("Diversification", "affects",      "Risk_Level"),
    
    # Event relationships
    ("Acquisition_AB",  "involves",     "Firm_A"),
    ("Acquisition_AB",  "involves",     "Firm_B"),
    ("Acquisition_DE",  "involves",     "Firm_D"),
    ("Acquisition_DE",  "involves",     "Firm_E"),
    ("Acquisition_FIZ", "involves",     "Firm_F"),
    ("M&A_Wave",        "involved",     "Firm_F"),
    ("M&A_Wave",        "involved",     "Firm_J"),
    
    # Market & Sector relationships
    ("Sector_Average_PE", "reference",  "PE_Ratio_F"),
    ("Dividend_Yield",  "sector_average", "DividendYield_A"),
    ("GrowthRate_B_Y1", "outperforms", "SectorAverage_Growth"),
    ("ROE_F_Y1",        "leadership",   "Sector_ROE"),
    ("Debt_to_Equity",  "varies_across", "Firm_A"),
    ("Debt_to_Equity",  "varies_across", "Firm_C"),
]

# ─────────────────────────────────────────────
# Entity Attributes: {entity: {type, value, unit, year, description}}
# 150+ entities across 10 firms with comprehensive financial metrics
# ─────────────────────────────────────────────
ENTITY_ATTRIBUTES = {
    # === FIRMS ===
    "Firm_A": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Mid-cap industrial firm, primary acquiring entity in Year 1",
    },
    "Firm_B": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "High-growth tech firm acquired by Firm_A for 45M USD",
    },
    "Firm_C": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Manufacturing firm with global supply chain and 12 facilities",
    },
    "Firm_D": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Diversified conglomerate, acquirer of Firm_E",
    },
    "Firm_E": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "SaaS/software startup acquired by Firm_D for 35M USD",
    },
    "Firm_F": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Sector leader with 200M USD revenue and strong financial position",
    },
    "Firm_G": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Multi-segment firm with emerging market exposure",
    },
    "Firm_H": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Established firm with 50+ distribution partners",
    },
    "Firm_I": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Product-focused firm with strong component supply relationships",
    },
    "Firm_J": {
        "entity_type": "Firm",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Mid-cap growth firm with strong credit rating",
    },
    
    # === FIRM_A METRICS ===
    "Revenue_A_Y1": {
        "entity_type": "Metric",
        "value": 120,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_A annual revenue for Year 1",
    },
    "Profit_A_Y1": {
        "entity_type": "Metric",
        "value": 30,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_A net profit for Year 1",
    },
    "Assets_A_Y1": {
        "entity_type": "Metric",
        "value": 450,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_A total assets in Year 1",
    },
    "Liabilities_A_Y1": {
        "entity_type": "Metric",
        "value": 150,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_A total liabilities in Year 1",
    },
    "PE_Ratio_A": {
        "entity_type": "Metric",
        "value": 18,
        "unit": "x",
        "year": 2024,
        "description": "Firm_A price-to-earnings ratio",
    },
    "ROE_A_Y1": {
        "entity_type": "Metric",
        "value": 25,
        "unit": "%",
        "year": 2024,
        "description": "Firm_A return on equity",
    },
    "ROA_A_Y1": {
        "entity_type": "Metric",
        "value": 12,
        "unit": "%",
        "year": 2024,
        "description": "Firm_A return on assets",
    },
    
    # === FIRM_B METRICS ===
    "Revenue_B_Y1": {
        "entity_type": "Metric",
        "value": 95,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_B annual revenue for Year 1",
    },
    "Profit_B_Y1": {
        "entity_type": "Metric",
        "value": 22,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_B net profit for Year 1",
    },
    "PE_Ratio_B": {
        "entity_type": "Metric",
        "value": 28,
        "unit": "x",
        "year": 2024,
        "description": "Firm_B price-to-earnings ratio indicating strong growth expectations",
    },
    "GrowthRate_B_Y1": {
        "entity_type": "Metric",
        "value": 32,
        "unit": "%",
        "year": 2024,
        "description": "Firm_B year-over-year growth rate",
    },
    "EmployeeCount_B": {
        "entity_type": "Metric",
        "value": 200,
        "unit": "headcount",
        "year": 2024,
        "description": "Firm_B total employees",
    },
    "EBITDAMargin_B": {
        "entity_type": "Metric",
        "value": 28,
        "unit": "%",
        "year": 2024,
        "description": "Firm_B EBITDA margin",
    },
    
    # === FIRM_C METRICS ===
    "Revenue_C_Y1": {
        "entity_type": "Metric",
        "value": 80,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_C annual revenue for Year 1",
    },
    "Profit_C_Y1": {
        "entity_type": "Metric",
        "value": 12,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_C net profit for Year 1",
    },
    "ProfitMargin_C": {
        "entity_type": "Metric",
        "value": 15,
        "unit": "%",
        "year": 2024,
        "description": "Firm_C net profit margin",
    },
    "Assets_C_Y1": {
        "entity_type": "Metric",
        "value": 280,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_C total assets",
    },
    "Facilities_C": {
        "entity_type": "Metric",
        "value": 12,
        "unit": "count",
        "year": 2024,
        "description": "Firm_C manufacturing facilities globally",
    },
    "AssetTurnover_C": {
        "entity_type": "Metric",
        "value": 1.8,
        "unit": "x",
        "year": 2024,
        "description": "Firm_C asset turnover ratio",
    },
    
    # === FIRM_D METRICS ===
    "Revenue_D_Y1": {
        "entity_type": "Metric",
        "value": 150,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_D annual revenue for Year 1",
    },
    "Profit_D_Y1": {
        "entity_type": "Metric",
        "value": 25,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_D net profit for Year 1",
    },
    "Assets_D_Y1": {
        "entity_type": "Metric",
        "value": 250,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_D total assets",
    },
    "QuickRatio_D": {
        "entity_type": "Metric",
        "value": 1.5,
        "unit": "ratio",
        "year": 2024,
        "description": "Firm_D quick ratio for liquidity",
    },
    "GrowthRate_D_Y1": {
        "entity_type": "Metric",
        "value": 12,
        "unit": "%",
        "year": 2024,
        "description": "Firm_D year-over-year growth rate",
    },
    
    # === FIRM_E METRICS ===
    "Revenue_E_Y1": {
        "entity_type": "Metric",
        "value": 35,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_E pre-acquisition annual revenue",
    },
    "GrowthRate_E_Y1": {
        "entity_type": "Metric",
        "value": 28,
        "unit": "%",
        "year": 2024,
        "description": "Firm_E year-over-year growth rate pre-acquisition",
    },
    "CustomerCount_E": {
        "entity_type": "Metric",
        "value": 150,
        "unit": "count",
        "year": 2024,
        "description": "Firm_E SaaS customers",
    },
    "MRR_E": {
        "entity_type": "Metric",
        "value": 2.8,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_E monthly recurring revenue",
    },
    "GrossMargin_E": {
        "entity_type": "Metric",
        "value": 72,
        "unit": "%",
        "year": 2024,
        "description": "Firm_E gross margin typical for software",
    },
    
    # === FIRM_F METRICS ===
    "Revenue_F_Y1": {
        "entity_type": "Metric",
        "value": 200,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_F annual revenue - sector leader",
    },
    "Assets_F_Y1": {
        "entity_type": "Metric",
        "value": 600,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_F total assets",
    },
    "ROE_F_Y1": {
        "entity_type": "Metric",
        "value": 32,
        "unit": "%",
        "year": 2024,
        "description": "Firm_F return on equity - industry leading",
    },
    "ROA_F_Y1": {
        "entity_type": "Metric",
        "value": 18,
        "unit": "%",
        "year": 2024,
        "description": "Firm_F return on assets",
    },
    "EmployeeCount_F": {
        "entity_type": "Metric",
        "value": 1200,
        "unit": "headcount",
        "year": 2024,
        "description": "Firm_F total employees globally",
    },
    "OperatingCashFlow_F": {
        "entity_type": "Metric",
        "value": 65,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_F operating cash flow",
    },
    
    # === FIRM_G METRICS ===
    "Revenue_G_Y1": {
        "entity_type": "Metric",
        "value": 110,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_G annual revenue",
    },
    "GrowthRate_G_Y1": {
        "entity_type": "Metric",
        "value": 8,
        "unit": "%",
        "year": 2024,
        "description": "Firm_G steady growth rate",
    },
    "Assets_G_Y1": {
        "entity_type": "Metric",
        "value": 300,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_G total assets",
    },
    "RevenueSegmentA_G": {
        "entity_type": "Metric",
        "value": 50,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_G segment A revenue",
    },
    "RevenueSegmentB_G": {
        "entity_type": "Metric",
        "value": 35,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_G segment B revenue",
    },
    "RevenueSegmentC_G": {
        "entity_type": "Metric",
        "value": 25,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_G segment C revenue",
    },
    
    # === FIRM_H METRICS ===
    "Revenue_H_Y1": {
        "entity_type": "Metric",
        "value": 90,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_H annual revenue",
    },
    "Assets_H_Y1": {
        "entity_type": "Metric",
        "value": 180,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_H total assets",
    },
    "GrossMargin_H": {
        "entity_type": "Metric",
        "value": 42,
        "unit": "%",
        "year": 2024,
        "description": "Firm_H gross margin with 2% improvement",
    },
    "DistributionNetwork_H": {
        "entity_type": "Metric",
        "value": 50,
        "unit": "count",
        "year": 2024,
        "description": "Firm_H distribution partners",
    },
    "GrowthRate_H_Y1": {
        "entity_type": "Metric",
        "value": 6,
        "unit": "%",
        "year": 2024,
        "description": "Firm_H year-over-year growth rate",
    },
    
    # === FIRM_I METRICS ===
    "Revenue_I_Y1": {
        "entity_type": "Metric",
        "value": 85,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_I annual revenue",
    },
    "Assets_I_Y1": {
        "entity_type": "Metric",
        "value": 200,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_I total assets",
    },
    "EBITDA_I": {
        "entity_type": "Metric",
        "value": 15,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_I EBITDA",
    },
    "EBITDAMargin_I": {
        "entity_type": "Metric",
        "value": 17.6,
        "unit": "%",
        "year": 2024,
        "description": "Firm_I EBITDA margin",
    },
    "InventoryTurnover_I": {
        "entity_type": "Metric",
        "value": 4.2,
        "unit": "x",
        "year": 2024,
        "description": "Firm_I inventory turnover ratio",
    },
    
    # === FIRM_J METRICS ===
    "Revenue_J_Y1": {
        "entity_type": "Metric",
        "value": 105,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_J annual revenue",
    },
    "Profit_J_Y1": {
        "entity_type": "Metric",
        "value": 18,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_J net profit",
    },
    "Assets_J_Y1": {
        "entity_type": "Metric",
        "value": 280,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_J total assets",
    },
    "GrowthRate_J_Y1": {
        "entity_type": "Metric",
        "value": 10,
        "unit": "%",
        "year": 2024,
        "description": "Firm_J growth rate",
    },
    "InterestCoverage_J": {
        "entity_type": "Metric",
        "value": 8.2,
        "unit": "x",
        "year": 2024,
        "description": "Firm_J interest coverage ratio",
    },
    
    # === BONDS ===
    "Bond_A": {
        "entity_type": "Instrument",
        "value": 80,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_A issued bond with 5.5% coupon",
    },
    "Bond_F": {
        "entity_type": "Instrument",
        "value": 120,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_F issued bond with 4.8% coupon",
    },
    "Bond_Y": {
        "entity_type": "Instrument",
        "value": 6,
        "unit": "% coupon",
        "year": 2024,
        "description": "Firm_C issued bond maturing Year 5",
    },
    "Bond_G": {
        "entity_type": "Instrument",
        "value": 4.5,
        "unit": "% coupon",
        "year": 2024,
        "description": "Firm_G convertible bond",
    },
    "Bond_I": {
        "entity_type": "Instrument",
        "value": 5.2,
        "unit": "% coupon",
        "year": 2024,
        "description": "Firm_I issued bond maturing Year 7",
    },
    
    # === EQUITIES ===
    "Equity_X": {
        "entity_type": "Instrument",
        "value": 500,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_A primary listed equity with market cap",
    },
    "Equity_B": {
        "entity_type": "Instrument",
        "value": 45,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_B equity with 3M shares outstanding",
    },
    "Equity_D": {
        "entity_type": "Instrument",
        "value": 100,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_D equity with 5M shares",
    },
    "Equity_F": {
        "entity_type": "Instrument",
        "value": 1200,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_F equity valuation",
    },
    "Equity_H": {
        "entity_type": "Instrument",
        "value": 60,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_H equity with 2M shares",
    },
    "Equity_J": {
        "entity_type": "Instrument",
        "value": 42,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_J equity with 1.5M shares",
    },
    
    # === EVENTS ===
    "Acquisition_AB": {
        "entity_type": "Event",
        "value": 45,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_A acquisition of Firm_B",
    },
    "Acquisition_DE": {
        "entity_type": "Event",
        "value": 35,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_D acquisition of Firm_E",
    },
    "Acquisition_FIZ": {
        "entity_type": "Event",
        "value": 80,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_F multi-acquisition of three companies",
    },
    "M&A_Wave": {
        "entity_type": "Event",
        "value": 200,
        "unit": "M USD",
        "year": 2024,
        "description": "Sector-wide M&A activity in Year 1",
    },
    
    # === REFERENCE METRICS ===
    "Sector_Average_PE": {
        "entity_type": "Metric",
        "value": 18,
        "unit": "x",
        "year": 2024,
        "description": "Sector average PE ratio",
    },
    "SectorAverage_Growth": {
        "entity_type": "Metric",
        "value": 10,
        "unit": "%",
        "year": 2024,
        "description": "Sector average growth rate",
    },
    "Sector_ROE": {
        "entity_type": "Metric",
        "value": 20,
        "unit": "%",
        "year": 2024,
        "description": "Sector average return on equity",
    },
    "DividendYield_A": {
        "entity_type": "Metric",
        "value": 3.2,
        "unit": "%",
        "year": 2024,
        "description": "Firm_A dividend yield above sector average",
    },
    
    # === YEARS ===
    "Year_5": {
        "entity_type": "Event",
        "value": 5,
        "unit": "year",
        "year": 2029,
        "description": "Maturity year for multiple bonds",
    },
    "Year_6": {
        "entity_type": "Event",
        "value": 6,
        "unit": "year",
        "year": 2030,
        "description": "Maturity year for Firm_G bond",
    },
    "Year_7": {
        "entity_type": "Event",
        "value": 7,
        "unit": "year",
        "year": 2031,
        "description": "Maturity year for Firm_I bond",
    },
    "Year_8": {
        "entity_type": "Event",
        "value": 8,
        "unit": "year",
        "year": 2032,
        "description": "Maturity year for Firm_F bond",
    },
    
    # === QUALITATIVE FACTORS ===
    "GrowthExpectation_A": {
        "entity_type": "Metric",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Firm_A positive growth outlook based on PE ratio",
    },
    "GrowthExpectation_B": {
        "entity_type": "Metric",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Firm_B strong growth expectation - high PE ratio",
    },
    "MarketLeadership": {
        "entity_type": "Metric",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Firm_F market leadership position",
    },
    "Risk_Level": {
        "entity_type": "Metric",
        "value": None,
        "unit": None,
        "year": 2024,
        "description": "Portfolio risk mitigated through diversification",
    },
    "Dividend_F": {
        "entity_type": "Metric",
        "value": 18,
        "unit": "M USD",
        "year": 2024,
        "description": "Firm_F combined special and regular dividend",
    },
}

# ─────────────────────────────────────────────
# Ontology: allowed entity types and relationships
# ─────────────────────────────────────────────
ONTOLOGY = {
    "entity_types": [
        "Firm", "Metric", "Instrument", "Event", 
        "Bond", "Equity", "Segment", "Partnership"
    ],
    "relationship_types": [
        "reported", "acquired", "acquired_by", "has_metric", "indicates", 
        "affects", "holds", "issued", "listed_under", "matures_in", 
        "involves", "disclosed_by", "partnership", "supply_chain", 
        "joint_venture", "technology_license", "distribution_agreement", 
        "consortium", "reseller", "supplier", "contributes_to",
        "growth_rate", "has_employees", "has_assets", "has_liabilities",
        "has_roe", "has_roa", "has_margin", "has_facilities", 
        "has_liquidity", "has_asset_turnover", "has_customers", 
        "subscription_revenue", "cash_flow", "segment_A", "segment_B", 
        "segment_C", "ebitda", "coverage_ratio", "distribution_partners",
        "sector_average", "outperforms", "varies_across", "reference", 
        "involved", "leadership"
    ],
}
