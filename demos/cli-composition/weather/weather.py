import subprocess

def get_weather(config):
    loc = config["location"].replace(" ", "+")
    units = "m" if config["metric"] else "u"

    if config["compact"]:
        url = f"https://wttr.in/{loc}?{units}&format=%l:+%c+%t+%w"
    else:
        url = f"https://wttr.in/{loc}?{units}&n"

    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "5", url],
            capture_output=True, text=True, timeout=10
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.rstrip()
        else:
            return f"Weather unavailable (no response)"
    except subprocess.TimeoutExpired:
        return "Weather unavailable (timeout)"
    except FileNotFoundError:
        return "Weather unavailable (curl not found)"
