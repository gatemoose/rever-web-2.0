from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from .Rever import Rever
import markdown
from weasyprint import HTML
# from io import BytesIO

def index(request):
    return render(request, 'index.html', {'name' : 'John Doe'})

def store(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        file = request.FILES.get('file')

        fs = FileSystemStorage(location=os.path.join('api', 'files'))
        filename = fs.save(file.name, file)

        input_path = str(os.getenv('PWD')) + '/api/files/' + filename
        output_path = str(os.getenv('PWD')) + '/api/files/COMPRESSED-' + filename

        rever = Rever()
        compress_ok = rever.compress(input_path, output_path, crf=28)

        response_ok = markdown.markdown(rever.analyze(output_path, prompt=prompt))

        os.remove(input_path)

        context = {
            'compression': compress_ok,
            'ai_response': response_ok,
            'filename': filename,
            'input': input_path,
            'output': output_path,
            'path': str(os.getenv('PWD'))
        }
        return render(request, 'index.html', context)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def download(request):
    markdown_text = request.POST.get('ai_response')

    html_content = markdown.markdown(markdown_text)

    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resposta.pdf"'

    return response