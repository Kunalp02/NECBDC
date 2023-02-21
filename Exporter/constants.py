import uuid
import string
import random

class RequestStatus:
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'


class PaymentStatus:
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'

class DeliveryStatus:
    PENDING = 'pending'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


def generate_request_number():
    return 'REQ' + str(uuid.uuid1().int >> 64)

def generate_order_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))