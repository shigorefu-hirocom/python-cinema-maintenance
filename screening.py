class Screening:
    def __init__(self, screening_id: str, movie_id: str, hall_id: str,
                 starts_at: str, price: int):
        self.screening_id = screening_id
        self.movie_id = movie_id
        self.hall_id = hall_id
        self.starts_at = starts_at
        self.price = price
