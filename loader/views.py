import os

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Upload, UploadStats, SizeChange, SizeChangeStats
from .forms import UploadForm, SizeChangeForm
from .scripts import resize, make_gif, add_gif_to_db, translate_color, cut_size
from hdick.settings import BASE_DIR, STATICFILES_DIRS


def index(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('upload')
        name = request.POST.get('output_name')
        request.session['name'] = name
        basewidth = request.POST.get('base_width')
        color_raw = request.POST.get('color')
        colour = translate_color(color_raw)
        speed = request.POST.get('speed')
        source = name+'.gif'

        if form.is_valid():
            for file in files:
                Upload.objects.create(upload=file, output_name=name, base_width=basewidth,
                                      color=colour, speed=speed)
            uploads = Upload.objects.filter(output_name=name, base_width=basewidth, speed=speed)

            # process images size/color
            try:
                filenames = []
                for i in uploads:
                    resize(str(i.upload), int(basewidth), colour)
                    filenames.append(str(i.upload))
            except FileNotFoundError:
                return render(request, 'loader/fail.html')
            else:
                # creates gif out of processed images
                make_gif(filenames, source, float(speed))
                # makes file class out of gif
                django_file = add_gif_to_db(source)
                # adds gif file class to loader.db + info for stats.db
                Upload.objects.create(upload=django_file, output_name=name+'.gif')
                UploadStats.objects.create(name=name, number_of_files=len(filenames),
                                     sourceurl=source, width_size=basewidth,
                                     frames=speed)

                return HttpResponseRedirect(reverse('loader:showall'))
        else:
            form = UploadForm()
            return render(request, 'loader/index.html', {'form': form})

    else:
        form = UploadForm()
        return render(request, 'loader/index.html', {'form': form})


# if jpg-gif conversion is successful, this view returns gif image
def show_all(request):
    name = request.session.get('name')
    uploads = Upload.objects.filter(output_name=name)
    gif = Upload.objects.filter(output_name=name+'.gif')
    gif_address = os.path.join(BASE_DIR, STATICFILES_DIRS[0] + name + '.gif')
    try:
        context = {'gif': gif_address}
    except AttributeError:
        form = UploadForm()
        return render(request, 'loader/index.html', {'form': form})

    else:
        # cleans files/database entries that are no longer needed
        for i in uploads:
            os.remove(str(i.upload))
        uploads.delete()
        gif.delete()
    return render(request, 'loader/showall.html', context)


def drop_size(request):
    if request.method == 'POST':
        size_form = SizeChangeForm(request.POST, request.FILES)
        size_name = request.POST.get('size_name')
        new_size = int(request.POST.get('new_size'))

        if size_form.is_valid():
            size_form.save()
            filefilter = SizeChange.objects.filter(size_name=size_name, new_size=new_size)
            extension = str(filefilter[0].size_file)[-4:]
            file = os.path.join(BASE_DIR, str(filefilter[0].size_file))
            # file size before processing
            old_size = os.stat(file).st_size
            # desired file size
            new_size = new_size*1000

            # checks if desired file size is smaller than size before processing
            if old_size <= new_size:
                size_form = SizeChangeForm()
                text = 'ERROR: Your new size must be smaller, than old one.'
                context = {'size_form': size_form, 'text': text}
                return render(request, 'loader/drop_size.html', context)

            else:
                # limits image to new file size, and cleans unnecessary files/db entries
                new_stat_size, output_file = cut_size(file, old_size, new_size, size_name,
                                                      extension)
                # adds info to  db stat table
                SizeChangeStats.objects.create(size_stat_name=size_name, old_stat_size=old_size,
                                                new_stat_size=new_stat_size,
                                               output_file_path=output_file)
                request.session['size_name'] = size_name
                request.session['extension'] = extension
                return HttpResponseRedirect(reverse('loader:drop_success'))

        else:
            size_form = SizeChangeForm()
            text = 'Choose JPG file and reduce its size.'
            context = {'size_form': size_form, 'text': text}
            return render(request, 'loader/drop_size.html', context)

    else:
        size_form = SizeChangeForm()
        text = 'Choose JPG file and reduce its size.'
        context = {'size_form': size_form, 'text': text}
        return render(request, 'loader/drop_size.html', context)


# if filesize change is successful this view returns link to new image
def drop_success(request):
    size_name = request.session.get('size_name')
    extension = request.session.get('extension')
    output_file = STATICFILES_DIRS[0] + size_name + extension
    return render(request, 'loader/drop_success.html', {'output': output_file})


# in case of critical error,view cleans all db "working table" entries and helps app to recover
def fail(request):
    Upload.objects.all().delete()
    return render(request, 'loader/fail.html')


def contact(request):
    return render(request, 'loader/contact.html')