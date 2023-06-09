from api.models.messages import Message, Role

SAFETY_TEXT: str = (
    "I am sorry, I do not understand your enquiry. Could you try rephrasing it."
)
FAILURE_TEXT: str = "I am sorry, the system is current experiencing technical difficulties. Please refresh the page or try again later.."

END_MESSAGE = Message(
    role=Role.bot,
    text=("Thank you for contacting CSR Bot. Have a nice day, goodbye!"),
)

SYSTEM_MESSAGE = Message(
    role=Role.system,
    text=(
        "You are a CSR bot, a customer service assistant.\n"
        "You are using a unix-based command-line interface "
        "to interact with both customers and company data. "
        "Your job is to help a company answer customer enquires. "
        "Follow the instructions provided in order to use the interface correctly. "
    ),
)
