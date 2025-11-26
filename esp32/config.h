/* 
 * Config for many of the settings required for the ESP32 to properly communicate
 * with the computer. All credits to Radhi SGHAIER for the overarching config and
 * WiFi communication
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

#ifndef __CONFG_H___
#define __CONFG_H___

/* Pin Definitions
 * For this ESP32, you could set a pin to an LED to show connection status
 * but this ESP32 communicates with the other via WiFi
 */
#define LED_PIN                     33
#define BTN_PIN                     25

/* Communication params
 * Basic variables for the code. 
 * QUEUE_LEN can really be anything but should match Queue size in the Python code.
 * MAX_BUFFER_LEN should also match Python code, needs to be large enough to transfer data
 */
#define ACK                         "A" // acknowledgment packet
#define QUEUE_LEN                   10
#define MAX_BUFFER_LEN              256

/* WiFi settings
 * Please replace with own network SSID and password
 */
#define WIFI_SSID                   "test"
#define WIFI_PASSWORD               "123456789"

/* Socket for communication
 * Needs to be replaced with the computer's local IP address. 
 * You can find this on Windows by checking settings for the 
 * Network & Internet settings and checking properties. 
 * On Linux run ip addr and put in the local address found there
 */
#define SERVER_ADDRESS              "10.140.15.195"
#define SERVER_PORT                 11111

#endif // __CONFG_H___
