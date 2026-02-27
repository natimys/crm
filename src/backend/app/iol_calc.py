def calculate_srkt(k1: float, k2: float, axl: float, a_constant: float) -> float:
    k_avg = (k1 + k2) / 2
    
    if axl <= 24.2:
        lc = axl
    else:
        lc = -3.446 + 1.396 * axl - 0.013 * (axl ** 2)
        
    r = 337.5 / k_avg
    
    acd_calc = a_constant * 0.62467 - 0.065
    
    numerator = 1336 * (1.336 * r - 0.3333 * lc)
    denominator = (lc - acd_calc) * (1.336 * r - 0.3333 * acd_calc)
    
    iol_power = numerator / denominator
    
    return round(iol_power, 2)