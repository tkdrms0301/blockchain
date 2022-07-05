import ctypes
from PyPDF2 import PdfFileReader, PdfFileWriter

pdfReader = PdfFileReader("./pdf/test.pdf", "rb")
print(id(pdfReader))
print(ctypes.cast(id(pdfReader), ctypes.py_object).value)
# step3.새로 만들 pdf 객체 생성
pdfWriter = PdfFileWriter()

# step5.1번 페이지가 붙여진 새로운 pdf 파일을 현재 경로('./')에 원하는 이름으로 저장
pdfWriter.addPage(pdfReader.getPage(0))
pdfWriter.write(open("./pdf/test_copy.pdf", "wb"))