#!/usr/bin/env python3
"""
Sensor Data Collection Module
Integrates with MQTT broker for real-time data streaming
"""

import logging
import json
from typing import Callable
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class MQTTCollector:
    """
    MQTT collector for real-time sensor data streaming
    """
    
    def __init__(self, broker: str = 'localhost', port: int = 1883, 
                 topics: list = None):
        self.broker = broker
        self.port = port
        self.topics = topics or ['industrial/sensors/#']
        self.client = None
        self.connected = False
        self.message_callbacks = []
        logger.info(f"MQTT Collector initialized: {broker}:{port}")
    
    def connect(self):
        """
        Connect to MQTT broker
        """
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            logger.info(f"Connected to MQTT broker at {self.broker}:{self.port}")
            self.connected = True
        except Exception as e:
            logger.error(f"Failed to connect to MQTT: {str(e)}")
            self.connected = False
    
    def on_connect(self, client, userdata, flags, rc):
        """
        MQTT connection callback
        """
        if rc == 0:
            logger.info("Connected to MQTT broker")
            for topic in self.topics:
                client.subscribe(topic)
                logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Connection failed with code {rc}")
    
    def on_message(self, client, userdata, msg):
        """
        MQTT message callback
        """
        try:
            payload = json.loads(msg.payload.decode())
            logger.debug(f"Message received on {msg.topic}: {payload}")
            
            # Call registered callbacks
            for callback in self.message_callbacks:
                callback(msg.topic, payload)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
    
    def register_callback(self, callback: Callable):
        """
        Register a callback for incoming messages
        """
        self.message_callbacks.append(callback)
    
    def start(self):
        """
        Start listening for messages
        """
        if not self.connected:
            self.connect()
        
        logger.info("Starting MQTT message loop...")
        self.client.loop_forever()
    
    def stop(self):
        """
        Stop listening and disconnect
        """
        if self.client:
            self.client.disconnect()
            logger.info("Disconnected from MQTT broker")


if __name__ == '__main__':
    logger.info("Sensor collection module ready")
