from colour import Color

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

def generate_gradient_tags(color1_hex, color2_hex, text):
    """Generates color tags for text based on a gradient between two hex colors."""
    color1_rgb = hex_to_rgb(color1_hex)
    color2_rgb = hex_to_rgb(color2_hex)
    
    gradient_tags = ""
    for i, char in enumerate(text):
        fraction = i / (len(text) - 1) if len(text) > 1 else 0  # Handle edge case for single-letter text
        interpolated_color = interpolate_color(color1_rgb, color2_rgb, fraction)
        color_hex = rgb_to_hex(interpolated_color)
        gradient_tags += f"<color={color_hex}>{char}</color>"
    
    return gradient_tags

# Example usage
color1 = "#FF5733"  # Start color
color2 = "#33B5FF"  # End color
text = "Gradient Text"

result = generate_gradient_tags(color1, color2, text)
print(result)