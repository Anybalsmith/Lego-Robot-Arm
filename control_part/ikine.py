import math
def ikine(x, y, z):
    # Longueurs des bras du robot (à adapter selon le robot)
    a1 = 0.06
    d1 = 0.105
    a2 = 0.155
    d4 = 0.085
    
    # Calcul de l'angle q1
    q1 = math.atan2(y, x)
    
    try:
        # Calcul de l'angle q3
        D = ((z - d1)**2 + (math.sqrt(x**2 + y**2) - a1)**2 - a2**2 - d4**2) / (2 * a2 * d4)
        if abs(D) > 1:
            raise ValueError("La position n'est pas atteignable")

        q3 = math.asin(D)
        
        # Calcul de l'angle q2
        k1 = a2 + d4 * math.sin(q3)
        k2 = d4 * math.cos(q3)
        q2 = math.atan2(
            k1 * (z - d1) - k2 * (math.sqrt(x**2 + y**2) - a1),
            k2 * (z - d1) + k1 * (math.sqrt(x**2 + y**2) - a1)
        )

        return q1, q2, q3
    except ValueError as e:
        print(e)
        return None