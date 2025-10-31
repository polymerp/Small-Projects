"""
BankClasses program. Simulates a bank/customers/accounts/transactions/dates
"""
import doctest
import datetime
# Total: -15


class MyDate:
    """
    A date object to represent a date
    """
    def __init__(self, day, month, year):
        self._day = day # -1
        self._month = month
        self._year = year

    def __str__(self):
        return f"{self._day}/{self._month}/{self._year}"


class Transaction:
    """
    Represents a single transaction. It's called with a transaction type of
    either a deposit or a withdrawal.
    If there are insufficient funds to complete the withdrawal, the
    transaction_type is set to no transaction.
    """
    TRANSACTION_DESCRIPTIONS = ["Deposit", "Withdrawal", "No transaction"]
    DEPOSIT = 0
    WITHDRAWAL = 1
    NO_TRANSACTION = 2

    def __init__(self, amount, transaction_type, date, current_balance):

        self._amount = amount
        if transaction_type == self.DEPOSIT: # -1
            self._balance_after_transaction = current_balance + amount
        elif transaction_type == self.WITHDRAWAL and not current_balance - amount < 0:
            self._balance_after_transaction = current_balance - amount
        else:
            self._balance_after_transaction = current_balance
            transaction_type = self.NO_TRANSACTION

        self._date = date
        self._type_index = transaction_type

    # -1

    def get_amount(self):
        """Return amount in transaction"""
        return self._amount

    def get_balance_after_transaction(self):
        """Return balance after transaction"""
        return self._balance_after_transaction

    def __str__(self):  # e.g. 24/1/2021 Deposit $500 Balance: $11700 \\\\\ 25/1/2021 No Transaction Balance $12
        if self._type_index == 0:
            return f"{self._date} Deposit ${self._amount} Balance: ${self._balance_after_transaction}"
        elif self._type_index == 1:
            return f"{self._date} Withdrawal ${self._amount} Balance: ${self._balance_after_transaction}"
        else:
            return f"{self._date} No transaction Balance: ${self._balance_after_transaction}"


class Account:
    """
    A bank account. Contains a list of transactions.
    """

    ACCOUNT_TYPE = "GET_RICH_QUICK ACCOUNT"

    def __init__(self, id): # -1
        self._ACCOUNT_ID = id
        self.balance = 0
        self.is_open = True
        self.transactions = []

    def get_is_open(self):
        """Return account open status"""
        if self.is_open:
            return True
        else:
            return False

    def get_current_balance(self):
        """Return account balance"""
        return self.balance

    def set_is_open(self, set_open):
        """Open account"""
        self.is_open = set_open

    def close_account(self, date):
        """Close account and withdraw funds"""
        self.is_open = False
        transaction = Transaction(self.balance, 1, date, self.balance)
        self.transactions.append(transaction)
        self.balance = 0

    def perform_transaction(self, amount, transaction_type, date):
        """Perform a transaction on the account"""
        transaction = Transaction(amount, transaction_type, date, self.balance)
        self.transactions.append(transaction)
        if self.is_open:
            if transaction_type == 0: # -1
                self.balance += amount
                return True
            elif (transaction_type == 1) and not (self.balance - amount < 0): # -1
                self.balance -= amount
                return True
            else:
                return False
        else:
            return False

    def get_max_10_transactions(self):
        """Return last 10 transactions"""
        temp10 = ""
        n = 1
        if len(self.transactions) >= 10:
            for i in range(-10, 0):
                temp10 += f"{n} {self.transactions[i]}\n"
                n += 1
        else:
            for i in range(-len(self.transactions), 0):
                temp10 += f"{n} {self.transactions[i]}\n"
                n += 1
        if self.is_open:
            return temp10
        else:
            return f"Account closed\n{temp10}"

    def __str__(self):
        """Return account details"""
        # -1
        if self.is_open:
            return (f"{self.ACCOUNT_TYPE} [{self._ACCOUNT_ID}"
                    f"]: Balance ${self.balance}")
        elif not self.is_open:
            return (f"{self.ACCOUNT_TYPE} [{self._ACCOUNT_ID}"
                    f"]: Balance ${self.balance} Account closed")


class Customer:
    """
    Represents a customer of a bank. They only have 1 account.
    """
    def __init__(self, person_name, person_id, account_id):
        self.name = person_name
        self._customer_id = person_id
        self.account = Account(account_id)

    def get_customer_id(self):
        """Return customer ID"""
        return self._customer_id

    def get_name(self):
        """Return customer Name"""
        return self.name

    def get_account_balance(self):
        """Return customer account balance"""
        return self.account.balance

    def has_an_open_account(self):
        """Return whether account is open"""
        return self.account.get_is_open()

    def close_account(self, date):
        """Close user's account"""
        return self.account.close_account(date)

    def open_account(self, date):
        """Open user's account"""
        self.account.set_is_open(date) # -1
        self.account.perform_transaction(0, 0, date)
        pass

    def perform_transaction(self, amount, transaction_type, date):
        """Perform transaction on user's account"""
        return self.account.perform_transaction(amount, transaction_type, date)

    def get_max_10_transactions(self):
        """Return last 10 transactions from user's account"""
        return self.account.get_max_10_transactions()

    def get_account_information(self):
        """Return account information"""
        return self.account.__str__()

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Customer ID: {self._customer_id}\n"
                f"{self.account.__str__()}")


