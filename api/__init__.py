#!/usr/bin/env python3
"""
REST API Application
Provides Flask-based REST endpoints for asset monitoring
"""

import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields, Namespace
import os

logger = logging.getLogger(__name__)

def create_app():
    """
    Create and configure Flask application
    """
    app = Flask(__name__)
    CORS(app)
    
    # Load configuration
    app.config['API_TITLE'] = 'Industrial Asset Monitoring API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config['RESTX_MASK_SWAGGER'] = False
    
    # Initialize API
    api = Api(app, version='1.0', title='Asset Monitoring API',
              description='Real-time industrial asset monitoring system')
    
    # Define namespaces
    ns_assets = Namespace('api/assets', description='Asset operations')
    ns_monitoring = Namespace('api/monitoring', description='Monitoring operations')
    ns_predictions = Namespace('api/predictions', description='Prediction operations')
    ns_alerts = Namespace('api/alerts', description='Alert operations')
    
    # Asset model
    asset_model = api.model('Asset', {
        'id': fields.String(required=True),
        'name': fields.String(required=True),
        'type': fields.String(required=True),
        'location': fields.String(),
        'status': fields.String()
    })
    
    @ns_assets.route('')
    class AssetList(Resource):
        def get(self):
            """Get all assets"""
            logger.info("Fetching all assets")
            return {'assets': [], 'count': 0}
        
        @ns_assets.expect(asset_model)
        def post(self):
            """Create new asset"""
            logger.info(f"Creating new asset: {request.json}")
            return {'message': 'Asset created'}, 201
    
    @ns_monitoring.route('/health/<asset_id>')
    class AssetHealth(Resource):
        def get(self, asset_id):
            """Get asset health metrics"""
            logger.info(f"Fetching health for asset: {asset_id}")
            return {
                'asset_id': asset_id,
                'status': 'healthy',
                'health_score': 95.5,
                'timestamp': None
            }
    
    @ns_predictions.route('/<asset_id>')
    class AssetPrediction(Resource):
        def get(self, asset_id):
            """Get RUL prediction"""
            logger.info(f"Fetching prediction for asset: {asset_id}")
            return {
                'asset_id': asset_id,
                'rul': 120.5,
                'confidence': 0.95,
                'unit': 'hours'
            }
    
    @ns_alerts.route('')
    class AlertList(Resource):
        def get(self):
            """Get active alerts"""
            logger.info("Fetching alerts")
            return {'alerts': [], 'count': 0}
        
        def post(self):
            """Create new alert"""
            logger.info(f"Creating alert: {request.json}")
            return {'message': 'Alert created'}, 201
    
    # Register namespaces
    api.add_namespace(ns_assets)
    api.add_namespace(ns_monitoring)
    api.add_namespace(ns_predictions)
    api.add_namespace(ns_alerts)
    
    # Health check
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'version': '1.0.0'})
    
    logger.info("Flask application created")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
