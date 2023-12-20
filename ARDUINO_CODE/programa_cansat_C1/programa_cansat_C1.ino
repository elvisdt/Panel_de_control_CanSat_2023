#include <Wire.h>
#include <SparkFun_BNO080_Arduino_Library.h>


#include <esp_now.h>
#include <WiFi.h>
#include <RH_NRF24.h>

// Crea una instancia del driver de NRF24, especificando los pines de CE y CSN
RH_NRF24 nrf24(4, 5); // CE, CSN

// BME---------
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// --------------------librerias propias---------------
#include "KalmanFilter.h"

#define SEALEVELPRESSURE_HPA (1014.05)

BNO080 myIMU;
Adafruit_BME280 bme; // I2C


typedef struct struct_message_espnow {
  float q0;
  float q1;
  float q2;
  float q3;
  float temp;
  float altura;

} struct_message_espnow;


// Create a struct_message called myData
struct_message_espnow myDataEsp;



typedef struct struct_data_BME {
  float temperature;
  float pressure ;
  float humidity ;
  float altitude;

} struct_data_BME;
struct_data_BME myDataBME; 

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
trama_1 C2SensorData;

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



float h0; 

////---------------Variables--------------------------


unsigned long t_prev = 0;
unsigned long t_prev1 = 0;

// Variavlees ------------------
unsigned long lastTimeBME = 0;  //  interval  50ms
const long delayBme = 50; // Intervalo de 100 ms

// delays para el muestreo de datos
unsigned long lastTimeSendNRF = 0;  //  interval  50ms

const long intervalBme = 80; // Intervalo de 100 ms


//-----------------------------------FUNCIONES-----------------------

// Instantiate the Kalman filter
//KalmanFilter(Q=0.1, R=1.0, P=1.0, X=0.0)
KalmanFilter kf_Ax(0.02, 4.0, 2.0, 0.0);
KalmanFilter kf_Ay(0.015, 3.0, 3.0, 0.0);
KalmanFilter kf_Az(0.01, 2.0, 2.0, 0.0);


float rk4_position(float t, float x, float v, float h);
float rk4_velocity(float t, float v, float a, float h);

float calcular_jerk(float a_old, float a_new, float delta_t);
float rk4_vel(float v, float a, float delta_t);
float rk4_pos(float x, float v, float delta_t);

void PrintDataC1(void);
void PrintDataSensor(void);



//------funcion ESPNOW---------------//
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len);


void setup() {

  /*--------CONFIGURACION COM SERIAL--------*/
  Serial.begin(115200);
  Wire.begin();


  /*-------------------CONFIGURACION ESPNOW-------------*/

  // Configurar el dispositivo como una estación WiFi
  WiFi.mode(WIFI_STA);

  // Iniciar ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  //------INICIALIZAR EL NRF--------------------
  while (!nrf24.init()) {
    Serial.println("init failed, retrying...");
    delay(1000);  // espera un segundo antes de reintentar
  }
  
  nrf24.setThisAddress(0x01);
  nrf24.setRF(RH_NRF24::DataRate250kbps, RH_NRF24::TransmitPower0dBm); // Cambiar a 250kbps
  nrf24.setHeaderTo(0x02); // Dirección del dispositivo receptor
 

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
  // configuracion para navegacion
  bme.setSampling(Adafruit_BME280::MODE_NORMAL,
                  Adafruit_BME280::SAMPLING_X2,  // temperatura
                  Adafruit_BME280::SAMPLING_X16, // presión
                  Adafruit_BME280::SAMPLING_X1,  // humedad
                  Adafruit_BME280::FILTER_X16,
                  Adafruit_BME280::STANDBY_MS_0_5);
  /*
  // La tasa sugerida es de 25Hz
  // 1 + (2 * T_ovs) + (2 * P_ovs + 0.5) + (2 * H_ovs + 0.5)
  // T_ovs = 2
  // P_ovs = 16
  // H_ovs = 1
  // = 40ms (25Hz)
  // con el tiempo de espera debería ser realmente de 24.16913... Hz
  // delay(1000);
  */
  Serial.println("Iniciando la altura inicicla...");
  float numdata = 50;
  float altitudeSum;
  for (int i = 0; i < numdata ; i++) {
    float altitude =  bme.readAltitude(SEALEVELPRESSURE_HPA); 
    altitudeSum += altitude;
    delay(40); // Retardo de 50 ms entre cada medición
  }

  h0 = altitudeSum/numdata; 

  /* ------PARAMETROS DE LECTURA DEL IMU---------*/

  //myIMU.enableAccelerometer(20); // Configurar el acelerómetro para que se actualice cada 20 ms
  myIMU.enableRotationVector(100);
  myIMU.enableLinearAccelerometer(100);

  delay(1000);
  esp_now_register_recv_cb(OnDataRecv);


  //------------ configuracion de ID-----------
  // carga primaria

   SensorData.id = 0X11;
   OrData.id =  0X12;

  t_prev = millis();
}

