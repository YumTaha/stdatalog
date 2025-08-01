#!/usr/bin/env python3
"""
STDatalog Heartbeat Monitor
Background process monitor for CLI and BLE services
"""

import socket
import time
import subprocess
import os
import sys
import logging

# Minimal logging to avoid noise
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler('/home/kirwinr/logs/heartbeat-monitor.log')]
)
logger = logging.getLogger(__name__)

class ServiceMonitor:
    def __init__(self):
        self.cli_socket = ('127.0.0.1', 8888)
        self.consecutive_failures = 0
        self.max_failures = 5
        self.check_interval = 60  # 1 minute
        self.restart_wait = 20    # 20 seconds after restart
        
    def check_cli_health(self):
        """Check if CLI service is responding via socket connection"""
        try:
            logger.info("Checking CLI health via socket 127.0.0.1:8888")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5 second timeout
            result = sock.connect_ex(self.cli_socket)
            sock.close()
            healthy = result == 0
            logger.info(f"CLI health check result: {'HEALTHY' if healthy else 'FAILED'} (code: {result})")
            return healthy
        except Exception as e:
            logger.info(f"CLI health check FAILED with exception: {e}")
            return False
    
    def check_ble_health(self):
        """Check if BLE service is running and has recent activity"""
        try:
            logger.info("Checking BLE health...")
            # Check if BLE service is active
            result = subprocess.run(['systemctl', 'is-active', 'stdatalog-ble'], 
                                  capture_output=True, text=True)
            service_active = result.stdout.strip() == 'active'
            logger.info(f"BLE service status: {result.stdout.strip()}")
            
            if not service_active:
                logger.info("BLE health check FAILED - service not active")
                return False
            
            # Check for recent log activity (last 2 minutes)
            log_file = '/home/kirwinr/logs/stdatalog-ble.log'
            if not os.path.exists(log_file):
                logger.info("BLE health check FAILED - log file not found")
                return False
                
            # Check if log file was modified recently
            mod_time = os.path.getmtime(log_file)
            current_time = time.time()
            time_diff = current_time - mod_time
            recent_activity = time_diff < 120  # Less than 2 minutes old
            
            logger.info(f"BLE log last modified: {time_diff:.1f} seconds ago")
            logger.info(f"BLE health check result: {'HEALTHY' if recent_activity else 'FAILED'} (log activity)")
            return recent_activity
            
        except Exception as e:
            logger.info(f"BLE health check FAILED with exception: {e}")
            return False
    
    def restart_services(self):
        """Stop both services, then restart CLI first, then BLE"""
        try:
            logger.info("🔄 Starting service restart sequence...")
            
            # Stop both services
            logger.info("⏹️ Stopping CLI service...")
            subprocess.run(['sudo', 'systemctl', 'stop', 'stdatalog-cli'], check=True)
            
            logger.info("⏹️ Stopping BLE service...")
            subprocess.run(['sudo', 'systemctl', 'stop', 'stdatalog-ble'], check=True)
            
            # Wait a moment
            logger.info("⏳ Waiting 5 seconds...")
            time.sleep(5)

            # Start CLI first
            logger.info("▶️ Starting CLI service...")
            subprocess.run(['sudo', 'systemctl', 'start', 'stdatalog-cli'], check=True)

            # Wait 3 seconds
            logger.info("⏳ Waiting 3 seconds...")
            time.sleep(3)

            # Start BLE
            logger.info("▶️ Starting BLE service...")
            subprocess.run(['sudo', 'systemctl', 'start', 'stdatalog-ble'], check=True)
            
            logger.info("✅ Services restarted successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to restart services: {e}")
            return False
    
    def reboot_system(self):
        """Reboot the system after too many failures"""
        logger.error("Too many consecutive failures - rebooting system")
        try:
            subprocess.run(['sudo', 'reboot'], check=True)
        except Exception as e:
            logger.error(f"Failed to reboot: {e}")
    
    def run(self):
        """Main monitoring loop"""
        # Wait 1 minute after boot before starting
        logger.info("💓 Heartbeat monitor starting - waiting 60 seconds...")
        total_delay = 60
        for i in range(total_delay, 0, -5):
            # Create progress bar
            progress = (total_delay - i) / total_delay
            bar_length = 20
            filled_length = int(bar_length * progress)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            percentage = int(progress * 100)
            
            logger.info(f"⏳ Boot delay: [{bar}] {percentage}% ({i}s remaining)")
            time.sleep(5)
        
        logger.info("🚀 Starting service health monitoring")
        
        while True:
            try:
                logger.info(f"🔍 Starting health check cycle (failure count: {self.consecutive_failures}/{self.max_failures})")
                
                # Check both services
                cli_healthy = self.check_cli_health()
                ble_healthy = self.check_ble_health()
                
                if cli_healthy and ble_healthy:
                    # Both services healthy - reset failure counter
                    if self.consecutive_failures > 0:
                        logger.info("💚 Services recovered - resetting failure count")
                    self.consecutive_failures = 0
                    logger.info(f"✅ All services healthy - waiting {self.check_interval} seconds for next check")
                    
                    # Progress bar for normal check interval
                    for i in range(self.check_interval, 0, -10):
                        progress = (self.check_interval - i) / self.check_interval
                        bar_length = 15
                        filled_length = int(bar_length * progress)
                        bar = '█' * filled_length + '░' * (bar_length - filled_length)
                        percentage = int(progress * 100)
                        logger.info(f"⏳ Next check in: [{bar}] {percentage}% ({i}s)")
                        time.sleep(10)
                    continue
                
                # At least one service failed
                self.consecutive_failures += 1
                failed_services = []
                if not cli_healthy:
                    failed_services.append("CLI")
                if not ble_healthy:
                    failed_services.append("BLE")
                
                logger.warning(f"💔 Health check FAILED for: {', '.join(failed_services)} "
                             f"(failure {self.consecutive_failures}/{self.max_failures})")
                
                if self.consecutive_failures >= self.max_failures:
                    # Too many failures - reboot system
                    self.reboot_system()
                    break
                else:
                    # Restart services and wait
                    if self.restart_services():
                        logger.info(f"⏳ Waiting {self.restart_wait} seconds before next check")
                        # Progress bar for restart wait
                        for i in range(self.restart_wait, 0, -2):
                            progress = (self.restart_wait - i) / self.restart_wait
                            bar_length = 10
                            filled_length = int(bar_length * progress)
                            bar = '█' * filled_length + '░' * (bar_length - filled_length)
                            percentage = int(progress * 100)
                            logger.info(f"⏳ Post-restart wait: [{bar}] {percentage}% ({i}s)")
                            time.sleep(2)
                    else:
                        # Restart failed - wait normal interval
                        logger.warning(f"⏳ Restart failed - waiting {self.check_interval} seconds before retry")
                        time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("🛑 Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error in monitor loop: {e}")
                time.sleep(self.check_interval)

if __name__ == "__main__":
    # Log startup info
    logger.info("=" * 50)
    logger.info("💓 STDatalog Heartbeat Monitor Starting")
    logger.info(f"📍 Working directory: {os.getcwd()}")
    logger.info(f"🐍 Python version: {sys.version}")
    logger.info(f"👤 Running as user: {os.getenv('USER', 'unknown')}")
    logger.info("=" * 50)
    
    monitor = ServiceMonitor()
    monitor.run()
