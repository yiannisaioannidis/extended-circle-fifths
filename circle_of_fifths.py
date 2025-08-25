import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Chords in custom order (starting from the top, moving clockwise)
chords = [
    "A", "F#m", "D", "Bm", "G", "Em", "C", "Am", "F", "Dm", "Bb", "Gm",
    "Eb", "Cm", "Ab", "Fm", "Db", "Bbm", "F#/Gb", "Ebm", "B", "G#m", "E", "C#m"
]

# Number of points now should be 25 (for 25 chords)
num_points = len(chords)

# Circle radius and center
radius = 20
center = (0, 0)

# Create angles for the 25 points (equally spaced around the circle)
angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.15, right=0.8)  # Adjust space for the textbox

# Textbox for displaying chords
textbox_ax = fig.add_axes([0.85, 0.2, 0, 6])  # Position for textbox
textbox_ax.axis("off")  # Hide the axes

# Initialize textbox with placeholder text
textbox = textbox_ax.text(0.1, 0.1, "Selected Chords\n will be displayed here",
                          horizontalalignment='center', verticalalignment='center',
                          fontsize=12, color='black')
original_text = "Selected Chords\n will be displayed here"

# To store the names of the clicked chords
clicked_chords = []
mirrored_chords = []

# To store the points clicked by the user
clicked_points = []
mirrored_points = []
is_recording = False  # Track whether the recording is active or not
show_mirror = False  # Track whether to show the mirrored shape
show_mirror_vertical = False  # Track whether to show vertical mirror
show_mirror_diagonal = False  # Track whether to show diagonal mirror
show_mirror_diagonal_neg = False  # Track whether to show diagonal mirror for y=-x axis

highlighted_chord = None  # Track the currently highlighted chord

# Compute points once so they can be reused
def compute_points():
    global x_points, y_points
    x_points = center[0] + radius * np.cos(angles)
    y_points = center[1] + radius * np.sin(angles)


# Modify update_textbox to ensure it updates properly
def update_textbox():
    """Updates the textbox with the clicked and transformed chords."""
    selected_chords_text = f"Selected Chords:\n{', '.join(clicked_chords)}" if clicked_chords else "No chords selected."
    transformed_chords_text = f"Transformed Chords:\n{', '.join(mirrored_chords)}" if mirrored_chords else "No transformation applied."

    textbox.set_text(f"{selected_chords_text}\n\n{transformed_chords_text}")
    fig.canvas.draw_idle()

def draw_circle():
    """Draws the circle and places the chords in the correct positions."""
    ax.clear()  # Clear any previous drawings
    ax.set_xlim(-radius - 2, radius + 2)
    ax.set_ylim(-radius - 2, radius + 2)
    ax.set_aspect('equal')
    ax.set_xticks([])  # Hide x ticks
    ax.set_yticks([])  # Hide y ticks
    ax.set_title("Extended Circle of Fifths", fontsize=30)

    # Draw circle
    circle = plt.Circle(center, radius, color='gray', fill=False, linewidth=4)
    ax.add_patch(circle)

    # Plot the chords at each point with optional highlight
    for i, (x, y) in enumerate(zip(x_points, y_points)):
        chord_label = chords[i]
        highlight = (highlighted_chord == i)

        # Highlight the chord label if mouse hovers over it
        ax.text(x, y, chord_label, fontsize=12, ha='center', va='center',
                bbox=dict(facecolor='yellow' if highlight else 'white', edgecolor='black', boxstyle='round,pad=0.3'))

    # Draw the lines between clicked points
    if len(clicked_points) > 1:
        for i in range(1, len(clicked_points)):
            x1, y1 = clicked_points[i - 1]
            x2, y2 = clicked_points[i]
            ax.plot([x1, x2], [y1, y2], 'k-', lw=2)

    # Draw mirrored shape if enabled
    if show_mirror and len(mirrored_points) > 1:
        for i in range(1, len(mirrored_points)):
            x1, y1 = mirrored_points[i - 1]
            x2, y2 = mirrored_points[i]
            ax.plot([x1, x2], [y1, y2], 'r--', lw=3)  # Green dashed for mirror

    # Draw vertical mirrored shape if enabled
    if show_mirror_vertical and len(mirrored_points) > 1:
        for i in range(1, len(mirrored_points)):
            x1, y1 = mirrored_points[i - 1]
            x2, y2 = mirrored_points[i]
            ax.plot([x1, x2], [y1, y2], 'b--.', lw=3)  # Blue dash-dot for vertical mirror

    # Draw diagonal mirrored shape if enabled
    if show_mirror_diagonal and len(mirrored_points) > 1:
        for i in range(1, len(mirrored_points)):
            x1, y1 = mirrored_points[i - 1]
            x2, y2 = mirrored_points[i]
            ax.plot([x1, x2], [y1, y2], 'y--', lw=3)  # Yellow dotted for diagonal mirror

    # Draw diagonal mirrored shape for y = -x axis if enabled
    if show_mirror_diagonal_neg and len(mirrored_points) > 1:
        for i in range(1, len(mirrored_points)):
            x1, y1 = mirrored_points[i - 1]
            x2, y2 = mirrored_points[i]
            ax.plot([x1, x2], [y1, y2], 'm--', lw=3)  # Magenta line for y=-x diagonal mirror

    # Force the canvas to update
    fig.canvas.draw_idle()


