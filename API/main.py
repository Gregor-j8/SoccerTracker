import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np
import json
from PIL import Image

# Load the three-sixty data
print("Loading JSON data...")
with open(r'c:\Users\grego\workspace\soccerTracker\Data\data\three-sixty\3788741.json', 'r') as f:
    events_data = json.load(f)

print(f"Loaded {len(events_data)} events")

# Load soccer field background image
print("Loading soccer field image...")
field_img = Image.open(r'c:\Users\grego\workspace\soccerTracker\API\Images\free-soccer-field-vector.jpg')

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Animation state
paused = False

# Initialize empty scatter plots that we'll update
teammates_scatter = ax.scatter([], [], c='blue', s=100, label='Teammates', zorder=3)
opponents_scatter = ax.scatter([], [], c='red', s=100, label='Opponents', zorder=3)
actor_scatter = ax.scatter([], [], c='green', s=200, label='Actor', marker='*', zorder=4)
keeper_scatter = ax.scatter([], [], c='orange', s=150, label='Goalkeeper', marker='s', zorder=3)

# Initialize polygon for visible area
visible_area_polygon = None

# Display the soccer field background image
ax.imshow(field_img, extent=[0, 120, 0, 80], aspect='auto', zorder=1, alpha=0.8)

# Set axis limits (soccer field dimensions)
ax.set_xlim(0, 120)
ax.set_ylim(0, 80)
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.legend(loc='upper right')
ax.grid(False)  # Turn off grid since we have the field background

# Animation update function
def update_frame(frame_num):
    global visible_area_polygon

    # Skip update if paused
    if paused:
        return teammates_scatter, opponents_scatter, actor_scatter, keeper_scatter

    # Get current event
    event = events_data[frame_num]

    # Update title with event info
    ax.set_title(f'Soccer Field - Event {frame_num + 1}/{len(events_data)}\nUUID: {event["event_uuid"]}')

    # Extract player positions
    teammate_x, teammate_y = [], []
    opponent_x, opponent_y = [], []
    actor_x, actor_y = [], []
    keeper_x, keeper_y = [], []

    for player in event['freeze_frame']:
        x, y = player['location']

        if player['actor']:
            actor_x.append(x)
            actor_y.append(y)
        elif player['keeper']:
            keeper_x.append(x)
            keeper_y.append(y)
        elif player['teammate']:
            teammate_x.append(x)
            teammate_y.append(y)
        else:
            opponent_x.append(x)
            opponent_y.append(y)

    # Update scatter plots
    teammates_scatter.set_offsets(np.c_[teammate_x, teammate_y])
    opponents_scatter.set_offsets(np.c_[opponent_x, opponent_y])
    actor_scatter.set_offsets(np.c_[actor_x, actor_y])
    keeper_scatter.set_offsets(np.c_[keeper_x, keeper_y])

    # Remove old visible area polygon if it exists
    if visible_area_polygon is not None:
        visible_area_polygon.remove()

    # Draw visible area polygon
    visible_area = event['visible_area']
    # Convert flat array to list of (x, y) tuples
    polygon_points = [(visible_area[i], visible_area[i+1]) for i in range(0, len(visible_area), 2)]
    visible_area_polygon = patches.Polygon(polygon_points, fill=False, edgecolor='purple',
                                          linewidth=2, linestyle='--', alpha=0.6, label='Visible Area')
    ax.add_patch(visible_area_polygon)

    return teammates_scatter, opponents_scatter, actor_scatter, keeper_scatter, visible_area_polygon

# Pause/resume functionality
def on_key(event):
    global paused
    if event.key == ' ':  # Spacebar to pause/resume
        paused = not paused
        status = "PAUSED" if paused else "PLAYING"
        print(f"Animation {status}")

# Connect the key press event
fig.canvas.mpl_connect('key_press_event', on_key)

# Create animation
# interval = milliseconds between frames (100ms = 10 frames per second)
anim = animation.FuncAnimation(fig, update_frame, frames=len(events_data),
                              interval=100, repeat=True, blit=False)

print("Starting animation...")
print("Press SPACEBAR to pause/resume the animation")
plt.show()
