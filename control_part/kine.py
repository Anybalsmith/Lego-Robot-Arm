import numpy as np

def dh_matrix(a, alpha, d, theta):
    """Generate the Denavit-Hartenberg transformation matrix."""
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0,              np.sin(alpha),               np.cos(alpha),              d],
        [0,              0,                           0,                          1]
    ])

def kine(q1, q2, q3):
    """Calculate the position (x, y, z) using DH parameters from the table."""
    # DH parameters from the table
    a1, alpha1, d1 = 0.06, np.pi/2, 0.105  
    a2, alpha2, d2 = 0.155, 0, 0  
    a3, alpha3, d3 = 0, np.pi/2, 0
    
    # Compute individual transformation matrices
    T1 = dh_matrix(a1, alpha1, d1, q1)
    T2 = dh_matrix(a2, alpha2, d2, q2)
    T3 = dh_matrix(a3, alpha3, d3, q3)
    
    # Compute the overall transformation matrix
    T = np.matmul(np.matmul(T1, T2), T3)
    
    # Extract the position (x, y, z) from the transformation matrix
    x, y, z = T[0, 3], T[1, 3], T[2, 3]
    
    return x, y, z, T

# Example usage
#q1 = np.radians(0)  
#q2 = np.radians(0)
#q3 = np.radians(0)

#x, y, z = kine(q1, q2, q3)
#print(f"Position: x = {x}, y = {y}, z = {z}")
