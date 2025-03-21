from django.shortcuts import render#, redirect
from django.http import HttpResponse#, JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from .Rever import Rever
import markdown
from weasyprint import HTML
# from .models import Request, Response

model_name = 'gemini-2.0-pro-exp-02-05'

def index(request):
    return render(request, 'api/index.html', {'model_name': model_name})

def download(request):
    markdown_text = request.POST.get('ai_response')

    html_content = markdown.markdown(markdown_text)

    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resposta.pdf"'

    return response

def run(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        file = request.FILES.get('file')

        fs = FileSystemStorage(location=os.path.join('api', 'files'))
        filename = fs.save(file.name, file)

        input_path = str(os.getenv('PWD')) + '/api/files/' + filename
        output_path = str(os.getenv('PWD')) + '/api/files/COMPRESSED-' + filename

        rever = Rever()
        compress_ok = rever.compress(input_path, output_path, crf=28)
        response = rever.analyze(output_path, prompt=prompt, model_name=model_name)
        token_usage = response[1]
        response_ok = markdown.markdown(response[0])

        os.remove(input_path)

        context = {
            'ai_response': response_ok,
            'compression': compress_ok,
            'token_usage': token_usage,
            'filename': filename,
            'input': input_path,
            'output': output_path,
            'path': str(os.getenv('PWD')),
            'model_name': model_name
        }

        return render(request, 'api/index.html', context)