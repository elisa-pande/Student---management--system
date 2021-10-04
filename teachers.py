class Teachers:
    def __init__(self, param_name: str):
        """
        Constructor for teachers object
        :param param_name: name of the tutor
        """
        # save the name of the element
        self.name = param_name
        # save the number of hours per week
        self.nr_h_week = 0
        # save the max number of hours
        self.nr_h_max_week = 15

    def add_h_per_week(self, number: int) -> None:
        """
        Function for adding number in the weekly schedule
        :param number: the number of hours
        :return: None
        """
        self.nr_h_week += number

    def reduce_h_per_week(self, number: int) -> None:
        """
        Function for reducing number in the weekly schedule
        :param number: the number of hours
        :return: None
        """
        self.nr_h_week -= number

    def check_weekly_hours(self) -> bool:
        """
        Check if actual h are in the normal limit
        :return: True if nr of less than max
        """
        if self.nr_h_week > self.nr_h_max_week:
            return False
        else:
            return True

    def display(self) -> None:
        """
        Prints information about the teachers object
        :return: None
        """
        print("Name:", self.name)
        print("Hours per week:", self.nr_h_week)
        print("Max hours per week:", self.nr_h_max_week)

    def check_name(self, name: str) -> bool:
        """
        Checks tutor name
        :param name: name to check
        :return: True if name coincide
        """
        return self.name == name


if __name__ == "__main__":
    # test class
    t1 = Teachers("Alejandro Lopez")
    t1.display()



