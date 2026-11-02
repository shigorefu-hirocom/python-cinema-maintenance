class Movie:
    def __init__(self, movie_id: str, title: str, release_year: int,
                 duration_minutes: int):
        self.movie_id = movie_id
        self.title = title
        self.release_year = release_year
        self.duration_minutes = duration_minutes
