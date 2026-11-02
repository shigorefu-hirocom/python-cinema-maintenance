class Hall:
    def __init__(self, hall_id: str, name: str, seat_count: int):
        self.hall_id = hall_id
        self.name = name
        self.seat_count = seat_count

    def is_valid_seat(self, seat_number: int) -> bool:
        return type(seat_number) is int and 1 <= seat_number <= self.seat_count
