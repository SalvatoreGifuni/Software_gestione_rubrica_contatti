class Contact:
    """
    A class to represent a contact.

    Attributes
    ----------
    name : str
        first name of the contact
    surname : str
        surname of the contact
    numbers : list[str]
        list of contact numbers
    emails : list[str]
        list of contact emails
    more_info : str
        additional information about the contact
    """
    def __init__(self, name: str, surname: str, numbers: list[str], emails: list[str], more_info: str):
        
        """
        Constructs all the necessary attributes for the contact object.

        Parameters
        ----------
        name : str
            first name of the contact
        surname : str
            surname of the contact
        numbers : list[str]
            list of contact numbers
        emails : list[str]
            list of contact emails
        more_info : str
            additional information about the contact
        """
        self.name = name
        self.surname = surname
        self.numbers = numbers
        self.emails = emails
        self.more_info = more_info

    def __str__(self) -> str:
        """
        Returns a string representation of the contact.

        Returns
        -------
        str
            formatted string containing contact details
        """
        return f"Name: {self.name} {self.surname}\nNumbers: {', '.join(self.numbers)}\nEmails: {', '.join(self.emails)}\nInfo: {self.more_info}"