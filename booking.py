class Booking:
    def __init__(self, booking_id: str, screening_id: str,
                 customer_name: str, seat_number: int, status: str = "active"):
        self.booking_id = booking_id
        self.screening_id = screening_id
        self.customer_name = customer_name
        self.seat_number = seat_number
        self.status = status

    def cancel(self) -> None:
        if self.status == "cancelled":
            raise ValueError("この予約はキャンセル済みです")
        self.status = "cancelled"
