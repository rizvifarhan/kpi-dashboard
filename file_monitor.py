import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import streamlit as st

class ExcelFileHandler(FileSystemEventHandler):
    def __init__(self, file_path, callback):
        self.file_path = file_path
        self.callback = callback
        self.last_modified = os.path.getmtime(file_path) if os.path.exists(file_path) else 0
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        if event.src_path == self.file_path:
            # Check if file was actually modified (not just accessed)
            current_modified = os.path.getmtime(self.file_path)
            if current_modified > self.last_modified:
                self.last_modified = current_modified
                self.callback()

class FileMonitor:
    def __init__(self):
        self.observer = None
        self.monitoring = False
    
    def start_monitoring(self, file_path, callback):
        """Start monitoring file for changes"""
        if not os.path.exists(file_path):
            return False
        
        try:
            # Stop existing monitoring
            self.stop_monitoring()
            
            # Create event handler
            event_handler = ExcelFileHandler(file_path, callback)
            
            # Set up observer
            self.observer = Observer()
            self.observer.schedule(
                event_handler,
                path=os.path.dirname(file_path),
                recursive=False
            )
            
            # Start monitoring
            self.observer.start()
            self.monitoring = True
            
            return True
            
        except Exception as e:
            st.error(f"Error starting file monitoring: {str(e)}")
            return False
    
    def stop_monitoring(self):
        """Stop file monitoring"""
        if self.observer and self.monitoring:
            self.observer.stop()
            self.observer.join()
            self.monitoring = False
    
    def is_monitoring(self):
        """Check if currently monitoring"""
        return self.monitoring
    
    def get_file_info(self, file_path):
        """Get file information"""
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'modified': time.ctime(stat.st_mtime),
            'created': time.ctime(stat.st_ctime)
        }

class PeriodicChecker:
    def __init__(self, interval=30):
        self.interval = interval
        self.running = False
        self.thread = None
    
    def start(self, check_function):
        """Start periodic checking"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_checker, args=(check_function,))
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Stop periodic checking"""
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _run_checker(self, check_function):
        """Run the periodic checker"""
        while self.running:
            try:
                check_function()
            except Exception as e:
                st.error(f"Error in periodic check: {str(e)}")
            
            time.sleep(self.interval)
