import generator
import scanner
import remover
import sys

def main():
    print("Available commands:")
    print(" - 'generate qr code': Create a new QR code")
    print(" - 'scan qr code': Scan a QR code using camera")
    print(" - 'remove qr code': Remove a QR code from database")
    print(" - 'exit': Quit the application")

    while True:
        try:
            user_input = input("\nEnter command: ").strip().lower()
            
            if user_input == "generate qr code":
                generator.generate_qr_code()
            elif user_input == "scan qr code":
                scanner.scan_qr_code()
            elif user_input == "remove qr code":
                remover.remove_qr_code()
            elif user_input == "exit":
                print("Exiting...")
                break
            else:
                print("Unknown command. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
