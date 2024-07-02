import psycopg2
from faker import Faker
import random

# Conectar a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="proyectofinal",
    host="172.16.185.131",
    port="2222"  # Asegúrate de usar el puerto correcto aquí
)
cur = conn.cursor()

fake = Faker()

cur.execute("SET search_path TO agenciadeviajes;")

# Funciones para generar y rellenar datos para cada tabla

def fill_hoteles(n):
    for _ in range(n):
        cur.execute("""
            INSERT INTO hoteles (nombre, direccion, ciudad, pais, telefono, precioNoche)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            fake.company()[:50],
            fake.address()[:100],
            fake.city()[:50],
            fake.country()[:50],
            str(fake.random_number(digits=10, fix_len=True)),
            round(random.uniform(50, 500), 2)
        ))

def fill_empleados(n):
    for _ in range(n):
        cur.execute("""
            INSERT INTO empleados (cedula, nombre, apellido, direccion, telefono, email, cargo, fechaContratacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            str(fake.random_number(digits=10, fix_len=True)),
            fake.first_name()[:50],
            fake.last_name()[:50],
            fake.address()[:100],
            str(fake.random_number(digits=10, fix_len=True)),
            fake.email()[:100],
            fake.job()[:50],
            fake.date()
        ))

def fill_clientes(n):
    for _ in range(n):
        cur.execute("""
            INSERT INTO clientes (cedula, nombre, apellido, direccion, telefono, email, fechaRegistro)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            str(fake.random_number(digits=10, fix_len=True)),
            fake.first_name()[:50],
            fake.last_name()[:50],
            fake.address()[:100],
            str(fake.random_number(digits=10, fix_len=True)),
            fake.email()[:100],
            fake.date()
        ))

def fill_paquetes(n):
    for _ in range(n):
        cur.execute("""
            INSERT INTO paquetes (nombre, descripcion, precio, duracion, fechaInicio, fechaFin)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            fake.catch_phrase()[:50],
            fake.text(max_nb_chars=200)[:200],
            round(random.uniform(100, 2000), 2),
            random.randint(1, 30),
            fake.date_this_year(before_today=True, after_today=False),
            fake.date_this_year(before_today=False, after_today=True)
        ))

def fill_ofertas(n):
    for _ in range(n):
        cur.execute("""
            INSERT INTO ofertas (nombre, descripcion, descuento, fechaInicio, fechaFin)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            fake.catch_phrase()[:50],
            fake.text(max_nb_chars=200)[:200],
            round(random.uniform(5, 50), 2),
            fake.date_this_year(before_today=True, after_today=False),
            fake.date_this_year(before_today=False, after_today=True)
        ))

def fill_actividades(n):
    for _ in range(n):
        cur.execute("""
            INSERT INTO actividades (nombre, descripcion, precio, duracion, ciudad)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            fake.catch_phrase()[:50],
            fake.text(max_nb_chars=200)[:200],
            round(random.uniform(10, 300), 2),
            random.randint(1, 12),
            fake.city()[:50]
        ))

def fill_destinos(n):
    for _ in range(n):
        cur.execute("""
            INSERT INTO destinos (ciudad, pais, descripcion, precioBase)
            VALUES (%s, %s, %s, %s)
        """, (
            fake.city()[:50],
            fake.country()[:50],
            fake.text(max_nb_chars=200)[:200],
            round(random.uniform(100, 1000), 2)
        ))

def fill_vuelos(n, destinos_ids):
    for _ in range(n):
        cur.execute("""
            INSERT INTO vuelos (numeroVuelo, aerolinea, origen, destinoID, fechaSalida, fechaLlegada, precio)
            VALUES  (%s, %s, %s, %s, %s, %s, %s)
        """, (
            fake.unique.bothify(text='??-#####')[:10],
            fake.company()[:50],
            fake.city()[:50],
            random.choice(destinos_ids),
            fake.date_time_this_year(before_now=True, after_now=False),
            fake.date_time_this_year(before_now=False, after_now=True),
            round(random.uniform(100, 1000), 2)
        ))

