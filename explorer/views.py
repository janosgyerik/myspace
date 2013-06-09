import os

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse

CONTENT_ROOT = settings.CONTENT_ROOT
CONTENT_WWWROOT = settings.CONTENT_WWWROOT

MESSAGEFILE = 'message.md'
SPECIALFILES = (MESSAGEFILE,)


@login_required
def folder(request, relpath=None):
    if relpath:
        return folder_for_relpath(request, relpath)
    else:
        return folder_home(request)


class InvalidRelpathError:
    pass


def folder_common(request, relpath=None, name='Home', breadcrumbs={}, dirs={}, files={}, error=None, template='explorer/folder.html'):
    message = get_message(relpath)
    return render_to_response(template, {
        "name": name,
        "breadcrumbs": breadcrumbs,
        "dirs": dirs,
        "files": files,
        "error": error,
        "message": message,
        }, RequestContext(request))


def folder_home(request):
    breadcrumbs = get_breadcrumbs()
    (dirs, files) = get_dirs_and_files()
    return folder_common(
            request,
            breadcrumbs=breadcrumbs,
            dirs=dirs,
            files=files,
            )


def folder_for_relpath(request, relpath):
    name = os.path.basename(relpath)
    name = slug_to_name(name)
    breadcrumbs = get_breadcrumbs(relpath)
    try:
        (dirs, files) = get_dirs_and_files(relpath)
        error = None
    except InvalidRelpathError:
        dirs = ()
        files = ()
        error = 'Path does not exist: %s' % relpath

    return folder_common(
            request,
            relpath=relpath,
            name=name,
            breadcrumbs=breadcrumbs,
            dirs=dirs,
            files=files,
            error=error,
            )


def slug_to_name(slug):
    return slug.replace('-', ' ').title()


def get_breadcrumbs(relpath=None):
    wwwroot = reverse(folder, args=('',))

    breadcrumbs = []
    head = relpath
    while head:
        (head, tail) = os.path.split(head)
        name = slug_to_name(tail)
        href = os.path.join(wwwroot, head, tail)

        item = {
                "name": name,
                "href": href,
                }
        breadcrumbs.append(item)

    breadcrumbs.reverse()

    return breadcrumbs


def get_dirs_and_files(relpath=None):
    if relpath:
        basepath = os.path.join(CONTENT_ROOT, relpath)
        if not os.path.isdir(basepath):
            raise InvalidRelpathError
    else:
        basepath = CONTENT_ROOT

    dirs = []
    files = []
    for item in os.listdir(basepath):
        if item.startswith('.'):
            continue
        if item in SPECIALFILES:
            continue

        path = os.path.join(basepath, item)
        if os.path.exists(path):
            info = {}

            if os.path.isfile(path):
                info['name'] = item
                info['size'] = os.path.getsize(path)
                if relpath:
                    href = os.path.join(CONTENT_WWWROOT, relpath, item)
                else:
                    href = os.path.join(CONTENT_WWWROOT, item)
                info['href'] = href
                files.append(info)
            elif os.path.isdir(path):
                info['name'] = slug_to_name(item)
                if relpath:
                    args = (os.path.join(relpath, item),)
                else:
                    args = (item,)
                info['href'] = reverse(folder, args=args)
                dirs.append(info)

    dirs = sorted(dirs, key=lambda x: x['name'])
    files = sorted(files, key=lambda x: x['name'])

    return (dirs, files)


def get_message(relpath=None):
    if relpath:
        path = os.path.join(CONTENT_ROOT, relpath, MESSAGEFILE)
    else:
        path = os.path.join(CONTENT_ROOT, MESSAGEFILE)

    message = None
    if os.path.isfile(path):
        with open(path) as fh:
            message = '\n'.join(fh.readlines())

    return message
