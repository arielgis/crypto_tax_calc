class CryptoEventList:
    """
    A class to represent a list of CryptoEvent objects.

    Attributes:
        events_list (list): A list to store CryptoEvent objects.

    Methods:
        add_event(crypto_event): Adds a CryptoEvent object to the events_list.
        sort_events(): Sorts the events_list based on the created_time of each CryptoEvent.
        toString(): Returns a string representation of the events_list.
    """

    def __init__(self):
        """
        Initializes a CryptoEventList object with an empty events_list.
        """
        self.events_list = []

    def add_event(self, crypto_event):
        """
        Adds a CryptoEvent object to the events_list.

        Args:
            crypto_event (CryptoEvent): The CryptoEvent object to be added.
        """
        self.events_list.append(crypto_event)

    def sort_events(self):
        """
        Sorts the events_list based on the created_time of each CryptoEvent.
        """
        self.events_list = sorted(self.events_list, key=lambda obj: obj.get_time())

    def toString(self):
        """
        Returns a string representation of the events_list.

        Returns:
            str: A string representation of the events_list.
        """
        my_string = "\n".join([x.toString() for x in self.events_list])
        return my_string  
    

class CryptoEvent:
    """
    A class to represent a list a crypto event.

    Attributes:
        created_time (string): the time of event
        event_type (string): type of event

    Methods:
        get_time():returns the tim
        sort_events(): Sorts the events_list based on the created_time of each CryptoEvent.
        toString(): Returns a string representation of the events_list.
    """
    
    def __init__(self, created_time, event_type):
        """
        Initializes a CryptoEventList object with the time and type of the event
        """
        self.created_time = created_time
        self.event_type = event_type
        
    def get_time(self):
        return self.created_time

class WalletTransferComplete(CryptoEvent):
    def __init__(self, tp1:'WalletTransferPartial', tp2:'WalletTransferPartial'):        
        super().__init__(tp1.get_time(), 'WalletTransferComplete')
        assert tp1.get_transfer_type() == 'withdraw'
        assert tp2.get_transfer_type() == 'deposit'       
        self.from_wallet = tp1.get_wallet()
        self.to_wallet = tp2.get_wallet()
        self.coin = tp1.get_coin()
        self.amount = tp1.get_amount()
        
        
    def toString(self):
        my_string = "WalletTransferComplete;{};{};{};{};{}".format(self.created_time, self.from_wallet, self.to_wallet, self.coin, self.amount)
        return my_string
        
        
class WalletTransferPartialList(CryptoEventList):
        
    def handle_partial_events(self, target_event_list:'CryptoEventList'):
        self.sort_events()
        n = len(self.events_list)
        assert n % 2 == 0, "must be even number"
        for i in range(0, n, 2):
            from_wallet = self.events_list[i]
            to_wallet = self.events_list[i+1]
            assert from_wallet.is_complementary(to_wallet)
            if from_wallet.get_transfer_type() == 'deposit':
                from_wallet, to_wallet = to_wallet, from_wallet
                new_complete_event = WalletTransferComplete(from_wallet, to_wallet)
                target_event_list.add_event(new_complete_event)
        target_event_list.sort_events()
        
        
class WalletTransferPartial(CryptoEvent):
    def __init__(self, created_time, wallet, coin, amount, transfer_type):
        super().__init__(created_time, 'WalletTransferPartial')
        self.wallet = wallet
        self.coin = coin
        self.amount = amount
        if transfer_type not in ['deposit','withdraw']:
            raise ValueError("Invalid input. Allowed values are 'deposit' and 'withdraw'.")
        self.type = transfer_type
        
    def get_wallet(self):
        return self.wallet
    
    def get_coin(self):
        return self.coin 
        
    def get_amount(self):
        return self.amount
    
    def get_transfer_type(self):
        return self.type
        
    def is_complementary(self, other:'WalletTransferPartial') -> bool:
        same_time = self.get_time() == other.get_time()
        same_amount =  self.get_amount() == other.get_amount()
        same_coin =  self.get_coin() == other.get_coin()
        complementary_type = self.get_transfer_type() != other.get_transfer_type()
        return same_time & same_amount & complementary_type        
        
    def toString(self):
        my_string = "WalletTransferPartial;{};{};{};{};{}".format(self.created_time, self.wallet, self.coin, self.amount, self.type)
        return my_string
    




