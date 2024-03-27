# Open the PDF file in binary mode
import PyPDF2
import google.generativeai as genai

GOOGLE_API_KEY = 'AIzaSyAR6g2UxdgR2HTr97C70if354JKw7yjvBo'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

with open('Case1-Jhon.pdf', 'rb') as file:
    # Create a PDF file reader object
    reader = PyPDF2.PdfReader(file)

    text = ""
    # Loop through all the pages and extract text
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()

html_text = ""
response = model.generate_content(f''' Consider You are a Lawyer  Analyse this case report and You have to prove jhon as culprit give three main key points:
{text}
''')
print(response.text)
