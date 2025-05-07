import calendar 

year = 2025

calendar.setfirstweekday(calendar.SUNDAY)
week_number = 1

for month in range(1, 13):
    print(f"\n{calendar.month_name[month]}")
    print("CW  Su Mo Tu We Th Fr Sa")

    month_cal = calendar.monthcalendar(year, month)

    for week in month_cal:

        week_with_cw = [f"CW{week_number:02d}"]
        week_with_cw += [f"{day:2}" if day != 0 else " " for day in week]

        print(" ".join(week_with_cw))

        week_number += 1