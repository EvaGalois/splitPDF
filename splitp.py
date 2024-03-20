import os
import PyPDF2

def split_pdf(input_pdf_path, output_folder):
    # 创建输出目录
    os.makedirs(output_folder, exist_ok=True)
    
    with open(input_pdf_path, 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])
            
            output_pdf_path = f'{output_folder}/page_{page_num + 1}.pdf'
            
            with open(output_pdf_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            print(f'Page {page_num + 1} extracted and saved as {output_pdf_path}')

# Example usage
input_pdf_path = 'F3202.pdf'  # 指定输入的PDF文件路径
output_folder = 'output_pages'  # 指定保存单页PDF文件的文件夹路径

split_pdf(input_pdf_path, output_folder)