def rotate_circle(event, direction):
    """Rotate the circle by a fixed angle in the given direction (clockwise or counterclockwise)."""
    global angles, x_points, y_points, clicked_chords, mirrored_points, mirrored_chords

    rotation_angle = np.radians(15)  # 15-degree step
    if direction == "clockwise":
        rotation_angle *= -1  # Negative for clockwise rotation

    angles = (angles + rotation_angle) % (2 * np.pi)  # Rotate angles
    compute_points()  # Recalculate points after rotation

    # Update clicked chords after rotation
    rotated_chords = []
    for point in clicked_points:
        x_point, y_point = point
        angle = np.arctan2(y_point - center[1], x_point - center[0])
        if angle < 0:
            angle += 2 * np.pi  # Normalize angle
        closest_point_idx = np.argmin(np.abs(angles - angle))
        rotated_chords.append(chords[closest_point_idx])

    clicked_chords = rotated_chords

    update_textbox()  # Update displayed chords
    draw_circle()  # Redraw with updated positions

    # Recalculate mirrored points and chords based on the updated clicked points
    mirrored_points = []
    mirrored_chords = []

    if show_mirror:
        mirrored_points = [(x, -y) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]

    if show_mirror_vertical:
        mirrored_points = [(-x, y) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]

    if show_mirror_diagonal:
        mirrored_points = [(y, x) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]

    if show_mirror_diagonal_neg:
        mirrored_points = [(-y, -x) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]

    update_textbox()  # Update the textbox with the transformed chords after rotation
    draw_circle()  # Redraw the circle with updated positions


def mirror_shape(event):
    """Generates and displays the mirrored version of the recorded shape (horizontal axis)."""
    global mirrored_points, show_mirror, mirrored_chords
    show_mirror = not show_mirror  # Toggle mirror display

    if show_mirror:
        # Reflect over horizontal axis and find the new chords
        mirrored_points = [(x, -y) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]  # Map to new chords
    else:
        mirrored_points = []
        mirrored_chords = []  # Clear mirrored chords when hiding mirror

    update_textbox()  # Update the textbox after transformation
    draw_circle()

def mirror_shape_vertically(event):
    """Generates and displays the vertically mirrored version of the recorded shape."""
    global mirrored_points, show_mirror_vertical, mirrored_chords
    show_mirror_vertical = not show_mirror_vertical  # Toggle vertical mirror display

    if show_mirror_vertical:
        # Reflect over vertical axis and find the new chords
        mirrored_points = [(-x, y) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]  # Map to new chords
    else:
        mirrored_points = []
        mirrored_chords = []  # Clear mirrored chords when hiding mirror

    update_textbox()  # Update the textbox after transformation
    draw_circle()

