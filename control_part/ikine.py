import math
def ikine(x, y, z):
    # Longueurs des bras du robot (à adapter selon le robot)
    l1 = 1.0
    l2 = 1.0
    l3 = 1.0
    
    # Calcul de l'angle q1
    q1 = math.atan2(y, x)
    
    # Calcul de l'angle q3
    D = ((z-l1)**2 + x**2 + y**2 - l2**2 - l3**2) / (2*l2*l3)
    if abs(D) <= 1:
        q3 = math.asin(D)
    else:
        q3 = 0
    # Calcul de l'angle q2
    k1 = l2 + l3*math.sin(q3)
    k2 = l3*math.cos(q3)
    q2 = math.atan2(k1(z-l1) - k2(math.sqrt(x**2 + y**2)), k2(z-l1) + k1(math.sqrt(x**2 + y**2)))     
    
    return q1, q2, q3