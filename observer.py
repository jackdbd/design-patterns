class Subscriber(object):
    """It's the Observer object. It receives messages from the Observable."""

    def __init__(self, name):
        self.name = name

    def receive(self, message):
        """Method assigned in, and called by, the Publisher.

        This method is assigned when the Publisher registers a Subscriber to a
        newsletter, and it's called when the Publisher dispatches a message.

        Parameters
        ----------
        message : str
        """
        print("{} received: {}".format(self.name, message))


class Publisher(object):
    """It's the Observable object. It dispatches messages to the Observers."""

    def __init__(self, newsletters):
        self.subscriptions = dict()
        for newsletter in newsletters:
            self.add_newsletter(newsletter)

    def get_subscriptions(self, newsletter):
        return self.subscriptions[newsletter]

    def register(self, newsletter, who, callback=None):
        """Register a Subscriber to this newsletter.

        Parameters
        ----------
        newsletter : str
        who : Subscriber
        callback : method
            callback function bound to the Subscriber object
        """
        if callback is None:
            callback = getattr(who, "receive")
        self.get_subscriptions(newsletter)[who] = callback

    def unregister(self, newsletter, who):
        """Remove a Subscriber object from a subscription to a newsletter.

        Parameters
        ----------
        newsletter : str
        who : Subscriber
        """
        try:
            del self.get_subscriptions(newsletter)[who]
        except KeyError:
            print(
                "{} is not subscribed to the {} newsletter!".format(
                    who.name, newsletter
                )
            )

    def dispatch(self, newsletter, message):
        """Send a message to all subscribers registered to this newsletter.

        Parameters
        ----------
        newsletter : str
        message : str
        """
        if len(self.get_subscriptions(newsletter).items()) == 0:
            print(
                "No subscribers for the {} newsletter. Nothing to send!".format(
                    newsletter
                )
            )
            return

        for subscriber, callback in self.get_subscriptions(newsletter).items():
            callback(message)

    def add_newsletter(self, newsletter):
        """Add a subscription key-value pair for a new newsletter.

        The key is the name of the new subscription, namely the name of the
        newsletter (e.g. 'Tech'). The value is an empty dictionary which will be
        populated by subscriber objects willing to register to this newsletter.

        Parameters
        ----------
        newsletter : str
        """
        self.subscriptions[newsletter] = dict()


def main():

    pub = Publisher(newsletters=["Tech", "Travel"])

    tom = Subscriber("Tom")
    sara = Subscriber("Sara")
    john = Subscriber("John")

    pub.register(newsletter="Tech", who=tom)
    pub.register(newsletter="Travel", who=tom)
    pub.register(newsletter="Travel", who=sara)
    pub.register(newsletter="Tech", who=john)

    pub.dispatch(newsletter="Tech", message="Tech Newsletter num 1")
    pub.dispatch(newsletter="Travel", message="Travel Newsletter num 1")

    pub.unregister(newsletter="Tech", who=john)

    pub.dispatch(newsletter="Tech", message="Tech Newsletter num 2")
    pub.dispatch(newsletter="Travel", message="Travel Newsletter num 2")

    pub.add_newsletter("Fashion")
    pub.register(newsletter="Fashion", who=tom)
    pub.register(newsletter="Fashion", who=sara)
    pub.register(newsletter="Fashion", who=john)
    pub.dispatch(newsletter="Fashion", message="Fashion Newsletter num 1")
    pub.unregister(newsletter="Fashion", who=tom)
    pub.unregister(newsletter="Fashion", who=sara)
    pub.dispatch(newsletter="Fashion", message="Fashion Newsletter num 2")


if __name__ == "__main__":
    main()
