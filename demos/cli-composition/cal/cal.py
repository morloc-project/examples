import calendar
from datetime import date

def show_calendar_wrapper(kwargs):
    return show_calendar(**kwargs)

def show_calendar(
      num_months = 1,
      monday_first = True,
      highlight_today = True,
      show_week_numbers = True
    ):

    today = date.today()
    year = today.year
    month = today.month

    if monday_first:
        first_day = 0
    else:
        first_day = 6

    # 0=Monday in Python's calendar module
    if monday_first:
        calendar.setfirstweekday(0)
    else:
        calendar.setfirstweekday(7)

    day_names_full = list(calendar.day_name)
    day_names_short = list(calendar.day_abbr)

    # rotate to match first_day
    day_names_full = day_names_full[first_day:] + day_names_full[:first_day]
    day_names_short = day_names_short[first_day:] + day_names_short[:first_day]

    lines = []

    for i in range(num_months):
        m = month + i
        y = year
        while m > 12:
            m -= 12
            y += 1

        cal = calendar.Calendar(firstweekday=first_day)
        weeks = cal.monthdayscalendar(y, m)

        # header
        month_name = calendar.month_name[m]
        header = f"{month_name} {y}"

        day_labels = day_names_short

        cw = max(len(d) for d in day_labels) + 1

        wn_prefix = "Wk  " if show_week_numbers else ""
        row_width = len(wn_prefix) + cw * 7
        lines.append(header.center(row_width).rstrip())
        lines.append(wn_prefix + "".join(d.rjust(cw) for d in day_labels))
        lines.append("-" * row_width)

        for week in weeks:
            cells = []
            for day in week:
                if day == 0:
                    cells.append(" " * cw)
                else:
                    day_str = str(day)
                    if (
                        highlight_today
                        and day == today.day
                        and m == today.month
                        and y == today.year
                    ):
                        # ANSI bold + reverse for today
                        styled = f"\033[1;7m{day_str}\033[0m"
                        # pad accounting for ANSI escape length
                        pad = cw - len(day_str)
                        cells.append(" " * pad + styled)
                    else:
                        cells.append(day_str.rjust(cw))

            row = "".join(cells)

            if show_week_numbers:
                # find first nonzero day in the week to compute ISO week number
                real_day = next((d for d in week if d != 0), None)
                if real_day is not None:
                    wn = date(y, m, real_day).isocalendar()[1]
                    row = f"{wn:>2}  {row}"
                else:
                    row = f"    {row}"

            lines.append(row.rstrip())

        if i < num_months - 1:
            lines.append("")

    return "\n".join(lines)