def mirror_shape_diagonally(event):
    """Generates and displays the diagonally mirrored version of the recorded shape."""
    global mirrored_points, show_mirror_diagonal, mirrored_chords
    show_mirror_diagonal = not show_mirror_diagonal  # Toggle diagonal mirror display

    if show_mirror_diagonal:
        # Reflect over diagonal (swap x and y) and find the new chords
        mirrored_points = [(y, x) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]  # Map to new chords
    else:
        mirrored_points = []
        mirrored_chords = []  # Clear mirrored chords when hiding mirror

    update_textbox()  # Update the textbox after transformation
    draw_circle()

def mirror_shape_diagonal_neg(event):
    """Generates and displays the diagonally mirrored version of the recorded shape for y = -x axis."""
    global mirrored_points, show_mirror_diagonal_neg, mirrored_chords
    show_mirror_diagonal_neg = not show_mirror_diagonal_neg  # Toggle diagonal mirror for y = -x axis

    if show_mirror_diagonal_neg:
        # Reflect over y = -x axis (swap and negate) and find the new chords
        mirrored_points = [(-y, -x) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]  # Map to new chords
    else:
        mirrored_points = []
        mirrored_chords = []  # Clear mirrored chords when hiding mirror

    update_textbox()  # Update the textbox after transformation
    draw_circle()

def get_chord_from_point(x, y):
    """Given a point (x, y), return the corresponding chord based on its position."""
    # Calculate the angle of the point
    angle = np.arctan2(y - center[1], x - center[0])

    if angle < 0:
        angle += 2 * np.pi  # Normalize the angle to be positive

    # Find the closest chord based on the angle
    closest_point_idx = np.argmin(np.abs(angles - angle))
    return chords[closest_point_idx]


def on_click(event):
    """Handles the click event to snap to the nearest chord and record it."""
    global is_recording, clicked_chords, mirrored_chords, mirrored_points, dragged_point_index

    if event.inaxes != ax:  # If the click is outside the main circle area, do nothing
        return

    if not is_recording:
        return  # Do nothing if not recording

    x_click, y_click = event.xdata, event.ydata

    # Find the closest predefined point (snap to nearest chord) on the circle.
    distances = [np.sqrt((x - x_click) ** 2 + (y - y_click) ** 2) for x, y in zip(x_points, y_points)]
    min_distance = min(distances)
    closest_point_idx = distances.index(min_distance)

    # Define a snapping threshold (adjust as needed)
    snap_threshold = radius * 0.2  # Snap if within 20% of the radius

    if min_distance > snap_threshold:
        return  # Ignore clicks that are too far from any chord

    # Get snapped point coordinates (this is the exact chord's position)
    snapped_x = x_points[closest_point_idx]
    snapped_y = y_points[closest_point_idx]

    # Add the clicked point and its corresponding chord to the lists
    clicked_points.append((snapped_x, snapped_y))
    clicked_chords.append(chords[closest_point_idx])  # Add the chord name to clicked_chords

    # Redraw the circle after adding the new chord
    update_textbox()
    draw_circle()


def start_recording(event):
    """Starts recording clicks."""
    global is_recording
    is_recording = True

def stop_recording(event):
    """Stops recording clicks."""
    global is_recording
    is_recording = False
    draw_circle()

def clear_circle(event):
    """Clears all drawn lines, points, and resets the text and chords."""
    global clicked_points, mirrored_points, clicked_chords, mirrored_chords
    global show_mirror, show_mirror_vertical, show_mirror_diagonal, show_mirror_diagonal_neg

    # Clear the points and chords
    clicked_points = []
    mirrored_points = []
    clicked_chords = []
    mirrored_chords = []

    # Reset the flags for mirrors
    show_mirror = False
    show_mirror_vertical = False
    show_mirror_diagonal = False
    show_mirror_diagonal_neg = False

    # Reset the textbox to the original state
    textbox.set_text(original_text)  # Reset text to original placeholder

    draw_circle()  # Redraw the circle after clearing

