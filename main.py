import os
import constants


def main():
    displayWelcome()

    filing_status = getFilingStatus()
    gross_income = getDollarAmount('Enter your gross income')

    # Adding tax credit feature
    tax_credits = getDollarAmount('Tax Credit Amount?')

    taxes = calculateTaxes(gross_income, filing_status, tax_credits)
    income = calculateIncome(gross_income, taxes)

    outputToConsole(taxes, income)
    outputToFile(taxes, income, gross_income,
                 filing_status['text'], tax_credits)


def getDollarAmount(prompt):
    number = input(prompt + ': $')

    is_number = False
    while is_number == False:
        try:
            number = float(number)
            is_number = True
        except:
            print('')
            print('Invalid input, please enter a number')
            number = input('${prompt}: $')
    return number


def displayWelcome():
    print("Income and withholdings for 2023 in Kansas")
    print('')


def getFilingStatus():
    is_int = False
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

    if (status_input == 1):
        fed_cap = constants.fed_single_caps
        kansas_cap = constants.kansas_single_caps
        filing_status_text = 'Single'
    elif (status_input == 2):
        fed_cap = constants.fed_married_caps
        kansas_cap = constants.kansas_married_caps
        filing_status_text = 'Married'
    elif (status_input == 3):
        fed_cap = constants.fed_hoh_caps
        kansas_cap = constants.kansas_hoh_caps
        filing_status_text = 'Head of Household'

    status_dictionary = {'status': status_input, 'fed_cap': fed_cap,
                         'state_cap': kansas_cap, 'text': filing_status_text}

    return status_dictionary


def calculateIncome(gross_income, taxes):
    income_after_tax = gross_income - \
        taxes['fed_taxes_paid'] - taxes['kansas_taxes_paid'] - \
        taxes['social_security_paid'] - taxes['medicare_paid']

    monthly_income = round((income_after_tax / constants.months_in_year), 2)
    weekly_income = round((income_after_tax / constants.weeks_in_year), 2)

    return {'income_after_tax': income_after_tax, 'monthly_income': monthly_income, 'weekly_income': weekly_income}


def calculateTaxes(gross_income, filing_status, tax_credits):
    fed_taxes_paid = calculateFederalTaxes(
        gross_income, filing_status['fed_cap'], tax_credits)

    kansas_taxes_paid = calculateStateTaxes(
        gross_income, filing_status['state_cap'])

    social_security_paid = calculateSocialSecurity(gross_income)
    medicare_paid = calculateMedicare(gross_income)

    return {'fed_taxes_paid': fed_taxes_paid, 'kansas_taxes_paid': kansas_taxes_paid, 'social_security_paid': social_security_paid, 'medicare_paid': medicare_paid}


def calculateFederalTaxes(gross_income, fed_cap, tax_credits):
    fed_taxes_paid = 0
    left_to_tax = gross_income

    for x in range(len(fed_cap)):
        if fed_cap[x] < left_to_tax:
            fed_taxes_paid = fed_taxes_paid + \
                (constants.fed_tax_rates[x] * fed_cap[x])
            left_to_tax = left_to_tax - fed_cap[x]
        else:
            fed_taxes_paid = fed_taxes_paid + \
                (constants.fed_tax_rates[x] * left_to_tax)
            left_to_tax = 0

    fed_taxes_paid = fed_taxes_paid - tax_credits

    return round(fed_taxes_paid, 2)


def calculateStateTaxes(gross_income, kansas_cap):
    kansas_taxes_paid = 0
    left_to_tax = gross_income

    for y in range(len(kansas_cap)):
        if kansas_cap[y] < left_to_tax:
            kansas_taxes_paid = kansas_taxes_paid + \
                (constants.kansas_tax_rates[y] * kansas_cap[y])
            left_to_tax = left_to_tax - kansas_cap[y]
        else:
            kansas_taxes_paid = kansas_taxes_paid + \
                (constants.kansas_tax_rates[y] * left_to_tax)
            left_to_tax = 0

    return round(kansas_taxes_paid, 2)


def calculateMedicare(gross_income):
    if gross_income > constants.medicare_premium_wage:
        medicare_paid = gross_income * \
            (constants.medicare_rate + constants.medicare_premium_rate)
    else:
        medicare_paid = gross_income * constants.medicare_rate

    return round(medicare_paid, 2)


def calculateSocialSecurity(gross_income):
    social_security_paid = gross_income * constants.social_security_rate

    if social_security_paid >= constants.social_security_max:
        social_security_paid = constants.social_security_max

    return round(social_security_paid, 2)


def outputToConsole(taxes, income):
    print('')
    print('')
    print('***************** Taxes *****************')
    print('')
    print('Federal Taxes Paid:   $', taxes['fed_taxes_paid'])
    print('Kansas Taxes Paid:    $', taxes['kansas_taxes_paid'])
    print('')
    print('***************** FICA ******************')
    print('')
    print('Social Security Paid: $', taxes['social_security_paid'])
    print('Medicare Paid:        $', taxes['medicare_paid'])
    print('')
    print('***************** Income ****************')
    print('')
    print('Net Income:           $', income['income_after_tax'])
    print('')
    print('Monthly Income:       $', income['monthly_income'])
    print('Weekly Income:        $', income['weekly_income'])
    print('')
    print("_________________________________________")
    print('Written by David Miles')
    print('')


def outputToFile(taxes, income, gross_income, filing_status_text, tax_credits):
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
        fout.write('Income:          $' + str(gross_income) + '\n')
        fout.write('Tax Credits:     $' + str(tax_credits) + '\n')
        fout.write('Filing Status:    ' + filing_status_text + '\n\n')
        fout.write('***************** Taxes *****************' + '\n\n')
        fout.write('Federal Taxes Paid:   $' +
                   str(taxes['fed_taxes_paid']) + '\n')
        fout.write('Kansas Taxes Paid:    $' +
                   str(taxes['kansas_taxes_paid']) + '\n\n')
        fout.write('***************** FICA ******************' + '\n\n')
        fout.write('Social Security Paid: $' +
                   str(taxes['social_security_paid']) + '\n')
        fout.write('Medicare Paid:        $' +
                   str(taxes['medicare_paid']) + '\n\n')
        fout.write('***************** Income ****************' + '\n\n')
        fout.write('Net Income:           $' +
                   str(income['income_after_tax']) + '\n\n')
        fout.write('Monthly Income:       $' +
                   str(income['monthly_income']) + '\n')
        fout.write('Weekly Income:        $' +
                   str(income['weekly_income']) + '\n\n')
        fout.write('_________________________________________\n')
        fout.write('Written by David Miles\n\n')
        fout.close()
        print('File Written: ' + str(os.getcwd()) + '\\' + fname)
    else:
        print('No file was written')


if __name__ == "__main__":
    main()
    print('')
    input("Press ENTER to exit")
    exit()
