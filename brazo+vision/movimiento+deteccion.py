import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Configuracion de pines para los servomotores
SERVO_X_PIN = 17  # Movimiento izquierda/derecha
SERVO_Y_PIN = 18  # Movimiento arriba/abajo
SERVO_GARRA_PIN = 27  # Apertura de la garra

# Configuracion de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_X_PIN, GPIO.OUT)
GPIO.setup(SERVO_Y_PIN, GPIO.OUT)
GPIO.setup(SERVO_GARRA_PIN, GPIO.OUT)

# Configuraciï¿½n de PWM para los servos
servo_x = GPIO.PWM(SERVO_X_PIN, 50)
servo_y = GPIO.PWM(SERVO_Y_PIN, 50)
servo_garra = GPIO.PWM(SERVO_GARRA_PIN, 50)

# Posiciones iniciales
servo_x.start(7.5)  # 90 grados (centro)
servo_y.start(2.5)  # 0 grados (posiciï¿½n inicial arriba)
servo_garra.start(5.5)  # Garra completamente abierta

def mover_servo(servo, angulo, delay=0.8):
    duty_cycle = (angulo / 18.0) + 2.5
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(delay)
    servo.ChangeDutyCycle(0)

def detectar_objeto(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x, y, w, h

    return None

def agarrar_objeto():
    print("Bajando para agarrar")
    # Recorrido controlado del servo Y
    for angulo in range(0, 91, 5):  # De 0 a 90 grados, incrementos de 5 grados
        mover_servo(servo_y, angulo, 0.20)  # Control de velocidad con un delay de 0.20 segundos
    time.sleep(1)

    # Cerrando la garra
    print("Cerrando garra")
    mover_servo(servo_garra, 5, 1.5)
    time.sleep(1)

    print("Levantando objeto")
    # Levantar el objeto, moviendo el servo Y de vuelta a la posiciï¿½n inicial
    for angulo in range(90, -1, -5):  # De 90 a 0 grados, incrementos de 5 grados
        mover_servo(servo_y, angulo, 0.20)
    time.sleep(1)

def soltar_objeto():
    print("Soltando objeto")
    mover_servo(servo_garra, 10, 1.5)

def main():
    print("Iniciando captura de video...")
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    if not cap.isOpened():
        print("No se pudo acceder a la camara")
        return

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Error al capturar fotograma")
            break

        resultado = detectar_objeto(frame)
        if resultado:
            x, y, w, h = resultado
            centro_x = x + w // 2

            # Determinar la posiciï¿½n del servo X
            if centro_x < 100:
                angulo_x = 75
            elif centro_x > 220:
                angulo_x = 115
            else:
                angulo_x = 90

            print(f"Moviendo servo X a {angulo_x} grados")
            mover_servo(servo_x, angulo_x, 1.5)
            time.sleep(2)  # Espera 2 segundos antes de mover el servo Y

            # Agarrar objeto sin importar la posiciï¿½n X
            agarrar_objeto()
            soltar_objeto()

            print("Proceso terminado")
            break  # Finaliza la ejecuciï¿½n

        cv2.imshow("Deteccion de Objeto Azul", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    servo_x.stop()
    servo_y.stop()
    servo_garra.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    main()