#!/usr/bin/env python3
"""
Main Entry Point for Industrial Asset Monitoring System
AI-Driven Real-Time Failure Prevention using Deep Learning
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def initialize_app():
    """Initialize the Industrial Asset Monitoring application"""
    logger.info("="*60)
    logger.info("Industrial Asset Monitoring System - Initialization")
    logger.info("="*60)
    
    # Check required directories
    required_dirs = ['data/raw', 'data/processed', 'models', 'logs']
    for directory in required_dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Directory ready: {directory}")
    
    # Initialize components
    logger.info("\n[1] Initializing Data Pipeline...")
    from data.loader import DataLoader
    data_loader = DataLoader()
    logger.info("✓ Data loader initialized")
    
    logger.info("\n[2] Initializing Deep Learning Models...")
    from models.model_trainer import ModelTrainer
    trainer = ModelTrainer()
    logger.info("✓ Model trainer initialized")
    
    logger.info("\n[3] Initializing Inference Engine...")
    from inference.engine import InferenceEngine
    inference_engine = InferenceEngine()
    logger.info("✓ Inference engine initialized")
    
    logger.info("\n[4] Initializing Alert System...")
    from alerts.alert_engine import AlertEngine
    alert_engine = AlertEngine()
    logger.info("✓ Alert engine initialized")
    
    logger.info("\n[5] Initializing REST API...")
    from api.app import create_app
    app = create_app()
    logger.info("✓ REST API application created")
    
    logger.info("\n" + "="*60)
    logger.info("✓ All systems initialized successfully!")
    logger.info("="*60)
    
    return app, inference_engine, alert_engine

def start_monitoring():
    """Start real-time asset monitoring"""
    logger.info("\nStarting Real-Time Monitoring...")
    
    from sensor.mqtt_collector import MQTTCollector
    
    broker = os.getenv('MQTT_BROKER', 'localhost')
    port = int(os.getenv('MQTT_PORT', 1883))
    
    collector = MQTTCollector(broker=broker, port=port)
    logger.info(f"✓ MQTT Collector connected to {broker}:{port}")
    
    return collector

def start_api_server(app, host='0.0.0.0', port=5000, debug=False):
    """Start the REST API server"""
    logger.info(f"\nStarting REST API Server on {host}:{port}")
    logger.info(f"Debug Mode: {debug}")
    logger.info("\nAPI Endpoints:")
    logger.info("  - Assets: GET/POST /api/assets")
    logger.info("  - Monitoring: GET /api/monitoring/health/{asset_id}")
    logger.info("  - Predictions: GET /api/predictions/{asset_id}")
    logger.info("  - Alerts: GET/POST /api/alerts")
    logger.info("  - Dashboard: http://localhost:5000/dashboard")
    logger.info("\nPress CTRL+C to stop the server")
    
    app.run(host=host, port=port, debug=debug)

def main():
    """
    Main application entry point
    """
    try:
        # Initialize application
        app, inference_engine, alert_engine = initialize_app()
        
        # Get configuration
        mode = os.getenv('APP_MODE', 'api').lower()
        debug = os.getenv('DEBUG', 'false').lower() == 'true'
        
        logger.info(f"\nApplication Mode: {mode}")
        
        if mode == 'api':
            # Run REST API server
            start_api_server(app, debug=debug)
            
        elif mode == 'monitor':
            # Run monitoring system
            collector = start_monitoring()
            collector.start()
            
        elif mode == 'training':
            # Run model training
            logger.info("\nStarting Model Training Pipeline...")
            from models.model_trainer import ModelTrainer
            trainer = ModelTrainer()
            trainer.train_all_models()
            
        elif mode == 'inference':
            # Run inference only
            logger.info("\nStarting Inference Engine...")
            from inference.engine import InferenceEngine
            engine = InferenceEngine()
            # Inference loop would go here
            
        elif mode == 'full':
            # Run all components
            import threading
            logger.info("\nStarting Full System (API + Monitoring)...")
            
            # Start monitoring in background thread
            collector = start_monitoring()
            monitor_thread = threading.Thread(target=collector.start, daemon=True)
            monitor_thread.start()
            
            # Start API server in main thread
            start_api_server(app, debug=debug)
        
        else:
            logger.error(f"Unknown mode: {mode}")
            logger.info("Available modes: api, monitor, training, inference, full")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n\nApplication stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