def fill_descuentosPaquetes(n, paquetes_ids, ofertas_ids):
    for _ in range(n):
        cur.execute("""
            INSERT INTO descuentosPaquetes (paqueteID, ofertaID)
            VALUES (%s, %s)
        """, (
            random.choice(paquetes_ids),
            random.choice(ofertas_ids)
        ))

def fill_reservas(n, clientes_ids, paquetes_ids, hoteles_ids, vuelos_ids, actividades_ids, empleados_ids):
    for _ in range(n):
        cliente_id = random.choice(clientes_ids)
        paquete_id = random.choice(paquetes_ids) if paquetes_ids else None
        hotel_id = random.choice(hoteles_ids) if hoteles_ids else None
        actividad_id = random.choice(actividades_ids) if actividades_ids else None
        empleado_id = random.choice(empleados_ids) if empleados_ids else None
        vuelo_id = random.choice(vuelos_ids) if vuelos_ids else None
        fecha_reserva = fake.date_time_this_year(before_now=True, after_now=False)
        estado = random.choice(['Reservado', 'Cancelado', 'Confirmado'])
        
        fecha_entrada_hotel = fake.date_time_this_year(before_now=False, after_now=True) if hotel_id else None
        fecha_salida_hotel = fake.date_time_this_year(before_now=False, after_now=True) if hotel_id else None
        habitacion_hotel = random.randint(1, 100) if hotel_id else None
        
        asiento_vuelo = random.randint(1, 100) if vuelo_id else None
        
        fecha_actividad = fake.date_time_this_year(before_now=False, after_now=True) if actividad_id else None
        
        cur.execute("""
            INSERT INTO reservas (clienteID, paqueteID, hotelID, actividadID, empleadoID, vueloID, fechaReserva, estado, fechaEntradaHotel, fechaSalidaHotel, habitacionHotel, asientoVuelo, fechaActividad)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            cliente_id,
            paquete_id,
            hotel_id,
            actividad_id,
            empleado_id,
            vuelo_id,
            fecha_reserva,
            estado,
            fecha_entrada_hotel,
            fecha_salida_hotel,
            habitacion_hotel,
            asiento_vuelo,
            fecha_actividad
        ))

def fill_pagos(n, reservas_ids):
    if not reservas_ids:
        print("No hay reservas disponibles para usar en fill_pagos.")
        return

    for _ in range(n):
        cur.execute("""
            INSERT INTO pagos (reservaID, monto, fechaPago, metodoPago)
            VALUES (%s, %s, %s, %s)
        """, (
            random.choice(reservas_ids),
            round(random.uniform(50, 1000), 2),
            fake.date(),
            random.choice(['Tarjeta de Crédito', 'Transferencia Bancaria', 'PayPal'])
        ))

# Llamadas a las funciones para rellenar las tablas
fill_hoteles(10)
fill_empleados(50)
fill_clientes(100)
fill_paquetes(20)
fill_ofertas(10)
fill_actividades(30)
fill_destinos(20)

# Obtener IDs generados para las relaciones
cur.execute("SELECT destinoID FROM destinos")
destinos_ids = [row[0] for row in cur.fetchall()]

fill_vuelos(50, destinos_ids)

# Obtener IDs generados para las relaciones en reservas y otros
cur.execute("SELECT clienteID FROM clientes")
clientes_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT paqueteID FROM paquetes")
paquetes_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT hotelID FROM hoteles")
hoteles_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT vueloID FROM vuelos")
vuelos_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT actividadID FROM actividades")
actividades_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT empleadoID FROM empleados")
empleados_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT ofertaID FROM ofertas")
ofertas_ids = [row[0] for row in cur.fetchall()]

fill_descuentosPaquetes(30, paquetes_ids, ofertas_ids)
fill_reservas(100, clientes_ids, paquetes_ids, hoteles_ids, vuelos_ids, actividades_ids, empleados_ids)

cur.execute("SELECT reservaID FROM reservas")
reservas_ids = [row[0] for row in cur.fetchall()]

fill_pagos(50, reservas_ids)

conn.commit()

# Cerrar la conexión
cur.close()
conn.close()

