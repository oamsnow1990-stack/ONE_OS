import logging
import sys

def get_logger(name: str):
    """สร้าง Logger มาตรฐานสำหรับทุก Service ใน ONE OS"""
    logger = logging.getLogger(name)
    
    # ถ้า logger ถูกตั้งค่าไว้แล้ว ให้คืนค่าเดิมเพื่อป้องกัน duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    
    # สร้าง Handler สำหรับแสดงผลใน Console
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger