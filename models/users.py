

class User:
    def __init__(self,name, family, hourly_rate, total_hour, total_minute, id=None):
        self.name = name
        self.family = family
        self.hourly_rate = hourly_rate
        self.total_hour = total_hour
        self.total_minute = total_minute
        self.salary = self.calc_salary()
        self.id = id
        


    def full_name(self):
        return f'{self.name} {self.family}'

    def calc_salary(self):
        total_hour = (self.total_minute / 60) + self.total_hour
        salary = int(total_hour * self.hourly_rate)
        return salary

    
           
class Developer(User):
    def __init__(self, name, family, hourly_rate, total_hour, total_minute):
        super().__init__(name, family, hourly_rate, total_hour, total_minute)
        self.role = 'Developer'

    def __repr__(self):
        return f"<({self.id}){self.name} {self.family} - {self.role} - {self.hourly_rate} - {self.salary}>"

    

class Manager(User):
    def __init__(self, name, family, hourly_rate, total_hour, total_minute):
        super().__init__(name, family, hourly_rate, total_hour, total_minute)
        self.role = 'Manager'



