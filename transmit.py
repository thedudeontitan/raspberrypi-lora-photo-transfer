import time
from PIL import Image
from pyLoRa import LoRa, Modulation

# Configure LoRa parameters
lora = LoRa(serial_port='/dev/ttyUSB0', sync_word=0xAB, frequency=433.0, tx_power=14)

# Load and convert the image
image_path = "image.jpg"  # Replace with the actual image path
image = Image.open(image_path)
image = image.resize((640, 480))  # Adjust image size as needed
image_data = image.tobytes()

# Split the image into smaller packets
packet_size = 64  # Adjust the packet size as needed
packets = [image_data[i:i+packet_size] for i in range(0, len(image_data), packet_size)]

# Send packets
for i, packet in enumerate(packets):
    print(f"Sending packet {i+1}/{len(packets)}")
    lora.send_packet(packet, modem=Modulation.LORA)
    time.sleep(0.1)  # Add a delay between packets

# Cleanup
lora.close()