# if applicant has high income AND good credit, then the applicant is Eligible for a loan

# 'and' Operator (All Conditions must be true)

has_high_income = True
has_good_credit = False

if has_high_income and has_good_credit:
    print("Eligible for loan")
else:
    print("Not Eligible for loan")


# 'or' Operator (At least condition is true)
if has_high_income or has_good_credit:
    print("Applicant either has good credit OR high income")

# 'not' Operator (Reverses the boolean)
has_good_credit = True
has_criminal_record = True

if has_good_credit and not has_criminal_record:
    print("Eligible for loan and no criminal record")
else:
    print("Not eligible for loan, applicant has a criminal record or bad credit")
