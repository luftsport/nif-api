

class Gender:
    def __init__(self, gender):

        genders = {'Male': 'M', 'Female': 'F', 'All': 'A', 'Unknown': 'U'}

        self.value = genders[gender]
