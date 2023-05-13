import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad
from users.models import User


def root(request):
    return JsonResponse({
        "status": "ok"
    })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data.get('name'),
        )

        return JsonResponse({
            "id": category.pk,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for category in self.object_list.order_by('name'):
            response.append({
                "id": category.pk,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)
        self.object.name = category_data.get('name')

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        author = get_object_or_404(User, pk=ad_data.pop('author_id'))
        category = get_object_or_404(Category, pk=ad_data.pop('category_id'))
        ad = Ad.objects.create(author=author, category=category, **ad_data)

        return JsonResponse({
            'id': ad.pk,
            'name': ad.name,
            'price': ad.price,
            'author': ad.author.username,
            'description': ad.description,
            'category': ad.category.name,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None

        })


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    ads_on_page = 10

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list.order_by('-price'), self.ads_on_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = []
        for ad in page_obj:
            response.append({'total': paginator.count,
                             'total_page': paginator.num_pages,
                             'items': [{
                                 'id': ad.id,
                                 'name': ad.name,
                                 'author': ad.author.username,
                                 'price': ad.price,
                                 'description': ad.description,
                                 'category': ad.category.name,
                                 'is_published': ad.is_published,
                                 'image': ad.image.url if ad.image else None
                             }]})

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "category": ad.category.name,
            "is_published": ad.is_published,
            'image': ad.image.url if ad.image else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        if 'name' in ad_data:
            self.object.name = ad_data.get('name')
        if 'description' in ad_data:
            self.object.description = ad_data.get('description')
        if 'price' in ad_data:
            self.object.price = ad_data.get('price')
        if 'category_id' in ad_data:
            category = get_object_or_404(Category, pk=ad_data.get('category_id'))
            self.object.category = category

        return JsonResponse({
            'id': self.object.pk,
            'name': self.object.name,
            'price': self.object.price,
            'author': self.object.author.username,
            'description': self.object.description,
            'category': self.object.category.name,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse({
            'id': self.object.pk,
            'name': self.object.name,
            'price': self.object.price,
            'author': self.object.author.username,
            'description': self.object.description,
            'category': self.object.category.name,
            'is_published': self.object.is_published,
            'image': self.object.image.url
        })
