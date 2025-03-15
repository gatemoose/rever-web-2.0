from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from .Rever import Rever

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
        compress_ok = rever.compress(input_path, output_path)

        response_ok = rever.analyze(output_path, prompt=prompt)

        context = {
            'compression': compress_ok,
            'response': response_ok,
            'filename': filename,
            'input': input_path,
            'output': output_path,
            'path': str(os.getenv('PWD'))
        }

        return render(request, 'result.html', context)

        return JsonResponse({
            'compression': compress_ok,
            'response': response_ok,
            'filename': filename,
            'input': input_path,
            'output': output_path,
            'path': str(os.getenv('PWD'))
        })
    return JsonResponse({'error': 'Método não permitido'}, status=405)