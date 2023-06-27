import math
import argparse


def is_int_or_float(user_input):
    try:
        int(user_input)
        return True
    except ValueError:
        try:
            float(user_input)
            return True
        except ValueError:
            print("Incorrect parameters: non-numerical input")
            quit()


def quit_if_negative_value(user_input):
    if user_input < 0:
        print("Incorrect parameters: negative value")
        quit()


def quit_if_negative_or_zero(user_input):
    if user_input <= 0:
        print("Incorrect parameters: negative or zero value")
        quit()


def calculate_differentiated_payments(principal, interest, number_of_payments):
    p = principal
    i = interest
    n = number_of_payments
    current_month = 1
    list_of_payments = []
    for month in range(n):
        differentiated_payment = p / n + i * (p - p * (current_month - 1) / n)
        list_of_payments.append(math.ceil(differentiated_payment))
        current_month += 1
    return list_of_payments


def calculate_annuity_payment(P, i, n):
    return P * (i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1)


def calculate_principal(A, i, n):
    return A / ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1))


def calculate_number_of_periods(P, A, i):
    if A / (A - i * P) > 0:
        return math.ceil(math.log(A / (A - i * P), 1 + i))
    else:
        raise ValueError("Can not calculate number of periods with these values "
                         "(negative input value for math.log)")


def print_number_of_periods(n):
    years = n // 12
    months = n - years * 12
    if years < 1:
        if months == 1:
            print(f"It will take {months} month to repay this loan!")
        else:
            print(f"It will take {months} months to repay this loan!")
    elif years == 1:
        if months < 1:
            print(f"It will take {years} year to repay this loan!")
        elif months == 1:
            print(f"It will take {years} year and {months} month to repay this loan!")
        else:
            print(f"It will take {years} year and {months} months to repay this loan!")
    else:
        if months < 1:
            print(f"It will take {years} years to repay this loan!")
        elif months == 1:
            print(f"It will take {years} years and {months} month to repay this loan!")
        else:
            print(f"It will take {years} years and {months} months to repay this loan!")


parser = argparse.ArgumentParser(description="""This program is a loan calculator, 
handling both annuity- and differentiated payments.""")

parser.add_argument("--type", choices=["annuity", "diff"],
                    help="Choose if the loan is annuity or differentiated,"
                         "input required.")
parser.add_argument("--payment", help="Input the monthly payment amount.")
parser.add_argument("--principal", help="Input the principal value.")
parser.add_argument("--periods", help="Input the number of months needed to repay the loan.")
parser.add_argument("--interest", help="Input the interest rate of your loan.")

args = parser.parse_args()
null_counter = 0
loan_type = args.type

# store and check input
payment = args.payment
if payment is None:
    null_counter += 1
elif is_int_or_float(payment):
    payment = float(payment)
    quit_if_negative_or_zero(payment)

principal = args.principal
if principal is None:
    null_counter += 1
elif is_int_or_float(principal):
    principal = float(principal)
    quit_if_negative_or_zero(principal)

periods = args.periods
if periods is None:
    null_counter += 1
elif is_int_or_float(periods):
    periods = int(periods)
    quit_if_negative_or_zero(periods)

# interest = args.interest
if args.interest is None:
    print("Incorrect parameters")
    quit()
if is_int_or_float(args.interest):
    nominal_interest = float(args.interest) / (12 * 100)  # convert yearly interest rate into monthly percent value
    quit_if_negative_value(nominal_interest)
else:
    raise TypeError("Interest rate must be entered and must be of integer or decimal value.")

# check that we have the right amount of values specified
if null_counter == 0:
    print("Nothing to calculate")
    quit()
elif null_counter > 1:
    print("Too many parameters missing")
    quit()

# check which one of the values that needs to be calculated
if loan_type == "diff":  # in this case payment has to be None for the program to work
    if payment:
        print('When --type is set to "diff", the program can only calculate the monthly payment. '
              'Please do not input --payment.')
        quit()
    else:
        payments = calculate_differentiated_payments(principal, nominal_interest, periods)
        for month in range(len(payments)):
            print(f"Month {month + 1}: payment is {payments[month]}")
        print()
        print(f"Overpayment = {int(sum(payments) - principal)}")
elif payment is None:  # !!!change annuity_payment to "payment"?
    annuity_payment = math.ceil(calculate_annuity_payment(principal, nominal_interest, periods))
    print(f"Your annuity payment = {annuity_payment}!")
    print(f"Overpayment = {int(annuity_payment * periods - principal)}")
elif principal is None:
    principal = int(calculate_principal(payment, nominal_interest, periods))
    print(f"Your loan principal = {principal}!")
    print(f"Overpayment = {math.ceil(payment * periods - principal)}")
elif periods is None:
    periods = calculate_number_of_periods(principal, payment, nominal_interest)
    print_number_of_periods(periods)
    print(f"Overpayment = {math.ceil(payment * periods - principal)}")
