def seconds_to_HMS(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    secs = int(seconds % 60)
    format_HMS = (hours, minutes, secs)
    return format_HMS

print(seconds_to_HMS(0) == (0, 0, 0))
print(seconds_to_HMS(1) == (0, 0, 1))
print(seconds_to_HMS(69) == (0, 1, 9))
print(seconds_to_HMS(420) == (0, 7, 0))
print(seconds_to_HMS(3661) == (1, 1, 1))
print(seconds_to_HMS(86399) == (23, 59, 59))