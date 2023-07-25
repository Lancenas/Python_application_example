from PIL import Image, ImageDraw, ImageFont
import os

DEFAULT_FONT_PATH = "/Library/Fonts/Microsoft/SimHei.ttf"  # Change this to your desired default font path

def get_font(font_size):
    default_font = ImageFont.load_default()
    custom_font_path = input(f"输入自定义字体路径（或按Enter使用默认值 {DEFAULT_FONT_PATH}): ")
    font_path = custom_font_path.strip() if custom_font_path.strip() else DEFAULT_FONT_PATH
    try:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, font_size)
    except (OSError, IOError, Image.DecompressionBombError, Image.UnidentifiedImageError):
        pass

    print(f"Font file not found at '{font_path}'. Using default font.")
    return default_font

def add_text_watermark(input_image, output_image, watermark_content,
                       font_size=50, opacity=0.5, angle=0, spacing=50):
    try:
        image = Image.open(input_image).convert("RGBA")
        width, height = image.size

        watermark_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark_image)
        font = get_font(font_size)
        textbbox = draw.textbbox((0, 0), watermark_content, font=font)

        # Calculate the number of rows and columns required to cover the image
        num_rows = (height + spacing) // (textbbox[3] - textbbox[1] + spacing)
        num_cols = (width + spacing) // (textbbox[2] - textbbox[0] + spacing)

        for row in range(num_rows):
            for col in range(num_cols):
                anchor_x = col * (textbbox[2] - textbbox[0] + spacing) + spacing // 2
                anchor_y = row * (textbbox[3] - textbbox[1] + spacing) + spacing // 2

                # Create a new ImageDraw object for the rotated text
                rotated_draw = ImageDraw.Draw(watermark_image)

                # Calculate the anchor point for rotation
                anchor_point = (anchor_x + (textbbox[2] - textbbox[0]) // 2, anchor_y + (textbbox[3] - textbbox[1]) // 2)

                # Rotate the text for the current grid cell
                rotated_text = Image.new("RGBA", (textbbox[2] - textbbox[0], textbbox[3] - textbbox[1]), (255, 255, 255, 0))
                text_draw = ImageDraw.Draw(rotated_text)
                text_draw.text((0, 0), watermark_content, fill=(255, 255, 255, int(255 * opacity)), font=font)

                rotated_text = rotated_text.rotate(angle, resample=Image.BICUBIC, expand=1)

                # Paste the rotated text onto the watermark image
                watermark_image.paste(rotated_text, anchor_point, rotated_text)

        watermarked_image = Image.alpha_composite(image, watermark_image)
        watermarked_image = watermarked_image.convert("RGB")  # Convert to RGB mode
        watermarked_image.save(output_image, format="JPEG", quality=95)

        print(f"Watermark added to {output_image}")

    except Exception as e:
        print(f"Error: {e}")

def add_image_watermark(input_image, output_image, watermark_image_path,
                        opacity=0.5, angle=0, spacing=50):
    try:
        image = Image.open(input_image).convert("RGBA")
        width, height = image.size

        watermark = Image.open(watermark_image_path).convert("RGBA")
        watermark_width, watermark_height = watermark.size

        watermark_image = Image.new("RGBA", image.size, (255, 255, 255, 0))

        # Calculate the number of rows and columns required to cover the image
        num_rows = (height + spacing) // (watermark_height + spacing)
        num_cols = (width + spacing) // (watermark_width + spacing)

        for row in range(num_rows):
            for col in range(num_cols):
                anchor_x = col * (watermark_width + spacing) + spacing // 2
                anchor_y = row * (watermark_height + spacing) + spacing // 2

                # Create a new rotated watermark image with adjusted opacity
                rotated_watermark = watermark.rotate(angle, resample=Image.BICUBIC, expand=1)
                watermark_with_opacity = Image.new("RGBA", rotated_watermark.size)
                for x in range(rotated_watermark.width):
                    for y in range(rotated_watermark.height):
                        r, g, b, a = rotated_watermark.getpixel((x, y))
                        watermark_with_opacity.putpixel((x, y), (r, g, b, int(a * opacity)))

                # Paste the rotated and opacity-adjusted watermark onto the watermark image
                watermark_image.paste(watermark_with_opacity, (anchor_x, anchor_y), watermark_with_opacity)

        watermarked_image = Image.alpha_composite(image, watermark_image)
        watermarked_image = watermarked_image.convert("RGB")  # Convert to RGB mode
        watermarked_image.save(output_image, format="JPEG", quality=95)

        print(f"Watermark added to {output_image}")

    except Exception as e:
        print(f"Error: {e}")

def batch_add_watermark(input_folder, output_folder, watermark_type, watermark_content, **kwargs):
    os.makedirs(output_folder, exist_ok=True)

    files = os.listdir(input_folder)
    for file in files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        if watermark_type == 'text':
            add_text_watermark(input_path, output_path, watermark_content, **kwargs)
        elif watermark_type == 'image':
            add_image_watermark(input_path, output_path, watermark_content, **kwargs)
        else:
            print("Unsupported watermark type. Use 'text' or 'image'.")

def get_numeric_input(prompt, data_type):
    while True:
        try:
            user_input = input(prompt)
            value = data_type(user_input)
            return value
        except ValueError:
            print("输入无效。请输入有效的数字值。")

def main():
    while True:
        print("请选择操作类型：")
        print("1 - 处理单个图片文件")
        print("2 - 批量处理图片文件夹")
        print("e - 退出进程")

        choice = input("请输入选择：")

        if choice == "1":
            input_file = input("请输入输入图片文件路径：")
            # 获取文件名和文件后缀名，使用 os.path.splitext 函数
            file_name, file_extension = os.path.splitext(input_file)

            # 将原始文件后缀替换为 "_watermark" 并加上新的后缀
            default_output_file = file_name + "_watermark" + file_extension

            output_file = input("请输入输出图片文件名（包含路径）（留空使用默认值：{}）：".format(default_output_file))
            if not output_file.strip():  # 检查用户输入是否为空
                output_file = default_output_file
            elif output_file.endswith("/"):
                # 处理用户输入的输出路径为目录的情况，使用 os.path.basename 获取原始文件名并替换为新的输出文件名
                output_file = os.path.join(output_file, os.path.basename(input_file).replace(file_extension, "_watermark" + file_extension))

            watermark_type = input("请输入水印类型（text/image）：")

            if watermark_type == "text":
                watermark_content = input("请输入水印文字内容 ：")
                font_size_input = input("请输入字体大小（留空使用预置值“16”）：")
                if not font_size_input.strip():  # Check if input is empty
                    font_size = 16
                else:
                    font_size = int(font_size_input)

                opacity_input = input("请输入水印透明度（0-1之间）（留空使用预置值“0.5”）：")
                if not opacity_input.strip():  # Check if input is empty
                    opacity = 0.5
                else:
                    opacity = float(opacity_input)

                angle_input = input("请输入水印旋转角度（0-360之间）（留空使用预置值“30”）：")
                if not angle_input.strip():  # Check if input is empty
                    angle = 30
                else:
                    angle = int(angle_input)

                spacing_input = input("请输入水印间距（留空使用预置值“50”）：")
                if not angle_input.strip():  # Check if input is empty
                    spacing = 50
                else:
                    spacing = int(spacing_input)

                if os.path.isfile(input_file):
                    add_text_watermark(input_file, output_file, watermark_content,
                                       font_size=font_size, opacity=opacity, angle=angle, spacing=spacing)
                else:
                    print("输入文件不存在。")

            elif watermark_type == "image":
                watermark_content = input("请输入水印图片路径：")
                opacity_input = input("请输入水印透明度（0-1之间）（留空使用预置值“0.5”）：")
                if not opacity_input.strip():  # Check if input is empty
                    opacity = 0.5
                else:
                    opacity = float(opacity_input)

                angle_input = input("请输入水印旋转角度（0-360之间）（留空使用预置值“30”）：")
                if not angle_input.strip():  # Check if input is empty
                    angle = 30
                else:
                    angle = int(angle_input)

                spacing_input = input("请输入水印间距（留空使用预置值“100”）：")
                if not angle_input.strip():  # Check if input is empty
                    spacing = 100
                else:
                    spacing = int(spacing_input)

                if os.path.isfile(input_file):
                    add_image_watermark(input_file, output_file, watermark_content,
                                        opacity=opacity, angle=angle, spacing=spacing)
                else:
                    print("输入文件不存在。")

            else:
                print("不支持的水印类型。请输入“text”或“image”。")

        elif choice == "2":
            input_folder = input("请输入输入图片文件夹路径：")
            output_folder = input("请输入输出图片文件夹路径：")
            # 输入水印类型
            watermark_type = input("请输入水印类型（text/image）：")

            if watermark_type == "text":
                watermark_content = input("请输入水印文字内容：")
                font_size_input = input("请输入字体大小（留空使用预置值“16”）：")
                if not font_size_input.strip():  # Check if input is empty
                    font_size = 16
                else:
                    font_size = int(font_size_input)

                opacity_input = input("请输入水印透明度（0-1之间）（留空使用预置值“0.5”）：")
                if not opacity_input.strip():  # Check if input is empty
                    opacity = 0.5
                else:
                    opacity = float(opacity_input)

                angle_input = input("请输入水印旋转角度（0-360之间）（留空使用预置值“30”）：")
                if not angle_input.strip():  # Check if input is empty
                    angle = 30
                else:
                    angle = int(angle_input)

                spacing_input = input("请输入水印间距（留空使用预置值“50”）：")
                if not angle_input.strip():  # Check if input is empty
                    spacing = 50
                else:
                    spacing = int(spacing_input)

                if os.path.isdir(input_folder):
                    batch_add_watermark(input_folder, output_folder, watermark_type, watermark_content,
                                        font_size=font_size, opacity=opacity, angle=angle, spacing=spacing)
                else:
                    print("输入文件夹不存在。")

            elif watermark_type == "image":
                watermark_content = input("请输入水印图片路径：")
                opacity_input = input("请输入水印透明度（0-1之间）（留空使用预置值“0.5”）：")
                if not opacity_input.strip():  # Check if input is empty
                    opacity = 0.5
                else:
                    opacity = float(opacity_input)

                angle_input = input("请输入水印旋转角度（0-360之间）（留空使用预置值“0”）：")
                if not angle_input.strip():  # Check if input is empty
                    angle = 0
                else:
                    angle = int(angle_input)

                spacing_input = input("请输入水印间距（留空使用预置值“100”）：")
                if not angle_input.strip():  # Check if input is empty
                    spacing = 100
                else:
                    spacing = int(spacing_input)

                if os.path.isdir(input_folder):
                    batch_add_watermark(input_folder, output_folder, watermark_type, watermark_content,
                                        opacity=opacity, angle=angle, spacing=spacing)
                else:
                    print("输入文件夹不存在。")

            else:
                print("不支持的水印类型。请输入“text”或“image”。")

        elif choice.lower() == "e":
            break

        else:
            print("无效选择。请重新输入。")

if __name__ == "__main__":
    main()
