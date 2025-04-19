import win32com.client
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches
import io
from PIL import Image
from html2docx import html2docx


def save_content_as_word(content, word_file_path):
    """
    将 HTML 内容转换为 Word 并保存到指定路径
    :param content: HTML 格式的字符串
    :param word_file_path: 保存 .docx 文件的路径
    """
    # 将 HTML 转换为字节流
    buf = html2docx(content, title="My Document")

    # 将字节流写入文件
    with open(word_file_path, "wb") as docx_file:
        docx_file.write(buf.getvalue())
def word_to_pdf(word_file, pdf_file):
    # 尝试使用 WPS Office 进行文件转换
    wps = win32com.client.Dispatch("Kwps.Application")
    wps.Visible = False  # 不显示 WPS 应用界面
    doc = wps.Documents.Open(word_file)  # 打开 Word 文件
    doc.SaveAs(pdf_file, FileFormat=17)  # 17 是保存为 PDF 格式
    doc.Close()  # 关闭文件
    wps.Quit()  # 退出 WPS 应用
from pdf2docx import Converter

def pdf_to_word(pdf_file, word_file):
    # 使用 pdf2docx 转换器
    cv = Converter(pdf_file)
    cv.convert(word_file, start=0, end=None)  # 转换整个文档
    cv.close()
# 示例调用
# word_to_pdf(r"F:\danzi\DocxXieTong\1.docx", "F:\danzi\DocxXieTong\output.pdf")
