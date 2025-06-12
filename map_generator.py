# map_generator.py
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.title("Detected Locations", pad=20)
plt.axis('off')
plt.text(0.5, 0.5, "Location Map Visualization\n(Replace with actual geodata)", 
         ha='center', va='center')
plt.savefig('map_placeholder.png', dpi=100)

