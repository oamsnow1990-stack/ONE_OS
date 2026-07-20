import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def generate_performance_report():
    """ดึงข้อมูลจาก SQLite และพล็อตกราฟประสิทธิภาพ"""
    try:
        conn = sqlite3.connect("one_os_memory.db")
        df = pd.read_sql_query("SELECT * FROM experiences", conn)
        conn.close()

        if df.empty:
            print("⚠️ [Visualizer] ยังไม่มีข้อมูลใน Database สำหรับพล็อตกราฟ")
            return

        # ตั้งค่า Layout ของกราฟ
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        plt.subplots_adjust(hspace=0.4)

        # 1. กราฟแนวโน้มความมั่นใจ (Confidence Trend)
        axes[0].plot(df['id'], df['success_rate'], color='cyan', alpha=0.7, label='Success Rate')
        axes[0].plot(df['id'], df['success_rate'].rolling(window=10).mean(), color='blue', label='Moving Avg (10)')
        axes[0].set_title('AI Confidence Evolution (Success Rate Trend)')
        axes[0].set_ylabel('Confidence Level')
        axes[0].legend()
        axes[0].grid(True, linestyle='--', alpha=0.6)

        # 2. กราฟเปรียบเทียบตามสภาพอากาศ (Weather Impact)
        weather_avg = df.groupby('weather')['success_rate'].mean()
        weather_avg.plot(kind='bar', ax=axes[1], color=['orange', 'gray', 'red'], alpha=0.8)
        axes[1].set_title('Performance Analysis by Weather Condition')
        axes[1].set_ylabel('Avg Success Rate')
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)
        axes[1].grid(axis='y', linestyle='--', alpha=0.6)

        print(f"📊 [Visualizer] กราฟถูกสร้างขึ้นสำเร็จ! บันทึกข้อมูลทั้งหมด {len(df)} รายการ")
        plt.show()

    except Exception as e:
        print(f"❌ [Visualizer] เกิดข้อผิดพลาดในการสร้างกราฟ: {e}")

if __name__ == "__main__":
    generate_performance_report()