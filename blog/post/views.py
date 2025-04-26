from django.shortcuts import render
from django.http import Http404
import os
from blog.settings import OBSIDIAN_VAULT_PATH
from .markdown_converter import ObsidianMarkdownConverter
from django.utils.text import slugify
import re
# Create your views here.

def post_list(request):
    try:
        filenames = [f for f in os.listdir(OBSIDIAN_VAULT_PATH) if f.endswith('.md')]
    except FileNotFoundError:
        return render(request, 'post/error.html', {'error_message': 'Vault folder not found.'})

    posts = []
    for filename in filenames:
        name_without_ext = filename[:-3]  # remove .md
        posts.append({
            'title': name_without_ext,
            'slug': slugify(name_without_ext)
        })

    return render(request, 'post/post_list.html', {'posts': posts})


def post_detail(request, slug):
    converter = ObsidianMarkdownConverter()

    # Reverse slug back to filename
    filenames = [f for f in os.listdir(OBSIDIAN_VAULT_PATH) if f.endswith('.md')]
    target_file = None
    for filename in filenames:
        name_without_ext = filename[:-3]  # Remove the .md extension
        if slugify(name_without_ext) == slug:
            target_file = filename
            break

    if not target_file:
        raise Http404("Post not found.")

    file_path = os.path.join(OBSIDIAN_VAULT_PATH, target_file)

    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Use the filename (without .md) as the title
    title = target_file[:-3].replace('-', ' ').title()

    # Convert markdown to HTML
    html_content = converter.convert(md_content)

    return render(request, 'post/post_detail.html', {
        'html_content': html_content,
        'title': title,
    })

