# Payment System Activity
# Objective: To understand and implement Abstraction, Inheritance, and Polymorphism in python using a simple real-world example.

# Problem Statement:
# Create a Payment System where the user selects a payment method and enters payment details.
# Different payment types calculate the final amount differently.

# Requirements:
# The program must:

# Accept user input for required details
# Be implemented using Object-Oriented Programming
# Demonstrate abstraction, encapsulation, inheritance, and polymorphism
# Include clear and meaningful comments in the source code explaining how these OOP concepts are applied in the program

# Abstraction
# Create an abstract base class named Payment
# Include:
# An abstract method pay(amount)
# A concrete method payment_info()

# Encapsulation
# Store the payer name as a private data member
# Provide a method to access it

# Inheritance
# Create two subclasses:
# CashPayment
# CardPayment
# Both must inherit from Payment

# Polymorphism
# Implement the pay(amount) method differently in each subclass
# Use one common function to process both payment types

# Sample Output:
# Enter payer name: Rahul
# Enter amount: 1000

# Choose payment method:
# 1. Cash Payment
# 2. Card Payment
# Enter choice (1 or 2): 2

# --- Payment Details ---
# Payer Name: Rahul
# Final Amount to pay: 1020.0

from abc import ABC, abstractmethod
class Payment(ABC):
    def __init__(self, payer_name):
        self.__payer_name = payer_name  # Encapsulation: private data member

    def get_payer_name(self):
        return self.__payer_name  # Method to access private data member

    @abstractmethod
    def pay(self, amount):
        pass  # Abstract method to be implemented by subclasses

    def payment_info(self):
        return f"Payer Name: {self.get_payer_name()}"  # Concrete method
    
class CashPayment(Payment):
    def pay(self, amount):
        return amount  # No additional charges for cash payment
    
class CardPayment(Payment):
    def pay(self, amount):
        return amount * 1.02  # 2% surcharge for card payment

def process_payment(payment_method, amount):
    final_amount = payment_method.pay(amount)  # Polymorphism: different implementations of pay()
    print("\n--- Payment Details ---")
    print(payment_method.payment_info())
    print(f"Final Amount to pay: {final_amount:.2f}")

if __name__ == "__main__":
    payer_name = input("Enter payer name: ")
    amount = float(input("Enter amount: "))

    print("\nChoose payment method:")
    print("1. Cash Payment")
    print("2. Card Payment")
    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        payment_method = CashPayment(payer_name)
    elif choice == '2':
        payment_method = CardPayment(payer_name)
    else:
        print("Invalid choice!")
        exit()

    process_payment(payment_method, amount)




