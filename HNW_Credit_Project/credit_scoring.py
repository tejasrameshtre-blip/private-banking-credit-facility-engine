import pandas as pd

# Load data — use whichever file you have
try:
    df = pd.read_csv('HNW_Scored.csv')
    print("Loaded HNW_Scored.csv from Alteryx")
except:
    df = pd.read_csv('HNW_Clients.csv')
    print("Loaded HNW_Clients.csv directly")

# Calculate ratios if not already present
if 'Liability_Ratio' not in df.columns:
    df['Liability_Ratio'] = df['Existing_Liabilities_GBP'] / df['Net_Worth_GBP']
if 'Liquidity_Ratio' not in df.columns:
    df['Liquidity_Ratio'] = df['Liquid_Assets_GBP'] / df['Net_Worth_GBP']

# Assign facility type if not already present
if 'Facility_Type' not in df.columns:
    def assign_facility(row):
        if row['Investment_Portfolio_GBP'] >= 1000000 and row['Credit_History'] != 'Poor':
            return 'Lombard Loan'
        elif row['Property_Value_GBP'] >= 500000:
            return 'Mortgage Facility'
        elif row['Liquid_Assets_GBP'] >= 200000:
            return 'Overdraft Facility'
        else:
            return 'Under Review'
    df['Facility_Type'] = df.apply(assign_facility, axis=1)

# Assign recommended facility size
if 'Recommended_Facility_GBP' not in df.columns:
    def assign_facility_size(row):
        if row['Facility_Type'] == 'Lombard Loan':
            return round(row['Investment_Portfolio_GBP'] * 0.7)
        elif row['Facility_Type'] == 'Mortgage Facility':
            return round(row['Property_Value_GBP'] * 0.75)
        elif row['Facility_Type'] == 'Overdraft Facility':
            return round(row['Liquid_Assets_GBP'] * 0.3)
        else:
            return 0
    df['Recommended_Facility_GBP'] = df.apply(assign_facility_size, axis=1)

# Risk scoring function
def calculate_risk(row):
    score = 0

    # Liability ratio (40 points)
    if row['Liability_Ratio'] < 0.1:
        score += 40
    elif row['Liability_Ratio'] < 0.2:
        score += 30
    elif row['Liability_Ratio'] < 0.3:
        score += 20
    else:
        score += 10

    # Liquidity ratio (25 points)
    if row['Liquidity_Ratio'] > 0.5:
        score += 25
    elif row['Liquidity_Ratio'] > 0.3:
        score += 15
    else:
        score += 5

    # Credit history (20 points)
    if row['Credit_History'] == 'Excellent':
        score += 20
    elif row['Credit_History'] == 'Good':
        score += 12
    else:
        score += 0

    # Years as client (10 points)
    if row['Years_as_Client'] >= 10:
        score += 10
    elif row['Years_as_Client'] >= 5:
        score += 6
    else:
        score += 2

    # Risk appetite (5 points)
    if row['Risk_Appetite'] == 'Conservative':
        score += 5
    elif row['Risk_Appetite'] == 'Moderate':
        score += 3
    else:
        score += 1

    # Rating
    if score >= 75:
        rating = 'LOW'
    elif score >= 50:
        rating = 'MEDIUM'
    else:
        rating = 'HIGH'

    return pd.Series({'Risk_Score': score, 'Risk_Rating': rating})

# Apply scoring
scores = df.apply(calculate_risk, axis=1)
df = pd.concat([df, scores], axis=1)

# Approval status
def assign_approval(row):
    if row['Risk_Rating'] == 'LOW' and row['Facility_Type'] != 'Under Review':
        return 'Approved'
    elif row['Risk_Rating'] == 'MEDIUM':
        return 'Conditional'
    else:
        return 'Declined'

df['Approval_Status'] = df.apply(assign_approval, axis=1)

# Save outputs
df.to_csv('HNW_Final_Scored.csv', index=False)
df.to_excel('HNW_Final_Scored.xlsx', index=False)

# Print summary
print("\n=== PRIVATE BANKING CREDIT FACILITY ELIGIBILITY REPORT ===")
print(f"Total HNW clients assessed: {len(df)}")
print(f"\nFacility Type Distribution:")
print(df['Facility_Type'].value_counts().to_string())
print(f"\nRisk Rating Distribution:")
print(df['Risk_Rating'].value_counts().to_string())
print(f"\nApproval Status:")
print(df['Approval_Status'].value_counts().to_string())
print(f"\nAverage Risk Score: {df['Risk_Score'].mean():.1f}/100")
print(f"Average Recommended Facility: £{df['Recommended_Facility_GBP'].mean():,.0f}")
print(f"Total Portfolio Exposure: £{df['Recommended_Facility_GBP'].sum():,.0f}")
print(f"\nTop 5 clients by facility size:")
top5 = df[['Client_Name','Facility_Type','Recommended_Facility_GBP','Risk_Rating','Approval_Status']].nlargest(5,'Recommended_Facility_GBP')
print(top5.to_string(index=False))
print("\nFiles saved: HNW_Final_Scored.csv and HNW_Final_Scored.xlsx")