def on_mouse_move(event):
    """Handles mouse hover event to highlight the chord label."""
    global highlighted_chord
    if event.inaxes == ax:
        # Calculate which chord is being hovered over
        x_mouse, y_mouse = event.xdata, event.ydata
        min_distance = float('inf')
        highlighted_chord = None

        # Compute the closest chord based on the mouse position
        for i, (x, y) in enumerate(zip(x_points, y_points)):
            distance = np.sqrt((x_mouse - x) ** 2 + (y_mouse - y) ** 2)
            if distance < radius * 0.1:  # If within a certain range (radius * 0.1)
                highlighted_chord = i
                break

        draw_circle()

def undo_last_point(event):
    """Handles undo logic, ensuring no new points are added."""
    global clicked_points, mirrored_points, clicked_chords, mirrored_chords

    if clicked_points:  # Only remove if there are points
        # Remove the last clicked point and corresponding chord
        clicked_points.pop()
        clicked_chords.pop()

        # Also update mirrored points and chords
        mirrored_points = [(x, y) for x, y in mirrored_points[:-1]]  # Remove last mirrored point
        mirrored_chords = mirrored_chords[:-1]  # Remove last mirrored chord

        update_textbox()  # Update the text after undo
        draw_circle()  # Redraw the circle after removal
    else:
        print("No points to undo.")  # Optional: Print feedback if there's nothing to undo

# Create buttons with more centered positions
ax_start = plt.axes([0.1, 0.02, 0.2, 0.05])
ax_stop = plt.axes([0.3, 0.02, 0.2, 0.05])
ax_clear = plt.axes([0.5, 0.02, 0.2, 0.05])
#ax_rotate = plt.axes([0.7, 0.02, 0.2, 0.05])
ax_rotate_cw = plt.axes([0.7, 0.02, 0.2, 0.025])
ax_rotate_ccw = plt.axes([0.7, 0.045, 0.2, 0.025])

ax_mirror = plt.axes([0.1, 0.07, 0.2, 0.05])
ax_mirror_vertical = plt.axes([0.3, 0.07, 0.2, 0.05])
ax_mirror_diagonal = plt.axes([0.5, 0.07, 0.2, 0.05])
ax_mirror_diagonal_neg = plt.axes([0.7, 0.07, 0.2, 0.05])

ax_undo = plt.axes([0.1, 0.8, 0.1, 0.05])

btn_start = Button(ax_start, 'Start Recording')
btn_stop = Button(ax_stop, 'Stop Recording')
btn_clear = Button(ax_clear, 'Clear Circle')
#btn_rotate = Button(ax_rotate, 'Transpose')


btn_rotate_cw = Button(ax_rotate_cw, 'Rotate Clockwise')
btn_rotate_ccw = Button(ax_rotate_ccw, 'Rotate Counterclockwise')

btn_rotate_cw.on_clicked(lambda event: rotate_circle(event, "clockwise"))
btn_rotate_ccw.on_clicked(lambda event: rotate_circle(event, "counterclockwise"))


btn_mirror = Button(ax_mirror, 'Mirror Horizontal')
btn_mirror_vertical = Button(ax_mirror_vertical, 'Mirror Vertical')
btn_mirror_diagonal = Button(ax_mirror_diagonal, 'Mirror Diagonal 1')
btn_mirror_diagonal_neg = Button(ax_mirror_diagonal_neg, 'Mirror Diagonal 2')

btn_undo = Button(ax_undo, 'Undo')

btn_start.on_clicked(start_recording)
btn_stop.on_clicked(stop_recording)
btn_clear.on_clicked(clear_circle)
#btn_rotate.on_clicked(rotate_circle)
btn_mirror.on_clicked(mirror_shape)
btn_mirror_vertical.on_clicked(mirror_shape_vertically)
btn_mirror_diagonal.on_clicked(mirror_shape_diagonally)
btn_mirror_diagonal_neg.on_clicked(mirror_shape_diagonal_neg)
# Connect the undo button to the undo handler
btn_undo.on_clicked(undo_last_point)

