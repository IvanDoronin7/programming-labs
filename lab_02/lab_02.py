def analyze_power_quality(u_list):
    lowV = 0
    highV = 0

    for u in u_list:
        if u < 207:
            lowV += 1
        elif u > 253:
            highV += 1

    deviations = lowV + highV
    total = len(u_list)

    return deviations / total < 0.05

u_list = [220, 205, 230, 260]
print(analyze_power_quality(u_list))
