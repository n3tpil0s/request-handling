from datetime import datetime as dt
import os
from .settings import FILES_PATH
from django.shortcuts import render_to_response
from django.views.generic import TemplateView



class FileList(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, date:"Date as string"=None, **kwargs) -> "context for template":
        context = super().get_context_data(**kwargs)
        server_files = []
        for file in os.listdir(FILES_PATH):
            file_stats = os.stat(os.path.join(FILES_PATH, file))
            file_info = {
                'name': file,
                'ctime': dt.fromtimestamp(file_stats.st_ctime),
                'mtime': dt.fromtimestamp(file_stats.st_mtime),
            }

            if date == None or date[:10] == dt.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d") \
             or date[:10] == dt.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d"):
                server_files.append(file_info)

        context.update({
            'files': server_files,
            'date': date  # Этот параметр необязательный
        })
        return context


def file_content(request, name):
    files = os.listdir(FILES_PATH)
    if name in files:
        with open(os.path.join(FILES_PATH, name), encoding='utf8') as f:
            f_content = f.read()
    else:
        f_content = 'File not found'

    return render_to_response(
        'file_content.html',
        context={'file_name': name, 'file_content': f_content}
)