# Variables to track dragging mode and the points being dragged
is_dragging = False
dragged_point_index = None  # The index of the point being dragged


def enter_drag_mode(event):
    """Toggle the dragging mode for moving points and highlight the button."""
    global is_dragging
    is_dragging = not is_dragging  # Toggle dragging mode

    if is_dragging:
        btn_drag_mode.color = 'lightgreen'  # Highlight the button with light green when drag mode is enabled
        print("Drag Mode: Enabled")
    else:
        btn_drag_mode.color = 'lightgray'  # Reset to light gray when drag mode is disabled
        print("Drag Mode: Disabled")

    btn_drag_mode.hovercolor = 'lightgreen' if is_dragging else 'lightgray'  # Update hover color as well
    fig.canvas.draw_idle()  # Force the canvas to update


def on_drag(event):
    """Handles dragging a point and snapping it to the nearest chord on the circle."""
    global dragged_point_index, clicked_points, clicked_chords, mirrored_points, mirrored_chords

    if not is_dragging or dragged_point_index is None:
        return  # Do nothing if not in drag mode or no point is selected

    x_drag, y_drag = event.xdata, event.ydata
    # Calculate the angle of the dragged point relative to the center
    angle = np.arctan2(y_drag - center[1], x_drag - center[0])
    if angle < 0:
        angle += 2 * np.pi  # Normalize the angle to be positive

    # Find the closest predefined chord based on angle
    nearest_chord_angle = min(angles, key=lambda a: abs(a - angle))

    # Snap the point to the nearest predefined chord (angle)
    snapped_x = center[0] + radius * np.cos(nearest_chord_angle)
    snapped_y = center[1] + radius * np.sin(nearest_chord_angle)

    # Update the clicked_points with the snapped position
    clicked_points[dragged_point_index] = (snapped_x, snapped_y)

    # Find the chord corresponding to the snapped position
    snapped_chord_index = np.argmin(np.abs(angles - nearest_chord_angle))
    clicked_chords[dragged_point_index] = chords[snapped_chord_index]

    # Also update the mirrored points based on the new snapped position
    mirrored_points = []
    mirrored_chords = []

    if show_mirror:
        mirrored_points = [(x, -y) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]

    if show_mirror_vertical:
        mirrored_points = [(-x, y) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]

    if show_mirror_diagonal:
        mirrored_points = [(y, x) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]

    if show_mirror_diagonal_neg:
        mirrored_points = [(-y, -x) for x, y in clicked_points]
        mirrored_chords = [get_chord_from_point(x, y) for x, y in mirrored_points]

    # Redraw the circle after the snap
    update_textbox()
    draw_circle()

def on_mouse_click(event):
    """Handles mouse click events for selecting the point to drag."""
    global is_dragging, dragged_point_index

    if not is_dragging:
        return  # Do nothing if not in dragging mode

    # Identify the nearest point to the click position and set it as the dragged point
    x_click, y_click = event.xdata, event.ydata
    min_distance = float('inf')
    dragged_point_index = None

    # Find the closest point to the mouse click
    for i, (x, y) in enumerate(clicked_points):
        distance = np.sqrt((x_click - x) ** 2 + (y_click - y) ** 2)
        if distance < radius * 0.1:  # If within a certain range (radius * 0.1)
            dragged_point_index = i
            break

# Add new button for dragging mode
ax_drag_mode = plt.axes([0.8, 0.15, 0.1, 0.05])
btn_drag_mode = Button(ax_drag_mode, 'Drag Mode')

btn_drag_mode.on_clicked(enter_drag_mode)

# Compute the points once
compute_points()

# Draw the initial circle
draw_circle()

# Connect the drag and mouse click events
fig.canvas.mpl_connect('button_press_event', on_mouse_click)
fig.canvas.mpl_connect('motion_notify_event', on_drag)

fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

plt.show()
