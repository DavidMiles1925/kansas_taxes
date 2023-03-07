import constants

# --- Input and Validation ---
is_int = False
is_number = False

print("Income and withholdings for 2023 in Kansas")
print('')
print('1) Single  2) Married  3) Head of Household')
status_input = input('Enter your filing Status: ')

while is_int == False:
    try:
        status_input = int(status_input)
        if status_input < 1 or status_input > 3:
            print('')
            print('Enter a number 1-3')
            status_input = input('Enter your filing Status: ')
        else:
            is_int = True
            continue
    except:
        print('')
        print('Invalid input')
        status_input = input('Enter your filing Status: ')

income = input('Enter your gross income: ')

while is_number == False:
    try:
        income = float(income)
        is_number = True
    except:
        print('')
        print('Invalid input, please enter a number')
        income = input('Enter your gross income: ')

# --- Status Logic --- #
if (status_input == 1):
    fed_cap = constants.fed_single_caps
    kansas_cap = constants.kansas_single_caps
elif (status_input == 2):
    fed_cap = constants.fed_married_caps
    kansas_cap = constants.kansas_married_caps
elif (status_input == 3):
    fed_cap = constants.fed_hoh_caps
    kansas_cap = constants.kansas_hoh_caps

# --- Federal Tax Calculation --- #
fed_taxes_paid = 0
left_to_tax = income

for x in range(len(fed_cap)):
    if fed_cap[x] < left_to_tax:
        fed_taxes_paid = fed_taxes_paid + \
            (constants.fed_tax_rates[x] * fed_cap[x])
        left_to_tax = left_to_tax - fed_cap[x]
    else:
        fed_taxes_paid = fed_taxes_paid + \
            (constants.fed_tax_rates[x] * left_to_tax)
        left_to_tax = 0

# --- State Tax Calculation --- #
kansas_taxes_paid = 0
left_to_tax = income

for y in range(len(kansas_cap)):
    if kansas_cap[y] < left_to_tax:
        kansas_taxes_paid = kansas_taxes_paid + \
            (constants.kansas_tax_rates[y] * kansas_cap[y])
        left_to_tax = left_to_tax - kansas_cap[y]
    else:
        kansas_taxes_paid = kansas_taxes_paid + \
            (constants.kansas_tax_rates[y] * left_to_tax)
        left_to_tax = 0

# --- FICA Calculations --- #
social_security_paid = income * constants.social_security_rate

if social_security_paid >= constants.social_security_max:
    social_security_paid = constants.social_security_max

if income > constants.medicare_premium_wage:
    medicare_paid = round(
        income * (constants.medicare_rate + constants.medicare_premium_rate), 2)
else:
    medicare_paid = round(income * constants.medicare_rate, 2)

# --- Final Calculations --- #
fed_taxes_paid = round(fed_taxes_paid, 2)
kansas_taxes_paid = round(kansas_taxes_paid, 2)
total_taxes_paid = round((fed_taxes_paid + kansas_taxes_paid), 2)
income_after_tax = round(
    (income - total_taxes_paid - medicare_paid - social_security_paid), 2)
monthly_income = round((income_after_tax / 12), 2)
weekly_income = round((income_after_tax / 52), 2)

# --- Output --- #
print('')
print('')
print('***************** Taxes *****************')
print('')
print('Federal Taxes Paid:   ', fed_taxes_paid)
print('Kansas Taxes Paid:    ', kansas_taxes_paid)
print('')
print('***************** FICA ******************')
print('')
print('Social Security Paid: ', social_security_paid)
print('Medicare Paid:        ', medicare_paid)
print('')
print('***************** Income ****************')
print('')
print('Net Income:           ', income_after_tax)
print('')
print('Monthly Income:       ', monthly_income)
print('Weekly Income:        ', weekly_income)
print('')
print("_________________________________________")
input("Press ENTER to exit")