class MyBank:
    """
    Represents a bank. Contains customers.
    """
    def __init__(self, name):
        # -1
        self.name = name
        self.customers = []
        self.day = 0
        self.month = 0
        self.year = 0

    @staticmethod
    def get_mydate_object():
        """Returns current date"""
        return datetime.date.today()  # -1

    @staticmethod
    def deposit_funds(current_customer):
        """Deposits funds to customer's account"""
        if current_customer.account.is_open:
            temp_depo = input("Enter the amount to deposit:")
            current_customer.perform_transaction(
                float(temp_depo), 0, datetime.date.today()) # -1
        elif not current_customer.account.is_open:
            print("Account is closed!")

    @staticmethod
    def withdraw_funds(current_customer):
        """Withdraws funds from customer's account """
        if current_customer.account.is_open:
            temp_depo = input("Enter the amount to withdraw:")
            current_customer.perform_transaction(
                float(temp_depo), 1, datetime.date.today()) # -1 # -1
        elif not current_customer.account.is_open:
            print("Account is closed!")

    @staticmethod
    def open_account(current_customer):
        """Opens customer's account"""
        current_customer.open_account(datetime.date.today()) # -1
        return current_customer.get_account_information()

    def close_account(self, current_customer):
        """Closes customer's account"""
        current_customer.close_account(datetime.date.today()) # -1
        self.customers.remove(current_customer)
        print(current_customer.get_account_information())

    def display_bank_summary(self):
        """Return a summary of the bank; number of customers and total money held in the bank"""
        x = 0
        for i in range(0, len(self.customers)):
            x += self.customers[i].account.balance
        result = f"\n************************************************************************\n" \
                 f"TakeMyMoney has {len(self.customers)} customers\nTotal amount in customer accounts ${x}\n" \
                 f"************************************************************************\n"
        print(result)

    @staticmethod
    def display_account_information(customer):
        """Returns customer's account information"""
        return customer.__str__()

    @staticmethod
    def display_welcome():
        """Returns welcome method"""
        return "Come bank with us - by Mr. Gardiner"

    def add_customer(self, customer):
        """Add customer to bank customers"""
        return self.customers.append(customer)

    def remove_customer(self, customer):
        """Remove customer to bank customers"""
        return self.customers.remove(customer)


