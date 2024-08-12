import re
import json
import os
from typing import List, Callable, Dict
from Contact import Contact

GOODBYE_MESSAGE = "Goodbye!"
INVALID_CHOICE_MESSAGE = "Invalid choice. Please try again."
INVALID_MESSAGE = "Invalid Format."
SUCC_UPDATE = "Contact updated successfully!"
NO_CONTACT = "Contact not found."
NO_FILE = "No file found."
ADD_MENU = "MENU\n1: Add Contact\n2: View Contacts\n3: Modify Contact\n4: Delete Contact\n5: Search Contact\n6: Save and Load Contacts\n7: Exit"
EDIT_MENU = "MENU\n1: Edit Name_Surname\n2: Edit Numbers\n3: Edit Emails\n4: Edit Info\n5: Exit"
SEPARATORS = ", -"
YES_LIST = {'y', 'yes'}
NO_LIST = {'n', 'no'}

class ContactManager:
    """
    A class to manage contacts.

    Attributes
    ----------
    contacts : Dict[str, Contact]
        dictionary to store contacts with the full name as the key

    Methods
    -------
    print_menu(menu: str)
        Prints the provided menu.
    is_valid_name(name: str) -> bool
        Checks if the provided name is valid.
    verify_contact_number(contact_number: str) -> bool
        Verifies if the provided contact number is valid.
    verify_contact_email(contact_email: str) -> bool
        Verifies if the provided contact email is valid.
    get_input(prompt: str, validation_fn: Callable[[str], bool], error_message: str) -> str
        Prompts the user for input and validates it.
    contact_number() -> List[str]
        Prompts the user to enter contact numbers.
    contact_email() -> List[str]
        Prompts the user to enter contact emails.
    contact_name() -> str
        Prompts the user to enter a contact name.
    contact_surname() -> str
        Prompts the user to enter a contact surname.
    contact_more_info() -> str
        Prompts the user to enter additional contact information.
    add_contact() -> None
        Adds a new contact.
    view_contacts() -> None
        Displays all contacts.
    edit_contact() -> None
        Edits an existing contact.
    delete_contact() -> None
        Deletes a contact.
    search_contact() -> List[str]
        Searches for a contact and returns the results.
    save_contacts(filepath: str) -> None
        Saves contacts to a file.
    load_contacts(filepath: str) -> None
        Loads contacts from a file.
    main() -> None
        Main function to run the contact manager.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the ContactManager object.
        """
        self.contacts: Dict[str, Contact] = {}

    def print_menu(self, menu: str) -> None:
        """
        Prints the provided menu.

        Parameters
        ----------
        menu : str
            the menu to be printed
        """
        print(menu)

    def is_valid_name(self, name: str) -> bool:
        """
        Checks if the provided name is valid.

        Parameters
        ----------
        name : str
            the name to be validated

        Returns
        -------
        bool
            True if the name is valid, False otherwise
        """
        return all(char.isalpha() or char in SEPARATORS for char in name)

    def verify_contact_number(self, contact_number: str) -> bool:
        """
        Verifies if the provided contact number is valid.

        Parameters
        ----------
        contact_number : str
            the contact number to be validated

        Returns
        -------
        bool
            True if the contact number is valid, False otherwise
        """
        return contact_number.isdigit() and len(contact_number) == 10

    def verify_contact_email(self, contact_email: str) -> bool:
        """
        Verifies if the provided contact email is valid.

        Parameters
        ----------
        contact_email : str
            the contact email to be validated

        Returns
        -------
        bool
            True if the contact email is valid, False otherwise
        """
        pattern = r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, contact_email) is not None

    def get_input(self, prompt: str, validation_fn: Callable[[str], bool], error_message: str) -> str:
        """
        Prompts the user for input and validates it.

        Parameters
        ----------
        prompt : str
            the input prompt
        validation_fn : Callable[[str], bool]
            the validation function
        error_message : str
            the error message to be displayed if validation fails

        Returns
        -------
        str
            the validated user input
        """
        while True:
            user_input = input(prompt).strip()
            if validation_fn(user_input):
                return user_input
            print(error_message)

    def contact_number(self) -> List[str]:
        """
        Prompts the user to enter contact numbers.

        Returns
        -------
        list[str]
            the list of contact numbers
        """
        contact_numbers = []
        while True:
            number = self.get_input("Enter contact number (10 digits) or 'u' for 'Unknown': ", lambda x: x.lower() == "u" or self.verify_contact_number(x), "Invalid number format. Please enter a 10-digit number.")
            if number.lower() == "u":
                number = "unknown"
            contact_numbers.append(number)

            if number == "unknown":
                break

            if not self.get_input("Do you want to add more numbers? (y/n): ", lambda x: x.lower() in YES_LIST | NO_LIST, INVALID_MESSAGE).lower() in YES_LIST:
                break

        return contact_numbers

    def contact_email(self) -> List[str]:
        """
        Prompts the user to enter contact emails.

        Returns
        -------
        list[str]
            the list of contact emails
        """
        contact_emails = []
        while True:
            email = self.get_input("Enter contact email or 'u' for 'Unknown': ", lambda x: x.lower() == "u" or self.verify_contact_email(x), "Invalid email format. Please enter a valid email address.")
            if email.lower() == "u":
                email = "unknown"
            contact_emails.append(email)

            if email == "unknown":
                break

            if not self.get_input("Do you want to add more emails? (y/n): ", lambda x: x.lower() in YES_LIST | NO_LIST, INVALID_MESSAGE).lower() in YES_LIST:
                break

        return contact_emails

    def contact_name(self) -> str:
        """
        Prompts the user to enter a contact name.

        Returns
        -------
        str
            the contact name
        """
        return self.get_input("Enter contact name: ", self.is_valid_name, "Invalid name format. Please use only letters and separators ( , - ).")

    def contact_surname(self) -> str:
        """
        Prompts the user to enter a contact surname.

        Returns
        -------
        str
            the contact surname
        """
        surname = self.get_input("Enter contact surname or 'u' for 'Unknown': ", lambda x: x.lower() == "u" or self.is_valid_name(x), "Invalid surname format. Please use only letters and separators ( , - ).")
        return " " if surname.lower() == "u" else surname

    def contact_more_info(self) -> str:
        """
        Prompts the user to enter additional contact information.

        Returns
        -------
        str
            the additional contact information
        """
        more_info = input("Enter contact more information or 'n' for 'None': ").strip()
        return "None" if more_info.lower() == "n" else more_info

    def add_contact(self) -> None:
        """
        Adds a new contact.
        """
        name = self.contact_name()
        surname = self.contact_surname()
        numbers = self.contact_number()
        emails = self.contact_email()
        more_info = self.contact_more_info()

        complete_name = f"{name} {surname}"
        contact = Contact(name, surname, numbers, emails, more_info)
        self.contacts[complete_name] = contact
        print("Contact added successfully!")

    def view_contacts(self) -> None:
        """
        Displays all contacts.
        """
        for contact in self.contacts.values():
            print(contact)

    def edit_contact(self) -> None:
        """
        Edits an existing contact.
        """
        results = self.search_contact()
        if results:
            try:
                index = int(input("Enter the number of the contact you want to edit from the search results: ").strip())
                if 0 <= index < len(results):
                    edit_name = results[index]
                    contact = self.contacts[edit_name]
                    while True:
                        self.print_menu(EDIT_MENU)
                        user_edit_choice = input("Choose an option: ")
                        if user_edit_choice == "1":
                            new_name = self.contact_name()
                            new_surname = self.contact_surname()
                            complete_name = f"{new_name} {new_surname}"
                            contact.name = new_name
                            contact.surname = new_surname
                            self.contacts[complete_name] = self.contacts.pop(edit_name)
                            edit_name = complete_name
                            print(SUCC_UPDATE)
                        elif user_edit_choice == "2":
                            contact.numbers = self.contact_number()
                            print(SUCC_UPDATE)
                        elif user_edit_choice == "3":
                            contact.emails = self.contact_email()
                            print(SUCC_UPDATE)
                        elif user_edit_choice == "4":
                            contact.more_info = self.contact_more_info()
                            print(SUCC_UPDATE)
                        elif user_edit_choice == "5":
                            break
                        else:
                            print(INVALID_CHOICE_MESSAGE)
                else:
                    print(INVALID_CHOICE_MESSAGE)
            except (ValueError, IndexError):
                print(INVALID_CHOICE_MESSAGE)
            except KeyError as e:
                print(f"Error editing contact: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def delete_contact(self) -> None:
        """
        Deletes a contact.
        """
        results = self.search_contact()
        if results:
            try:
                index = int(input("Enter the number of the contact you want to delete from the search results: ").strip())
                if 0 <= index < len(results):
                    del_name = results[index]
                    del self.contacts[del_name]
                    print("Contact deleted successfully!")
                else:
                    print(INVALID_CHOICE_MESSAGE)
            except (ValueError, IndexError):
                print(INVALID_CHOICE_MESSAGE)
            except KeyError as e:
                print(f"Error deleting contact: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def search_contact(self) -> List[str]:
        """
        Searches for a contact and returns the results.

        Returns
        -------
        list[str]
            the list of search results
        """
        search_key = input("Enter the name or surname of the contact to search: ").strip().casefold()
        results = [(full_name, contact) for full_name, contact in self.contacts.items() if search_key in full_name.casefold().split()]

        if results:
            for i, (full_name, contact) in enumerate(results):
                print(f"{i}: {contact}")
            return [full_name for full_name, contact in results]
        else:
            print(NO_CONTACT)
            return []

    def save_contacts(self, filepath: str) -> None:
        """
        Saves contacts to a file.

        Parameters
        ----------
        filepath : str
            the file path where contacts will be saved
        """
        try:
            with open(filepath, 'w') as file:
                json.dump({name: contact.__dict__ for name, contact in self.contacts.items()}, file, indent=4)
                print("Contacts saved successfully!")
        except IOError as e:
            print(f"Error saving contacts: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def load_contacts(self, filepath: str) -> None:
        """
        Loads contacts from a file.

        Parameters
        ----------
        filepath : str
            the file path from which contacts will be loaded
        """
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    loaded_contacts = json.load(file)
                    self.contacts = {name: Contact(**details) for name, details in loaded_contacts.items()}
                print("Contacts loaded successfully!")
            else:
                print(NO_FILE)
        except IOError as e:
            print(f"Error loading contacts: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def main(self) -> None:
        """
        Main function to run the contact manager.
        """
        filepath = os.path.join(os.getcwd(), "Rubrica.json")

        while True:
            self.print_menu(ADD_MENU)
            user_choice = input("Choose an option: ")
            if user_choice == "1":
                self.add_contact()
            elif user_choice == "2":
                self.view_contacts()
            elif user_choice == "3":
                self.edit_contact()
            elif user_choice == "4":
                self.delete_contact()
            elif user_choice == "5":
                self.search_contact()
            elif user_choice == "6":
                while True:
                    print("1: Save Contacts\n2: Load Contacts\n3: Back")
                    sub_choice = input("Choose an option: ")
                    if sub_choice == "1":
                        self.save_contacts(filepath)
                    elif sub_choice == "2":
                        self.load_contacts(filepath)
                    elif sub_choice == "3":
                        break
                    else:
                        print(INVALID_CHOICE_MESSAGE)
            elif user_choice == "7":
                print(GOODBYE_MESSAGE)
                break
            else:
                print(INVALID_CHOICE_MESSAGE)