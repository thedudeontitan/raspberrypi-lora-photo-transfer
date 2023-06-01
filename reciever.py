import time
from PIL import Image
from pyLoRa import LoRa, Modulation

# Configure LoRa parameters
lora = LoRa(serial_port='/dev/ttyUSB0', sync_word=0xAB, frequency=433.0, tx_power=14)

# Receive packets
packets = []
while True:
    packet = lora.receive_packet(modem=Modulation.LORA)
    if packet is not None:
        packets.append(packet)
        print(f"Received packet {len(packets)}")
    else:
        break
    time.sleep(0.1)  # Add a delay between packet checks

# Concatenate the received packets
image_data = b"".join(packets)

# Reconstruct the image
image = Image.frombytes("RGB", (640, 480), image_data)

# Save the received image
image_path = "received_image.jpg"  # Replace with the desired path and filename
image.save(image_path)

# Cleanup
lora.close()