# Projet : Robot arm pick and place

**IT Project Management Project**

Le but du projet est d'effectuer du *pick and place* à partir d'un bras robotisé Lego muni d'une pince. Ce projet intègre une partie vision qui consiste en la détection des objets à déplacer par la caméra et leurs coordonnées. Une fois cela fait, l'effecteur de notre bras robotisé devra se déplacer vers les coordonnées de la boîte, la saisir (*pick*), puis la déplacer vers une position donnée (*place*).

## La partie vision

La caméra est placée au-dessus de la scène à une distance fixe et détecte les coordonnées du centre de gravité de chaque pièce. Ensuite, elle les ramène dans le repère de base lié à la plateforme du robot.

## La partie commande

À partir du modèle géométrique inverse (MGI) du robot, on peut déterminer les coordonnées articulaires nécessaires $\mathbf{q} = [q_1, q_2, q_3]^T$ de chaque articulation du robot pour le déplacer vers une position précise, représentée par les coordonnées (x, y, z, $\alpha$) où l'on souhaite amener la caisse.

Le MGI peut être déterminé en exploitant la figure suivante :



| MGI | MGI |
|:------------------:|:------------------:|
| ![Description de l'image 1](mgi_1.png) | ![Description de l'image 2](mgi_2.png) |

<span style="color:gray"><small>*source: Cours de Robotique Jacques Gangloff - Telecom Physique Strasbourg*</small></span>

La coordonnée articulaire évidente est bien évidement $q_1 = \alpha$, ou $q_1 = arctan2 (o_y,o_x)$ si l'on ne dispose pas du paramètre $\alpha$.

## Algorithm

```python

# Arm Length
ARM_LENGTH1 = a1
ARM_LENGTH2 = a2
ARM_LENGTH3 = a3

# Calibration
initial_q1 = 0.0
initial_q2 = 0.0
initial_q3 = 0.0

motor_platform.reset_angle(initial_q1)
motor_arm_1.reset_angle(initial_q2)
motor_arm_2.reset_angle(initial_q3)
motor_gripper.reset_angle(0)

current_q1 = initial_q1
current_q2 = initial_q2
current_q3 = initial_q3

Function to_degrees(q1, q2, q3):
    Return q1_deg, q2_deg, q3_deg

Function MGI(x, y, z, alpha):
    q1 = alpha
    q2 = f(x,y,z,ARM_LENGTH1, ARM_LENGTH2)
    q3 = f(x,y,z,ARM_LENGTH1, ARM_LENGTH2)
    return q1, q2, q3

Function move_to(x, y, alpha):
    global current_q1, current_q2, current_q3
    q1,q2,q3 = MGI(x,y,z,alpha)
    q1_deg, q2_deg, q3_deg = to_degrees(q1, q2, q3)

    motor_platform.move(velocity, q1_deg)
    motor_arm_1.move(velocity, q2_deg)
    motor_arm_2.move(velocity, q3_deg)

    # Update current position
    current_q1 = q1
    current_q2 = q2
    current_q3 = q3

# USE CASE

moto_to(20, 30, 10, 25)

```