void loop() {

    unsigned long currentTime = millis();
    bool success = false;

    // periodo de muestreo para el BME280 = 20HZ : 50ms
    if (currentTime - lastTimeBME >= delayBme){
        myDataBME.temperature = bme.readTemperature();     //  °C
        myDataBME.pressure    = bme.readPressure() / 100.0;  //  hPa
        myDataBME.humidity    = bme.readHumidity();          //  %
        myDataBME.altitude    = bme.readAltitude(SEALEVELPRESSURE_HPA) - h0;          //  m

        //PrintDataSensor();
        SensorData.BME.temperature = myDataBME.temperature;
        SensorData.BME.pressure = myDataBME.pressure;
        SensorData.BME.humidity = myDataBME.humidity;      

        lastTimeBME = currentTime; // Actualizar el tiempo de envío
    }

 
    if (myIMU.dataAvailable()) {

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
      }

    
     if (currentTime - lastTimeSendNRF >= 200){

      bool success = nrf24.send((uint8_t*)&SensorData, sizeof(SensorData));
      nrf24.waitPacketSent();

      if (success){
          Serial.print("NRF24 ");
          Serial.print(SensorData.id, HEX); Serial.print(": ");
          Serial.print(SensorData.BME.temperature); Serial.print(", "); 
          Serial.print(SensorData.BME.pressure); Serial.print(", "); 
          Serial.print(SensorData.BME.humidity); Serial.print(", ");
          Serial.print(SensorData.AccelLin.ax); Serial.print(", "); 
          Serial.print(SensorData.AccelLin.ay); Serial.print(", "); 
          Serial.print(SensorData.AccelLin.az); Serial.print(", "); 
          Serial.println(); 
      }
      else {
        Serial.println("Lost conection...");
      }
      
      lastTimeSendNRF = currentTime; 

      /*
      delay(100);

      nrf24.send((uint8_t*)&OrData, sizeof(OrData));
      nrf24.waitPacketSent();
      
      Serial.print(OrData.id); Serial.print(": ");
      Serial.print(OrData.Orientation.q0); Serial.print(", ");
      Serial.print(OrData.Orientation.q1); Serial.print(", ");
      Serial.print(OrData.Orientation.q2); Serial.print(", ");
      Serial.print(OrData.Orientation.q3); Serial.print(", ");
      Serial.println();  
      */

     }


}




float calcular_jerk(float a_old, float a_new, float delta_t) {
  return (a_new - a_old) / delta_t;
}

//---------------Métodos de cálculo de velocidad-------------------
float euler_vel(float v, float a, float delta_t) {
  return v + a * delta_t;
}

float euler_cromer_vel(float v, float a, float jerk, float delta_t) {
  float a_next = a + jerk * delta_t;
  return v + a_next * delta_t;
}

float heun_vel(float v, float a, float jerk, float delta_t) {
  float a_next = a + jerk * delta_t;
  return v + (a + a_next) / 2.0 * delta_t;
}

float midpoint_vel(float v, float a, float jerk, float delta_t) {
  float a_mid = a + jerk * delta_t / 2.0;
  return v + a_mid * delta_t;
}

float rk4_vel(float v, float a, float delta_t) {
  float k1 = delta_t * a;
  float k2 = delta_t * a;
  float k3 = delta_t * a;
  float k4 = delta_t * a;
  return v + 1 / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4);
}

//---------------Métodos de cálculo de velocidad-------------------
float euler_pos(float x, float v, float delta_t) {
  return x + v * delta_t;
}

float euler_cromer_pos(float x, float v, float v_next, float delta_t) {
  return x + v_next * delta_t;
}

float heun_pos(float x, float v, float v_next, float delta_t) {
  return x + (v + v_next) / 2.0 * delta_t;
}

float midpoint_pos(float x, float v, float v_next, float delta_t) {
  return x + (v + v_next) / 2.0 * delta_t;
}

float rk4_pos(float x, float v, float delta_t) {
  float k1 = delta_t * v;
  float k2 = delta_t * (v + k1 / 2);
  float k3 = k2;   //delta_t * (v + k2 / 2);
  float k4 = delta_t * (v + k3);
  return x + (k1 + 2 * k2 + 2 * k3 + k4)/6;
}

//-------------------------------------------------------------------------------
float rk4_position( float x, float v, float h) {
  float k1 = h * v;
  float k2 = h * (v + k1/2);
  float k3 = k2;
  float k4 = h * (v + k3);
  return x + (k1 + 2*k2 + 2*k3 + k4) / 6;
}

//--------------Método Runge-Kutta de cuarto orden (RK4) para calcular la velocidad
float rk4_velocity(float t, float v, float a, float h) {
  float k1 = h * a;
  float k2 = h * a; // La aceleración es constante en este intervalo de tiempo
  float k3 = k2;
  float k4 = h * a;
  return v + (k1 + 2*k2 + 2*k3 + k4) / 6;
}

//----------------------------filtros--------------------



//--------- Funcion de retorno ESPNOW----------
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&C2SensorData, incomingData, sizeof(C2SensorData));

  //Serial.println();
  
  //Serial.print("Bytes recibidos: ");
  //Serial.println(len);

  Serial.print("ESPNOW ");
  Serial.print(C2SensorData.id,HEX); Serial.print(": ");
  Serial.print(C2SensorData.BME.temperature); Serial.print(", "); 
  Serial.print(C2SensorData.BME.pressure); Serial.print(", "); 
  Serial.print(C2SensorData.BME.humidity); Serial.print(", ");
  Serial.print(C2SensorData.AccelLin.ax); Serial.print(", "); 
  Serial.print(C2SensorData.AccelLin.ay); Serial.print(", "); 
  Serial.print(C2SensorData.AccelLin.az); Serial.print(", "); 
  Serial.println(); 


}
