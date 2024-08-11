class DateParser:
    @staticmethod
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @staticmethod
    def parse_date(date_str):
        months = ['January', 'February', 'March', 'April','May', 'June', 'July', 'August','September', 'October', 'November', 'December']

        parts = date_str.split("-")
        if len(parts) != 3:
            return None
        
        month = parts[0]
        if month not in months:
            return None

        try:
            day = int(parts[1])
            year = int(parts[2])
        except ValueError:
            return None
        
        month_num = months.index(month) + 1
        
        if month_num < 1 or month_num > 12 or day < 1 or year < 1:
            return None
        
        if month_num in [4, 6, 9, 11] and day > 30:
            return None
        elif month_num == 2:
            if (DateParser.is_leap_year(year) and day > 29) or (not DateParser.is_leap_year(year) and day > 28):
                return None
        elif day > 31:
            return None
        
        return (year, month_num, day)
    
input_value = input()
print(DateParser.parse_date(input_value))