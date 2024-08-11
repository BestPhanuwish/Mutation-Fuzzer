def check_day(day):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    weekend = ["Saturday", "Sunday"]
    if day in weekdays:
        return "Weekday"
    elif day in weekend:
        return "Weekend"
    else:
        return "Not a valid day"
input_day = input()
print(check_day(input_day))