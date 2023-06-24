import time

# Aceleración inicial
a = 0.0  # Supongamos que es 0.0 para este ejemplo

# Velocidad inicial
v_euler = 0.0
v_euler_cromer = 0.0
v_heun = 0.0
v_midpoint = 0.0
v_rk4 = 0.0

x_euler = 0.0
x_euler_cromer = 0.0
x_heun = 0.0
x_midpoint = 0.0
x_rk4 = 0.0

def leer_sensor():
    # Esta función debería leer el valor de aceleración desde tu sensor
    # Aquí simplemente devolvemos un valor aleatorio como ejemplo
    import random
    return random.random()

def calcular_jerk(a_old, a_new, delta_t):
    return (a_new - a_old) / delta_t

def euler(v, a, delta_t):
    return v + a * delta_t

def euler_cromer_vel(v, a, jerk, delta_t):
    a_next = a + jerk * delta_t
    v_next = v + a_next * delta_t
    return v_next

def heun_vel(v, a, jerk, delta_t):
    a_next = a + jerk * delta_t
    v_next = v + (a + a_next) / 2.0 * delta_t
    return v_next

def midpoint_vel(v, a, jerk, delta_t):
    a_mid = a + jerk * delta_t / 2.0
    v_next = v + a_mid * delta_t
    return v_next

def rk4_vel(v, a, jerk, delta_t):
    k1 = delta_t * a
    k2 = delta_t * (a + jerk * delta_t / 2)
    k3 = delta_t * (a + jerk * delta_t / 2)
    k4 = delta_t * (a + jerk * delta_t)
    v_next = v + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return v_next


def euler_pos(x, v, delta_t):
    return x + v * delta_t

def euler_cromer_pos(x, v, v_next, delta_t):
    return x + v_next * delta_t

def heun_pos(x, v, v_next, delta_t):
    return x + (v + v_next) / 2.0 * delta_t

def midpoint_pos(x, v, v_next, delta_t):
    return x + (v + v_next) / 2.0 * delta_t

def rk4_pos(x, v, delta_t):
    k1 = delta_t * v
    k2 = delta_t * (v + k1 / 2)
    k3 = delta_t * (v + k2 / 2)
    k4 = delta_t * (v + k3)
    return x + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)




t_prev = time.time()

while True:  # Bucle infinito para capturar aceleración en tiempo real
    time.sleep(0.1)

    t_now = time.time()
    delta_t = t_now - t_prev
    
    # Leer el valor de aceleración desde el sensor
    a_new = leer_sensor()

    # Calcular la jerk
    jerk = calcular_jerk(a, a_new, delta_t)

    # Calcular la velocidad utilizando diferentes métodos
    v_euler = euler(v_euler, a_new, delta_t)
    v_euler_cromer = euler_cromer_vel(v_euler_cromer, a_new, jerk, delta_t)
    v_heun = heun_vel(v_heun, a_new, jerk, delta_t)
    v_midpoint = midpoint_vel(v_midpoint, a_new, jerk, delta_t)
    v_rk4 = rk4_vel(v_rk4, a_new, jerk, delta_t)

    # Imprimir las velocidades
    #print(f" VEL > Euler: {v_euler:.6f}, Euler-Cromer: {v_euler_cromer:.6f}, Heun: {v_heun:.6f}, Midpoint: {v_midpoint:.6f}, Rk4: {v_rk4:.6f}")


    # Calcular la posición utilizando diferentes métodos
    x_euler = euler_pos(x_euler, v_euler, delta_t)
    x_euler_cromer = euler_cromer_pos(x_euler_cromer, v_euler_cromer, v_euler_cromer, delta_t)
    x_heun = heun_pos(x_heun, v_heun, v_heun, delta_t)
    x_midpoint = midpoint_pos(x_midpoint, v_midpoint, v_midpoint, delta_t)
    x_rk4 = rk4_pos(x_rk4, v_rk4, delta_t)


    # Imprimir las posiciones
    print(f"POS > Euler: {x_euler:.6f}, Euler-Cromer: {x_euler_cromer:.6f}, Heun: {x_heun:.6f}, Midpoint: {x_midpoint:.6f}, Rk4: {x_rk4:.6f}")


    # Actualizar la la aceleracion old
    a = a_new

    
    # Actualizar t_prev para el próximo ciclo
    t_prev = t_now
