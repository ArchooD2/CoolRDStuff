import sys
import tkinter as tk
from tkinter import colorchooser, simpledialog
from tkinter import ttk
from colour import Color
import pyperclip

def hex_to_rgb(hex_color):
    """Converts a hex color to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    """Converts an RGB tuple to a hex color."""
    return '#{:02X}{:02X}{:02X}'.format(*rgb_color)

def interpolate_color(color1, color2, fraction):
    """Interpolates between two RGB colors by a given fraction."""
    return tuple(
        int(color1[i] + (color2[i] - color1[i]) * fraction)
        for i in range(3)
    )

def generate_gradient_tags(color1_hex, color2_hex, text, color_mid_hexes=[], word_mode=False):
    """Generates color tags for text based on a gradient between two or more hex colors,
    ignoring syllable spacers ('/') and spaces.
    """
    color1_rgb = hex_to_rgb(color1_hex)
    color2_rgb = hex_to_rgb(color2_hex)

    if color_mid_hexes:
        for i in range(len(color_mid_hexes)):
            if color_mid_hexes[i]:
                color_mid_hexes[i] = hex_to_rgb(color_mid_hexes[i])
            else:
                color_mid_hexes = []
                break

    gradient_tags = ""
    segments = text.split(' ') if word_mode else list(text)
    colored_segment_count = len([seg for seg in segments if seg not in ['/', ' ']])

    if colored_segment_count == 0:
        return text  # Return the input directly if there are no colorable characters

    color_index = 0  # To keep track of how many colorable characters have been processed

    for i, segment in enumerate(segments):
        if segment in ['/', ' ']:
            gradient_tags += segment
        else:
            fraction = color_index / (colored_segment_count - 1) if colored_segment_count > 1 else 0
            
            interpolated_color = (255, 255, 255)
            if color_mid_hexes:
                length = len(color_mid_hexes)
                fracnum = 1 / (length + 1)

                for j in range(length + 2):
                    if fraction < (j * fracnum) or fraction > ((j + 1) * fracnum):
                        continue

                    col1 = color1_rgb if j == 0 else color_mid_hexes[j - 1]
                    col2 = color2_rgb if j >= length else color_mid_hexes[min(j, length - 1)]
                    
                    interpolated_color = interpolate_color(col1, col2, (fraction - fracnum * j) * (length + 1))
                    break
            else:
                interpolated_color = interpolate_color(color1_rgb, color2_rgb, fraction)

            color_hex = rgb_to_hex(interpolated_color)
            
            # Handle segments with '/' within them by splitting and reapplying color tags
            if '/' in segment:
                sub_segments = segment.split('/')
                for sub_seg in sub_segments[:-1]:
                    gradient_tags += f"<color={color_hex}>{sub_seg}</color>/"
                gradient_tags += f"<color={color_hex}>{sub_segments[-1]}</color>"
            else:
                gradient_tags += f"<color={color_hex}>{segment}</color>"
            
            color_index += 1

            if word_mode and i < len(segments) - 1:
                gradient_tags += ' '  # Add space between words

    return gradient_tags.strip()


def copy_to_clipboard(text):
    """Copies text to the clipboard."""
    pyperclip.copy(text)

def create_ui():
    root = tk.Tk()
    root.title("Gradient Text Generator")
    root.geometry("500x550")

    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#cccccc")
    
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Color picker and text entry widgets
    ttk.Label(main_frame, text="Start Color:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
    start_color_entry = tk.Entry(main_frame)
    start_color_entry.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

    def pick_start_color():
        color_code = colorchooser.askcolor(title="Choose Start Color")[1]
        if color_code:
            start_color_entry.delete(0, tk.END)
            start_color_entry.insert(0, color_code)
            start_color_preview.config(bg=color_code)

    pick_start_button = ttk.Button(main_frame, text="Pick Color", command=pick_start_color)
    pick_start_button.grid(column=2, row=0, padx=5, pady=5)

    start_color_preview = tk.Label(main_frame, text="", width=2, bg="#ffffff")
    start_color_preview.grid(column=3, row=0, padx=5, pady=5)

    ttk.Label(main_frame, text="End Color:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
    end_color_entry = tk.Entry(main_frame)
    end_color_entry.grid(column=1, row=1, padx=5, pady=5, sticky=(tk.W, tk.E))

    def pick_end_color():
        color_code = colorchooser.askcolor(title="Choose End Color")[1]
        if color_code:
            end_color_entry.delete(0, tk.END)
            end_color_entry.insert(0, color_code)
            end_color_preview.config(bg=color_code)

    pick_end_button = ttk.Button(main_frame, text="Pick Color", command=pick_end_color)
    pick_end_button.grid(column=2, row=1, padx=5, pady=5)

    end_color_preview = tk.Label(main_frame, text="", width=2, bg="#ffffff")
    end_color_preview.grid(column=3, row=1, padx=5, pady=5)

    # Mid color toggle and entry
    ttk.Label(main_frame, text="Mid Color:").grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)
    mid_color_entry = tk.Entry(main_frame)
    mid_color_entry.grid(column=1, row=2, padx=5, pady=5, sticky=(tk.W, tk.E))

    def pick_mid_color():
        color_code = colorchooser.askcolor(title="Choose Mid Color")[1]
        if color_code:
            mid_color_entry.delete(0, tk.END)
            mid_color_entry.insert(0, color_code)
            mid_color_preview.config(bg=color_code)

    pick_mid_button = ttk.Button(main_frame, text="Pick Color", command=pick_mid_color)
    pick_mid_button.grid(column=2, row=2, padx=5, pady=5)

    mid_color_preview = tk.Label(main_frame, text="", width=2, bg="#ffffff")
    mid_color_preview.grid(column=3, row=2, padx=5, pady=5)

    ttk.Label(main_frame, text="Text:").grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
    text_entry = tk.Entry(main_frame, width=40)
    text_entry.grid(column=1, row=3, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E))

    word_mode = tk.BooleanVar()
    word_mode_check = ttk.Checkbutton(main_frame, text="Word Mode", variable=word_mode)
    word_mode_check.grid(column=0, row=4, columnspan=2, pady=5, sticky=tk.W)

    def generate_output():
        start_color = start_color_entry.get()
        end_color = end_color_entry.get()
        mid_color = mid_color_entry.get() if mid_color_entry.get() else None
        text = text_entry.get()
        result = generate_gradient_tags(start_color, end_color, text, color_mid_hexes=[mid_color], word_mode=word_mode.get())
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)
        update_preview(text, start_color, end_color, mid_color, word_mode.get())
        copy_to_clipboard(result)

    def update_preview(text, start_color, end_color, mid_color, word_mode):
        """Updates the preview text widget to display the gradient."""
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        mid_rgb = hex_to_rgb(mid_color) if mid_color else None
        segments = text.split(' ') if word_mode else list(text)
        colored_segment_count = len([seg for seg in segments if seg not in ['/', ' ']])

        preview_text_widget.config(state=tk.NORMAL)
        preview_text_widget.delete(1.0, tk.END)
        color_index = 0

        for i, segment in enumerate(segments):
            if segment in ['/', ' ']:
                preview_text_widget.insert(tk.END, segment)
            else:
                fraction = color_index / (colored_segment_count - 1) if colored_segment_count > 1 else 0

                if mid_rgb:
                    length = 1  # Since we have only one mid color
                    fracnum = 1 / (length + 1)
                    col1 = start_rgb if fraction < fracnum else mid_rgb
                    col2 = mid_rgb if fraction < fracnum else end_rgb
                    interpolated_color = interpolate_color(col1, col2, fraction * (length + 1))
                else:
                    interpolated_color = interpolate_color(start_rgb, end_rgb, fraction)

                color_hex = rgb_to_hex(interpolated_color)
                preview_text_widget.insert(tk.END, segment, (color_hex,))
                color_index += 1

        for tag in preview_text_widget.tag_names():
            if tag != "sel":  # Avoid re-configuring the default selection tag
                preview_text_widget.tag_config(tag, foreground=tag)

        preview_text_widget.config(state=tk.DISABLED, selectbackground="", selectforeground="")

    generate_button = ttk.Button(main_frame, text="Generate and Copy", command=generate_output)
    generate_button.grid(column=1, row=5, columnspan=3, pady=10)

    ttk.Label(main_frame, text="Output:").grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)
    output_text = tk.Text(main_frame, height=5, width=60, wrap="word")
    output_text.grid(column=0, row=6, columnspan=4, padx=5, pady=5, sticky=(tk.W, tk.E))

    preview_text_widget = tk.Text(main_frame, height=3, width=60, wrap="word", font=("Helvetica", 12, "bold"))
    preview_text_widget.grid(column=0, row=7, columnspan=4, padx=5, pady=5)
    preview_text_widget.config(state=tk.DISABLED, selectbackground=None, selectforeground=None)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        color1 = sys.argv[1]  # Start color
        color2 = sys.argv[2]  # End color
        text = sys.argv[3]    # Text input
        mid_colors = []
        i = 4
        while i < len(sys.argv):
            mid_colors.append(sys.argv[i])
            i += 1
        result = generate_gradient_tags(color1, color2, text, color_mid_hexes=mid_colors)
        print(result)
    else:
        create_ui()
