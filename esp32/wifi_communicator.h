/* 
 * Communication code for the ESP 32 side. Inspired by the author stated in the
 * next header. Feel free to reference his GitHub for documentation, but I will
 * provide documentation in depth in the code and otherwise to help 
 * maintainability
 *
 * Author: Samantha Raby
 */

/* 
 * -----------------------------------------------------------------------------
 * Example: Two way communication between ESP32 and Python using WIFI
 * -----------------------------------------------------------------------------
 * Author: Radhi SGHAIER: https://github.com/Rad-hi
 * -----------------------------------------------------------------------------
 * Date: 07-05-2023 (7th of May, 2023)
 * -----------------------------------------------------------------------------
 * License: Do whatever you want with the code ...
 *          If this was ever useful to you, and we happened to meet on 
 *          the street, I'll appreciate a cup of dark coffee, no sugar please.
 * -----------------------------------------------------------------------------
 */

#ifndef __WIFI_COMMUNICATOR_H__
#define __WIFI_COMMUNICATOR_H__

#include "my_wifi.h"
#include "config.h"

static SemaphoreHandle_t _send_tsk_mutex;
static SemaphoreHandle_t _recv_tsk_mutex;
static SemaphoreHandle_t _startstop_tsk_mutex;

static QueueHandle_t _send_q;
static QueueHandle_t _recv_q;
static QueueHandle_t _startstop_q;
static TaskHandle_t _socket_reporter_task_h = NULL;

// The sockets client
static WiFiClient _client;

/*
  Attempt to connect the client
*/
void connect_client(){
  Serial.println("[WiFi] Attempting to connect to the computer");
  // We have to connect, no other options
  while(!_client.connect(SERVER_ADDRESS, SERVER_PORT)){ 
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\n[WiFi] Connection successful");
}

bool is_client_connected(){
  return _client.connected();
}

void reconnect() {
  if (!client.connected()) {
    Serial.println("[WiFi] Conection lost. Reconnecting now");
  }
}

void send_message(char *msg){
  xQueueSend(_send_q, (void*)msg, 5);
}

bool get_message(char *msg){
  return xQueueReceive(_recv_q, (void*)msg, 5) == pdTRUE;
}

bool get_stop_message(bool *msg) {
  return xQueueReceive(_startstop_q, (void*)msg, 5) == pdTRUE;
}

/*
  This task would wait for the send signal and send whatever in the sending queue
*/
static void sender_task(void*){
  // Unless conneted to the client, no need for this to run
  xSemaphoreTake(_send_tsk_mutex, portMAX_DELAY);

  char buff[MAX_BUFFER_LEN] = {0};
  while(1){
    // Wait for a notification to do anything
    if(xQueueReceive(_send_q, (void*)&buff, 5) == pdTRUE){
      reconnect();
      _client.print(buff);
      Serial.print("[Sender] Sent: ");
      Serial.println(buff);
    }
    delay(10);
  }
}

/*
  One large tast to handle all the incoming messages from the PC
*/
static void receiver_task(void *){
  // Unless conneted to the client, no need for this to run
  xSemaphoreTake(_recv_tsk_mutex, portMAX_DELAY);

  char buf[MAX_BUFFER_LEN] = {0};

  while(1){
    reconnect();
    // wait until data is available
    if (_client.available()) {
      int idx = 0;
      char ch;

      // Read until the newline character or until the buffer is full
      while(_client.available() && idx < MAX_BUFFER_LEN - 1) {
        ch = _client.read();
        if (ch == '\n') break;
        buf[idx++] = ch;
      }
      buf[idx] = '\0' //Null terminate the buffer

      Serial.print("[Receiver] Received: ");
      Serial.println(buf);

      // For start/stop commands 
      if (strncmp(buf, "CMD:START", 9) == 0) {
        bool val - true;
        xQueueSend(_startstop_q, &val, 5);
        Serial.println("[Receiver] Start command received");
      } else if (strncmp(buf, "CMD:STOP", 8) == 0) {
        bool val = false;
        xQueueSend()_startstop_q, &val, 5;
        Serial.println("[Receiver] Stop command received");
      } else if (buf[0] == 'A') { // Handle ACK-prefixed messages
        Serial.print("[Receiver] ACK received");
        Serial.print(&buf[1]);
        xQueueSend(_recv_q, &buf[1], 5);
      } else { //Our regular message, i.e. data like voltage sweep ranges
        xQueueSend(_recv_q, &buf, 5);
      }
    }
    delay(50); // Prevent CPU Hogging with this small delay
  }
}

/*
  This function would initialize the communicator and setup everything
*/
void setup_wifi_communicator(){
  _send_q = xQueueCreate(QUEUE_LEN, MAX_BUFFER_LEN);
  _recv_q = xQueueCreate(QUEUE_LEN, MAX_BUFFER_LEN);
  _startstop_q = xQueueCreate(QUEUE_LEN, sizeof(bool));

  _recv_tsk_mutex = xSemaphoreCreateMutex();
  _send_tsk_mutex = xSemaphoreCreateMutex();
    
  // block both tasks once created for them to wait for the client to connect
  xSemaphoreTake(_send_tsk_mutex, portMAX_DELAY);
  xSemaphoreTake(_recv_tsk_mutex, portMAX_DELAY);
  
  // Create tasks
  xTaskCreatePinnedToCore(sender_task, "sendTask", 4096, NULL, 3, NULL, 1);
  xTaskCreatePinnedToCore(receiver_task, "receiveTask", 4096, NULL, 3, NULL, 1);

  // Connect before releasing the tasks
  connect_client();

  // release tasks
  xSemaphoreGive(_send_tsk_mutex);
  xSemaphoreGive(_recv_tsk_mutex);
}

#endif // __WIFI_COMMUNICATOR_H__
