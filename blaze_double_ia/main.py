import time
from blaze import BlazeCollector

if __name__ == "__main__":
    print("🚀 IA Blaze Double iniciada.")
    blaze = BlazeCollector()
    while True:
        blaze.coletar_dados()
        time.sleep(10)