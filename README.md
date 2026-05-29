# private-banking-credit-facility-engine
HNW client credit facility eligibility system using Alteryx, Python and Tableau
# Private Banking Credit Facility Eligibility Engine

An end-to-end HNW client credit facility assessment system 
built using Alteryx, Python, and Tableau.

## What it does
- Ingests 50 simulated High Net Worth client records
- Alteryx validates data and calculates key financial ratios
- Python scores each client using a 5-factor risk model
- Recommends facility type (Lombard Loan / Mortgage / Overdraft)
- Tableau dashboard visualises portfolio exposure and risk distribution

## Key Results
- Total clients assessed: 50
- Lombard Loans: 42 | Mortgage: 3 | Overdraft: 5
- LOW risk: 23 | MEDIUM: 24 | HIGH: 3
- Average recommended facility: £4,891,550
- Total portfolio exposure: £244,577,505

## Risk Scoring Model (100 points)
| Factor | Max Points |
|---|---|
| Liability Ratio | 40 |
| Liquidity Ratio | 25 |
| Credit History | 20 |
| Years as Client | 10 |
| Risk Appetite | 5 |

## Facility Types
| Type | Criteria | Size |
|---|---|---|
| Lombard Loan | Portfolio ≥ £1M + no defaults | 70% of portfolio |
| Mortgage Facility | Property ≥ £500k | 75% of property value |
| Overdraft Facility | Liquid assets ≥ £200k | 30% of liquid assets |

## Tool Stack
- Alteryx Designer — data validation and ratio calculation
- Python (pandas) — risk scoring and facility recommendation
- Tableau Public — interactive portfolio dashboard
- Excel — client data and output reports

## Dashboard
![Dashboard](dashboard.png)

## Live Dashboard
[View on Tableau Public](YOUR_TABLEAU_PUBLIC_LINK_HERE)
