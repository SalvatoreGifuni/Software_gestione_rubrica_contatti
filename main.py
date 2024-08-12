from ContactManager import ContactManager

if __name__ == "__main__":
    """
    The entry point of the Contact Manager program.
    """
    manager = ContactManager()
    try:
        manager.main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")