__author__ = 'Alex'

from os import remove
from django import forms
from django.core.files import File
from django.db.models.fields.files import ImageField
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.template import RequestContext
from photos.models import *
##TODO DELETE PHOTOS FROM HARDRIVE NOT JUST DB *******DONE********
##TODO MULTIPLE UPLOADS *******DONE********
##TODO NICE FRONT END
##TODO DRAG AND DROP
##TODO RESTFUL API
##TODO ONLY OWNER CAN DELETE *******DONE********
@login_required
def index(request):
    photos = Photo.objects.filter(owner = request.user, album_id=None)
    albums = Album.objects.filter(owner = request.user)

    if request.method == 'POST':
        if 'uploadFile' in request.POST:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                for file in request.FILES.getlist('file'):
                    Photo(owner = request.user, pub_date = timezone.now(), photo = file, title = file.name ).save()
                return render_to_response('photos/index.html', {'photos': photos, "albums":albums},context_instance=RequestContext(request))
            else:
                error_message = "Please upload JPGS, GIFS, or PNG format only"
                form = UploadFileForm()
                return render_to_response('photos/index.html', {'form': form, 'photos': photos, "albums":albums, 'error_message': error_message},context_instance=RequestContext(request))
        elif 'uploadAlbum' in request.POST:
            form = AlbumForm(request.POST)
            if form.is_valid():
                Album(owner = request.user, title = request.POST['title']).save()
                return render_to_response('photos/index.html', {'photos': photos, "albums":albums,},context_instance=RequestContext(request))
            else:
                error_message = "Please input a proper album name"
                form = AlbumForm()
                return render_to_response('photos/index.html', {'form': form, 'photos': photos, "albums":albums, 'error_message': error_message},context_instance=RequestContext(request))
        elif 'deleteAlbum' in request.POST:
            album = Album.objects.get(pk = request.POST['delete'])
            if album.owner == request.user:
                album.delete()
            return render_to_response('photos/index.html', {'photos': photos, "albums":albums},context_instance=RequestContext(request))
        elif 'deletePhoto' in request.POST:
            photo = Photo.objects.get(pk = request.POST['delete'])
            if photo.owner == request.user:
                os.remove(photo.photo.path)
                photo.delete()
            return render_to_response('photos/index.html', {'photos': photos, "albums":albums},context_instance=RequestContext(request))
    else:
        form = UploadFileForm()
        formAlbum = AlbumForm()
        return render_to_response('photos/index.html', {'form': form,'formAlbum': formAlbum, 'photos': photos, "albums":albums},context_instance=RequestContext(request))

@login_required
def album(request, album_id):
    albumSelected = get_object_or_404(Album, pk=album_id)
    photos = Photo.objects.filter(owner = request.user).exclude(album__isnull=False)
    albumPhotos = Photo.objects.filter(owner = request.user, album_id = albumSelected)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist('file'):
                Photo(owner = request.user, pub_date = timezone.now(), photo = file, title = file.name ).save()
            return render_to_response('album/index.html', {'form': form, 'albumNumber': albumSelected, 'photos': photos, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))
        elif 'delete' in request.POST:
            if photo.owner == request.user:
                photo = Photo(pk = request.POST['delete'])
                photo.delete()
            return render_to_response('album/index.html', {'albumNumber': albumSelected, 'photos': photos, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))
        elif 'addAlbum' in request.POST:
            photo = Photo.objects.filter(pk = request.POST['addAlbum']).update(album = albumSelected)
            return render_to_response('album/index.html', {'albumNumber': albumSelected, 'photos': photos, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))
        else:
            error_message = "Please input a proper album name"
            form = AlbumForm()
            return render_to_response('album/index.html', {'albumNumber': albumSelected, 'error_message': error_message, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))
    else:
        return render_to_response('album/index.html', {'photos': photos, 'albumSelected': albumSelected, 'albumPhotos':albumPhotos},context_instance=RequestContext(request))