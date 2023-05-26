


class Camera:
    def __init__(self) -> None:
        """
        """
        self.id = 0
        self.is_risky = True
    
    def change_params(self,id,is_risky):
        self.id = id
        self.is_risky = is_risky