def test_bank():
    """
    # Mydate , Transaction , Account testing
    # ==== #
    # MyDate Class
    >>> date1 = MyDate(3, 12, 2021)
    >>> print(date1)
    3/12/2021

    >>> date2 = MyDate(23, 4, 2021)
    >>> print(date2)
    23/4/2021

    # ==== #
    # Transaction Class
    print("Preliminary testing of the Transaction class")
    >>> transaction = Transaction(100, Transaction.DEPOSIT, MyDate(3, 1, 2021),
    ... 3000)
    >>> print(transaction)
    3/1/2021 Deposit $100 Balance: $3100

    >>> transaction2 = Transaction(300, Transaction.WITHDRAWAL, MyDate(3, 1,
    ... 2021), 600)
    >>> print(transaction2)
    3/1/2021 Withdrawal $300 Balance: $300

    >>> transaction3 = Transaction(100.01, Transaction.WITHDRAWAL, MyDate(3, 1,
    ... 2021), 100)
    >>> print(transaction3)
    3/1/2021 No transaction Balance: $100

    # ==== #
    # Account Class
    print("Preliminary testing of the Account class")

    # -- 1 -- #
    >>> account = Account(1234)
    >>> account.perform_transaction(200, Transaction.DEPOSIT, MyDate(23, 4,
    ... 2021))
    True
    >>> print('1. Balance $' + str(account.get_current_balance()))
    1. Balance $200
    >>> account.perform_transaction(600, Transaction.DEPOSIT, MyDate(23, 4,
    ... 2021))
    True
    >>> print(account)
    GET_RICH_QUICK ACCOUNT [1234]: Balance $800

    # -- 2 -- #
    >>> account = Account(1234)

    # Transactions
    >>> account.perform_transaction(200, Transaction.DEPOSIT, MyDate(23, 4,
    ... 2021))
    True
    >>> account.perform_transaction(100, Transaction.WITHDRAWAL, MyDate(23, 4,
    ... 2021))
    True
    >>> account.perform_transaction(100.01, Transaction.WITHDRAWAL, MyDate(23,
    ... 4, 2021))
    False
    >>> account.perform_transaction(700, Transaction.DEPOSIT, MyDate(23, 4,
    ... 2021))
    True
    >>> account.perform_transaction(800, Transaction.WITHDRAWAL, MyDate(23, 4,
    ... 2021))
    True
    >>> print(account.get_max_10_transactions())
    1 23/4/2021 Deposit $200 Balance: $200
    2 23/4/2021 Withdrawal $100 Balance: $100
    3 23/4/2021 No transaction Balance: $100
    4 23/4/2021 Deposit $700 Balance: $800
    5 23/4/2021 Withdrawal $800 Balance: $0
    <BLANKLINE>

    # -- 3 -- #
    >>> print(account)
    GET_RICH_QUICK ACCOUNT [1234]: Balance $0

    # -- 4 -- #
    >>> account.close_account(MyDate(1, 1, 9999))
    >>> print(account)
    GET_RICH_QUICK ACCOUNT [1234]: Balance $0 Account closed

    # -- 5 -- #
    >>> account = Account(1234)
    >>> deposits = [35, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    >>> for deposit in deposits:
    ...     account.perform_transaction(deposit, Transaction.DEPOSIT,
    ... MyDate(25, 4, 2021))
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    >>> print(account.get_max_10_transactions())
    1 25/4/2021 Deposit $25 Balance: $60
    2 25/4/2021 Deposit $30 Balance: $90
    3 25/4/2021 Deposit $35 Balance: $125
    4 25/4/2021 Deposit $40 Balance: $165
    5 25/4/2021 Deposit $45 Balance: $210
    6 25/4/2021 Deposit $50 Balance: $260
    7 25/4/2021 Deposit $55 Balance: $315
    8 25/4/2021 Deposit $60 Balance: $375
    9 25/4/2021 Deposit $65 Balance: $440
    10 25/4/2021 Deposit $70 Balance: $510
    <BLANKLINE>

    # Customer class

    >>> cust = Customer("Mr. Gardiner", 1, 1000)
    >>> print(cust)
    Name: Mr. Gardiner
    Customer ID: 1
    GET_RICH_QUICK ACCOUNT [1000]: Balance $0
    >>> cust.perform_transaction(1000, Transaction.DEPOSIT, MyDate(27, 2,
    ... 2022))
    True
    >>> cust.perform_transaction(300, Transaction.WITHDRAWAL, MyDate(27, 2,
    ... 2022))
    True
    >>> cust.perform_transaction(250, Transaction.WITHDRAWAL, MyDate(28, 2,
    ... 2022))
    True
    >>> cust.perform_transaction(500, Transaction.WITHDRAWAL, MyDate(1, 3,
    ... 2022))
    False
    >>> print(cust.get_max_10_transactions())
    1 27/2/2022 Deposit $1000 Balance: $1000
    2 27/2/2022 Withdrawal $300 Balance: $700
    3 28/2/2022 Withdrawal $250 Balance: $450
    4 1/3/2022 No transaction Balance: $450
    <BLANKLINE>
    >>> cust.close_account(MyDate(2, 3, 2022))
    >>> print(cust)
    Name: Mr. Gardiner
    Customer ID: 1
    GET_RICH_QUICK ACCOUNT [1000]: Balance $0 Account closed
    >>> cust.open_account(MyDate(3, 3, 2022))
    >>> print(cust.get_max_10_transactions())
    1 27/2/2022 Deposit $1000 Balance: $1000
    2 27/2/2022 Withdrawal $300 Balance: $700
    3 28/2/2022 Withdrawal $250 Balance: $450
    4 1/3/2022 No transaction Balance: $450
    5 2/3/2022 Withdrawal $450 Balance: $0
    6 3/3/2022 Deposit $0 Balance: $0
    <BLANKLINE>

    # MyBank class
    >>> take_my_money = MyBank("TakeMyMoney")
    >>> customers = []
    >>> customers.append(Customer("Mr. Gardiner", 1, 1001))
    >>> customers.append(Customer("Mr. Bean", 2, 1002))
    >>> customers.append(Customer("Gabe Newell", 3, 1003))
    >>> customers.append(Customer("Winnie the Pooh", 4, 1004))
    >>> for customer in customers:
    ...     take_my_money.add_customer(customer)
    >>> take_my_money.close_account(customers[1])
    GET_RICH_QUICK ACCOUNT [1002]: Balance $0 Account closed
    >>> import io, sys
    >>> sys.stdin = io.StringIO("500.5")  # input
    >>> take_my_money.deposit_funds(customers[0])
    Enter the amount to deposit:
    >>> take_my_money.deposit_funds(customers[1])   # Should fail
    ...                                             # Account is closed
    Account is closed!
    >>> sys.stdin = io.StringIO("600")  # input
    >>> take_my_money.deposit_funds(customers[3])   # Enter 600
    Enter the amount to deposit:
    >>> sys.stdin = io.StringIO("200")  # input
    >>> take_my_money.withdraw_funds(customers[0]) # Enter 200
    Enter the amount to withdraw:
    >>> take_my_money.display_bank_summary()
    <BLANKLINE>
    ************************************************************************
    TakeMyMoney has 3 customers
    Total amount in customer accounts $900.5
    ************************************************************************
    <BLANKLINE>
    """
    pass


doctest.testmod()  # or doctest.testmod(verbose=True)
