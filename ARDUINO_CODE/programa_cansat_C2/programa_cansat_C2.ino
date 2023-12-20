                              
#include <Wire.h>
#include <SparkFun_BNO080_Arduino_Library.h>

#include <esp_now.h>
#include <WiFi.h>

// BME---------
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>


#include "KalmanFilter.h"
#define SEALEVELPRESSURE_HPA (1013.25)

BNO080 myIMU;
Adafruit_BME280 bme; // I2C


// DIRECCION MAC DEL RECEPTOR
uint8_t broadcastAddress[] = {0x24, 0x6F, 0x28, 0x88, 0xC9, 0x90};
// 0x24,0x6F:28:88:C9:90

// Structura de data 

typedef struct trama_1 {
  uint8_t id;
  struct BME {
    float temperature;
    float pressure ;
    float humidity ;
  } BME;

  struct AccelLin{
    float ax;
    float ay;
    float az;
  } AccelLin;

} trama_1;

trama_1 SensorData;

typedef struct trama_2 {
  uint8_t id;

  struct Orientation{
    float q0;
    float q1;
    float q2;
    float q3;
  } Orientation;

} trama_2;

trama_2 OrData;



//KalmanFilter(Q=0.1, R=1.0, P=1.0, X=0.0)
KalmanFilter kf_Ax(0.02, 4.0, 2.0, 0.0);
KalmanFilter kf_Ay(0.015, 3.0, 3.0, 0.0);
KalmanFilter kf_Az(0.01, 2.0, 2.0, 0.0);

// Variavlees ------------------
unsigned long lastTimeBME = 0;  //  interval  50ms
const long delayBme = 50; // Intervalo de 100 ms

esp_now_peer_info_t peerInfo;

// funcion de retorno al enviar data
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  //Serial.print("\r\nEstado de la data envíada enviada:\t");
  //Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Exito" : "Error");
  Serial.print("ESPNOW ");
  Serial.print(SensorData.id,HEX); Serial.print(": ");
  Serial.print(SensorData.BME.temperature); Serial.print(", "); 
  Serial.print(SensorData.BME.pressure); Serial.print(", "); 
  Serial.print(SensorData.BME.humidity); Serial.print(", \t");
  Serial.print(SensorData.AccelLin.ax); Serial.print(", "); 
  Serial.print(SensorData.AccelLin.ay); Serial.print(", "); 
  Serial.print(SensorData.AccelLin.az); Serial.print(", "); 
  Serial.println(); 

}
 
void setup() {
  // inicializar puerto serial
  Serial.begin(115200);
  Wire.begin();
  
  /*-------------------CONFIGURACION ESPNOW-------------*/
  // Activar wifi
  WiFi.mode(WIFI_STA);
  // Inicializar ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error al inicializar ESP-NOW");
    return;
  }

  
  // Una vez que ESP Now se inicie con éxito, nos registraremos para enviar CB a
  // obtener el estado del paquete transmitido
  esp_now_register_send_cb(OnDataSent);
  
  // Registrar receptor
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Añadir Receptor      
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("No se pudo añadir al receptor");
    return;
  }

  

  /*------- CONFIGURACION SESNOR IMU---------------*/

  if (!myIMU.begin(0x4A)) {
    Serial.println("Error al iniciar BNO085");
    while (1);
  }

  /*------- CONFIGURACION SESNOR BME280---------------*/

  if (!bme.begin(0x76)) {
    Serial.println("Error al iniciar BME280");
    while (1);
  }

  bme.setSampling(Adafruit_BME280::MODE_NORMAL,
                  Adafruit_BME280::SAMPLING_X2,  // temperatura
                  Adafruit_BME280::SAMPLING_X16, // presión
                  Adafruit_BME280::SAMPLING_X1,  // humedad
                  Adafruit_BME280::FILTER_X16,
                  Adafruit_BME280::STANDBY_MS_0_5);



  //myIMU.enableAccelerometer(20); // Configurar el acelerómetro para que se actualice cada 20 ms
  myIMU.enableRotationVector(200);
  myIMU.enableLinearAccelerometer(200);

   SensorData.id = 0X21;
   OrData.id =  0X22;

  delay(500);

}
 
void loop() {
  unsigned long currentTime = millis();

  if (myIMU.dataAvailable()) {


    

    // periodo de muestreo para el BME280 = 20HZ : 50ms
    if (currentTime - lastTimeBME >= delayBme){
        SensorData.BME.temperature  = bme.readTemperature();     //  °C
        SensorData.BME.pressure    = bme.readPressure() / 100.0;  //  hPa
        SensorData.BME.humidity     = bme.readHumidity();          //  %
       
        //PrintDataSensor();
      lastTimeBME = currentTime; // Actualizar el tiempo de envío
    }


    float acx, acy, acz;
    float q0, q1, q2, q3;
    float RadAcu;
    uint8_t CuatAcu, Aacc, Gacc;

    // lectura de la data para lso calculos....
    myIMU.getLinAccel(acx, acy, acz, Aacc);
    myIMU.getQuat( q1, q2, q3, q0, RadAcu, CuatAcu);

    OrData.Orientation.q0 =  q0;
    OrData.Orientation.q1 =  q1;
    OrData.Orientation.q2 =  q2;
    OrData.Orientation.q3 =  q3;


    float ax_s = kf_Ax.update(acx);
    float ay_s = kf_Ay.update(acy);
    float az_s = kf_Az.update(acz);

    //-------- Almacenamiento de la data de aceleracion filtrada--------//
    SensorData.AccelLin.ax = ax_s;
    SensorData.AccelLin.ay = ay_s;
    SensorData.AccelLin.az = az_s;
  

      // Enviar mensaje via ESP-NOW
      esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &SensorData, sizeof(SensorData));
   
      if (result == ESP_OK) {
    
        Serial.println("E correcto");

      }
      else {
        Serial.println("E Fallido");
      }
      
  }

}