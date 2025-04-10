# Robotica2
## Nombres: Cristian Alejandro Durán Ignacio - Alfaro Ayzama José Fernando - Ever Rolando Rejas Espinoza

# 🚀 Proyecto 2

## 🤖 Brazo Robótico con Visión Artificial 🤖
### Este proyecto implementa un brazo robótico, controlado por una Raspberry Pi 4, capaz de **detectar objetos de color azul** mediante una cámara web y **mover sus servomotores** para levantarlos según la posición detectada.

## 📌 Introducción
### El proyecto combina **visión artificial** mediante OpenCV con el control físico de **3 servomotores MG995**, los cuales permiten:

### - Girar la base del brazo de izquierda a derecha,
### - Elevar o bajar la articulación de arriba hacia abajo,
### - Accionar una garra para agarrar objetos azules.
### Este software fue desarrollado y probado en el **editor Mu**, corriendo sobre el sistema operativo Raspbian en una **Raspberry Pi 4**, con acceso remoto desde una PC.

## 🚀Para armado y utilizacion de codigo
### Clonar el repositorio 
git clone https://github.com/Josefer98/Robotica2.git
### Copiar el codigo en un entorno adecuado para python
Para este proyecto se utilzo el editor MU
![Editor MU de Rasbien](files/mu.jpg)
### Instalar dependencias
en la teminal ejecuta:
![comandos](files/comandos.jpg)
### conectar camara y probar en rasberry
conecta la camara mediante el usb
prueba con este comando:
![comandos](files/pruebacam.jpg)
### Armar brazo robótico
  -usa el pin 17 para el primer servomotor que controlara el movimiento de derecha a izquierda
  -usa el pin 18 para el sefundo servomotor que controlara el movimiento de arriba a abajo
  -usa el pin 27 para el tercer servomotor que controlara que la garra abra o cierre
  -coneccion a tierra importante 
  -conecciones
  ![Conecciones echas](files/circuito.jpeg)
  -brazo armado
  ![brazo](brazo/mu.jpeg)
  -opcional el uso de de una fuente para dar energia solo a los servomotores
  ![Fuente](files/fuente.jpeg)
# 🎥Demostracion de funcionamineto
![Brazo robot](files/demostracion.gif)
  
