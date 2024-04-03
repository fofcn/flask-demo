import fitz  # fitz模块就是PyMuPDF


if __name__ == '__main__':
    pdf = fitz.open()  
    imgfile = "Picture5.png"  
    img = fitz.open(imgfile) 
    rect = img[0].rect  # 获取图片大小
    pdfbytes = img.convert_to_pdf()  # 使用图片创建一个PDF
    img.close()
    imgPDF = fitz.open("pdf", pdfbytes)  # 打开图片流，将PDF数据存入
    pdf.insert_pdf(imgPDF)  # 将图片流插入爱你PDF
    output_pdf_path = "output.pdf"  # 输出PDF的路径
    pdf.save(output_pdf_path)  
