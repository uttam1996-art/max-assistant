
print("Welcome to MAX AI!")

while True:
    command = input("You: ").lower()

    if command == "hello":
        print("MAX: Hello Sir! Kemiti achhanti?")

    elif command == "your name":
        print("MAX: My name is MAX AI.")

    elif command == "how are you":
        print("MAX: Mu bhala achhi Sir!")

    elif command == "exit":
        print("MAX: Goodbye Sir!")
        break

    else:
        print("MAX: Sorry Sir, mu bujhi parili nahi.")
