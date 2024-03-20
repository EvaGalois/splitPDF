import os
import PyPDF2
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QIcon

class PDFSplitter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('GaloisSplitPdf')
        self.setWindowIcon(QIcon('icon.ico'))
        layout = QVBoxLayout()

        self.label_path = QLabel('选择PDF文件:')
        layout.addWidget(self.label_path)

        self.entry_path = QLineEdit(self)
        layout.addWidget(self.entry_path)

        self.button_browse_pdf = QPushButton('浏览', self)
        self.button_browse_pdf.clicked.connect(self.browsePDF)
        layout.addWidget(self.button_browse_pdf)

        self.label_output = QLabel('输出文件夹:')
        layout.addWidget(self.label_output)

        self.entry_output = QLineEdit(self)
        layout.addWidget(self.entry_output)

        self.button_browse_output = QPushButton('选择输出目录', self)
        self.button_browse_output.clicked.connect(self.browseOutputFolder)
        layout.addWidget(self.button_browse_output)

        self.range_layout = QHBoxLayout()

        self.label_start = QLabel('起始页:')
        self.range_layout.addWidget(self.label_start)

        self.start_page_entry = QLineEdit(self)
        self.range_layout.addWidget(self.start_page_entry)

        self.label_end = QLabel('终止页:')
        self.range_layout.addWidget(self.label_end)

        self.end_page_entry = QLineEdit(self)
        self.range_layout.addWidget(self.end_page_entry)

        layout.addLayout(self.range_layout)

        self.split_button = QPushButton('拆分', self)
        self.split_button.clicked.connect(self.splitPDF)
        layout.addWidget(self.split_button)

        self.merge_button = QPushButton('合并', self)
        self.merge_button.clicked.connect(self.mergePDF)
        layout.addWidget(self.merge_button)

        self.setLayout(layout)

    def browsePDF(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, '选择PDF文件', '', 'PDF Files (*.pdf);;All Files (*)', options=options)
        if filepath:
            self.entry_path.setText(filepath)

    def browseOutputFolder(self):
        options = QFileDialog.Options()
        folderpath = QFileDialog.getExistingDirectory(self, '选择输出目录', options=options)
        if folderpath:
            self.entry_output.setText(folderpath)

    def splitPDF(self):
        input_pdf_path = self.entry_path.text()
        output_folder = self.entry_output.text()

        if input_pdf_path and output_folder:
            try:
                os.makedirs(output_folder, exist_ok=True)
                with open(input_pdf_path, 'rb') as input_file:
                    pdf_reader = PyPDF2.PdfReader(input_file)

                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer = PyPDF2.PdfWriter()
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                        output_pdf_path = os.path.join(output_folder, f'page_{page_num + 1}.pdf')

                        with open(output_pdf_path, 'wb') as output_file:
                            pdf_writer.write(output_file)
                print('PDF拆分完成！')
            except Exception as e:
                print(f'错误：{str(e)}')
        else:
            print('请输入有效的PDF文件和输出文件夹路径。')

    def mergePDF(self):
        input_pdf_path = self.entry_path.text()
        output_folder = self.entry_output.text()
        start_page_text = self.start_page_entry.text()
        end_page_text = self.end_page_entry.text()

        if not input_pdf_path or not output_folder or not start_page_text or not end_page_text:
            print('请输入有效的PDF文件、输出文件夹路径，以及起始页和终止页。')
            return

        try:
            start_page = int(start_page_text)
            end_page = int(end_page_text)

            with open(input_pdf_path, 'rb') as input_file:
                pdf_reader = PyPDF2.PdfReader(input_file)
                total_pages = len(pdf_reader.pages)

                if start_page < 1 or end_page > total_pages:
                    print(f'错误：起始页和终止页必须在1到{total_pages}的范围内。')
                    return

                if start_page > end_page:
                    print('错误：起始页不能大于终止页。')
                    return

                os.makedirs(output_folder, exist_ok=True)
                pdf_writer = PyPDF2.PdfWriter()

                for page_num in range(start_page - 1, end_page):
                    pdf_writer.add_page(pdf_reader.pages[page_num])

                output_pdf_path = os.path.join(output_folder, 'merged.pdf')

                with open(output_pdf_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                print('PDF合并完成！')

        except ValueError:
            print('错误：起始页和终止页必须是有效的整数。')

        except Exception as e:
            print(f'错误：{str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFSplitter()
    window.show()
    sys.exit(app.exec_())
