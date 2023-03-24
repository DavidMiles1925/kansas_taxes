import os
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
            print('Invalid input, enter a number 1-3')
            status_input = input('Enter your filing Status: ')
        else:
            is_int = True
            continue
    except:
        print('')
        print('Invalid input, enter a number 1-3')
        status_input = input('Enter your filing Status: ')

income = input('Enter your gross income: $')

while is_number == False:
    try:
        income = float(income)
        is_number = True
    except:
        print('')
        print('Invalid input, please enter a number')
        income = input('Enter your gross income: $')

# --- Status Logic --- #
if (status_input == 1):
    fed_cap = constants.fed_single_caps
    kansas_cap = constants.kansas_single_caps
    filing_status = 'Single'
elif (status_input == 2):
    fed_cap = constants.fed_married_caps
    kansas_cap = constants.kansas_married_caps
    filing_status = 'Married'
elif (status_input == 3):
    fed_cap = constants.fed_hoh_caps
    kansas_cap = constants.kansas_hoh_caps
    filing_status = 'Head of Household'

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
monthly_income = round((income_after_tax / constants.months_in_year), 2)
weekly_income = round((income_after_tax / constants.weeks_in_year), 2)

# --- Output to Console --- #
print('')
print('')
print('***************** Taxes *****************')
print('')
print('Federal Taxes Paid:   $', fed_taxes_paid)
print('Kansas Taxes Paid:    $', kansas_taxes_paid)
print('')
print('***************** FICA ******************')
print('')
print('Social Security Paid: $', social_security_paid)
print('Medicare Paid:        $', medicare_paid)
print('')
print('***************** Income ****************')
print('')
print('Net Income:           $', income_after_tax)
print('')
print('Monthly Income:       $', monthly_income)
print('Weekly Income:        $', weekly_income)
print('')
print("_________________________________________")
print('Written by David Miles')
print('')

# --- Output to File --- #
write_to_file = input('Write output to file? (y/n)')

if write_to_file == 'y' or write_to_file == 'Y':
    print('')
    fname = input('Enter file name: ')

    count = len(fname)

    if fname[(count-4):count] != '.txt':
        fname = fname + '.txt'

    if os.path.exists(fname):
        fout = open(fname, 'a')
    else:
        fout = open(fname, 'w')

    fout.write('***************** Income ****************' + '\n\n')
    fout.write('Income:          $' + str(income) + '\n')
    fout.write('Filing Status:    ' + filing_status + '\n\n')
    fout.write('***************** Taxes *****************' + '\n\n')
    fout.write('Federal Taxes Paid:   $' + str(fed_taxes_paid) + '\n')
    fout.write('Kansas Taxes Paid:    $' + str(kansas_taxes_paid) + '\n\n')
    fout.write('***************** FICA ******************' + '\n\n')
    fout.write('Social Security Paid: $' + str(social_security_paid) + '\n')
    fout.write('Medicare Paid:        $' + str(medicare_paid) + '\n\n')
    fout.write('***************** Income ****************' + '\n\n')
    fout.write('Net Income:           $' + str(income_after_tax) + '\n\n')
    fout.write('Monthly Income:       $' + str(monthly_income) + '\n')
    fout.write('Weekly Income:        $' + str(weekly_income) + '\n\n')
    fout.write('_________________________________________\n')
    fout.write('Written by David Miles\n\n')
    fout.close()

print('')
input("Press ENTER to exit")
exit()
