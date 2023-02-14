# warehouse-surveillance-system

Website: [Wss-web](https://wssweb.net/)

The project is divided into two parts: client and server

## Client

Use the Raspberry Pi as the terminal node to collect video data. Use opencv as image recognition in Raspberry Pi to detect whether there are strangers approaching the warehouse. If so, the system will start different modes according to the movement trajectory, behavior, and facial features of the person.

## Server
### WSS-web

A device management and data visualization platform built with Django+MySQL.

### Login
![wss_web_login](https://user-images.githubusercontent.com/47854126/217678299-a11a90ec-d8e0-4f9e-bb5e-c846c0e0f1b1.png)

At present, a complete login system has been implemented: including Github-oauth authentication login, registration, password retrieval, email verification and other functions.

### API-management
![api-keys](https://user-images.githubusercontent.com/47854126/217678256-161a0fd2-cf15-49a4-950c-ea281bde3ab1.png)

### Devices
![image](https://user-images.githubusercontent.com/47854126/218561209-bce32ed4-9a80-40ca-8127-1d600e740617.png)


Implemented API-keys management page. Users can add, change, and delete their own APIs.
TODO: Use the API-key to verify the authority for the connection request corresponding to each terminal node.



