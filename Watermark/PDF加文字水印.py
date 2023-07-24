import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def load_custom_font(font_path):
    try:
        pdfmetrics.registerFont(TTFont('CustomFont', font_path))
        return True
    except:
        print("不支持该字体，请重新输入！")
        return False

def add_text_watermark(input_pdf, output_pdf, watermark_text, font_path, font_size=50, opacity=0.5, rotation=45, x_spacing=150, y_spacing=150):
    # 加载自定义字体
    if not load_custom_font(font_path):
        return

    # 打开PDF文件
    pdf_reader = PyPDF2.PdfReader(input_pdf)
    pdf_writer = PyPDF2.PdfWriter()

    # 设置水印字体和大小
    c = canvas.Canvas("watermark_tmp.pdf", pagesize=letter)
    c.setFont('CustomFont', font_size)

    # 设置水印透明度
    c.setFillAlpha(opacity)

    # 在每个位置添加水印
    for x in range(0, int(c._pagesize[0]), x_spacing):
        for y in range(0, int(c._pagesize[1]), y_spacing):
            c.saveState()
            c.translate(x, y)
            c.rotate(rotation)
            c.drawString(0, 0, watermark_text)
            c.restoreState()

    c.save()

    # 打开水印PDF文件
    watermark_reader = PyPDF2.PdfReader("watermark_tmp.pdf")
    watermark_page = watermark_reader.pages[0]

    # 给每一页加上水印
    for page in pdf_reader.pages:
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    # 保存输出的PDF文件
    with open(output_pdf, "wb") as output_file:
        pdf_writer.write(output_file)

    # 关闭文件
    pdf_reader.stream.close()
    watermark_reader.stream.close()

    # 删除水印PDF文件
    os.remove("watermark_tmp.pdf")

if __name__ == "__main__":
    while True:
        # 输入文件名、水印文字、自定义字体路径以及其他参数
        input_pdf_filename = input("请输入输入PDF文件名（包含路径）：")
        default_output_pdf_filename = input_pdf_filename.replace(".pdf", "_watermark.pdf")

        output_pdf_filename = input("请输入输出PDF文件名（包含路径）（留空使用默认值：{}）：".format(default_output_pdf_filename))
        if not output_pdf_filename.strip():  # Check if input is empty
            output_pdf_filename = default_output_pdf_filename
        elif output_pdf_filename.endswith("/"):
            output_pdf_filename += input_pdf_filename.split("/")[-1].replace(".pdf", "_watermark.pdf")

        watermark_text = input("请输入水印文字（留空使用预置值“The is Watermark”）：")
        if not watermark_text.strip():  # Check if input is empty
            watermark_text = "The is Watermark"

        custom_font_path = input("请输入字体文件的路径（留空使用预置值“/Library/Fonts/Microsoft/SimHei.ttf”）：")
        if not custom_font_path.strip():  # Check if input is empty
            custom_font_path = "/Library/Fonts/Microsoft/SimHei.ttf"

        font_size_input = input("请输入字体大小（留空使用预置值“24”）：")
        if not font_size_input.strip():  # Check if input is empty
            font_size = 24
        else:
            font_size = int(font_size_input)

        opacity_input = input("请输入水印透明度（0-1之间）（留空使用预置值“0.2”）：")
        if not opacity_input.strip():  # Check if input is empty
            opacity = 0.2
        else:
            opacity = float(font_size_input)

        rotation_input = input("请输入水印旋转角度（0-360之间）（留空使用预置值“30”）：")
        if not rotation_input.strip():  # Check if input is empty
            rotation = 30
        else:
            rotation = int(font_size_input)

        x_spacing_input = input("请输入水印横向间距（留空使用预置值“150”）：")
        if not x_spacing_input.strip():  # Check if input is empty
            x_spacing = 150
        else:
            x_spacing = int(x_spacing_input)

        y_spacing_input = input("请输入水印纵向间距（留空使用预置值“150”）：")
        if not y_spacing_input.strip():  # Check if input is empty
            y_spacing = 150
        else:
            y_spacing = int(y_spacing_input)

        # 添加水印
        add_text_watermark(input_pdf_filename, output_pdf_filename, watermark_text, custom_font_path, font_size,
                           opacity, rotation, x_spacing, y_spacing)

        choice = input("是否继续添加水印？（输入 'e' 退出，输入其他任意键继续）：")
        if choice.lower() == 'e':
            break