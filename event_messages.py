from dataclasses import dataclass


@dataclass
class EventMessage:
    """Dataclass to help organize the parameters for sending messages about scheduled events."""
    title: str  # The title of the message to be sent.
    description: str = ""  # The description of the message to be sent.
    send_event_link: bool = True  # Whether to include a link to the event in the message, which generates a preview.
    create_discussion_thread: bool = False  # Whether to create a discussion thread from the last sent message.


base_messages = {
    "New": EventMessage(
        title="New Event Created",
        description="Is it a bird? A plane? No! It's a new team event! See details below!",
        create_discussion_thread=True
    ),
    "Updated": EventMessage(
        title="Event Updated",
        description=f"Hear ye, hear ye! An event was updated! See details below!",
    ),
    "Cancelled": EventMessage(
        title="Event Cancelled",
        send_event_link=False,
    ),
}