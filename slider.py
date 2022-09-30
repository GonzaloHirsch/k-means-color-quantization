import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from kmeans import run_algorithm
import matplotlib.ticker as ticker
from compress import store_image

current_val = 0

def build_slider(image, base_color_count):
    # Create the figure and the line that we will manipulate
    rows = 1 if image.shape[0] > image.shape[1] else 2
    cols = 2 if image.shape[0] > image.shape[1] else 1
    fig, (ax1, ax2) = plt.subplots(rows, cols, figsize=(12,7))

    # Set the initial images
    ax1.imshow(image/255)
    img_data = ax2.imshow(image/255)

    # Set OG image title
    ax1.set_title(f'Original ({base_color_count} colors)')

    # Removing axis
    # https://pythonguides.com/matplotlib-remove-tick-labels/#:~:text=The%20syntax%20to%20remove%20ticks%20and%20tick%20labels%20are%20as%20follow%3A
    ax1.xaxis.set_major_locator(ticker.NullLocator())
    ax1.yaxis.set_major_locator(ticker.NullLocator())
    ax2.xaxis.set_major_locator(ticker.NullLocator())
    ax2.yaxis.set_major_locator(ticker.NullLocator())

    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(bottom=0.15)

    # Make a horizontal slider to control the frequency.
    axbox = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    text_box = TextBox(axbox, 'Number of Colors', initial=0)
    fig.canvas.blit(fig.bbox)

    # The function to be called anytime a slider's value changes
    def update(val):
        global current_val
        # Initial value, use all colors
        try:
            # Define which image to use
            im = None
            print("CALCULATING IMAGE...")
            if int(val) == 0:
                im = image
                ax2.set_title(f'Original ({base_color_count} colors)')
            # Run algorithm
            else:
                current_val = int(val)
                im = run_algorithm(np.copy(image), current_val)
                ax2.set_title(f'Compressed ({val} colors)')
            # Set the image to the data and update
            print("SETTING IMAGE...")
            img_data.set_data(im/255)
            print("FLUSHING...")
            # copy the image to the GUI state, but screen might not be changed yet
            fig.canvas.blit(fig.bbox)
            # flush any pending GUI events, re-painting the screen if needed
            fig.canvas.flush_events()
            # fig.canvas.flush_events()
        except Exception as err:
            print(err)
    # register the update function with each slider
    text_box.on_submit(update)

    def save_image(event):
        global current_val
        print("SAVING IMAGE...")
        if current_val <= 0:
            current_val = 1
        algo_image = np.array(run_algorithm(np.copy(image), current_val), dtype=np.uint8)
        store_image(algo_image, current_val)

    # Add save button
    btnbox = fig.add_axes([0.81, 0.1, 0.07, 0.03])
    bnext = Button(btnbox, 'Save')
    bnext.on_clicked(save_image)

    plt.show()