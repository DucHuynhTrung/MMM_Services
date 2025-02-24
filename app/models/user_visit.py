from datetime import datetime

class UserVisit:
    def __init__(self, ID: str, FirstName: str, LastName: str, DateVisit: datetime, LastVisit: datetime, TotalVisit: int, IsSignin: bool, DateSignin: datetime = datetime(1750,1,1)):
        self.ID = ID
        self.FirstName = FirstName
        self.LastName = LastName
        self.DateVisit = DateVisit
        self.LastVisit = LastVisit
        self.TotalVisit = TotalVisit
        self.IsSignin = IsSignin
        self.DateSignin = DateSignin

