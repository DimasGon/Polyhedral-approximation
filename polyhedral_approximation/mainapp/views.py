from django.shortcuts import render
from django.views.generic import View
from .forms import InputForm
from .models import DataModel
import os
from .laba import solve

class MainView(View):

    template_name = 'mainapp/main.html'

    def move_file(self, filename):
        root_dir = os.path.abspath(os.curdir)
        try:
            os.remove(root_dir + f'\common_static\img\{filename}')
        except Exception:
            pass
        try:
            os.rename(root_dir + f'\{filename}', root_dir + f'\common_static\img\{filename}')
        except Exception:
            pass

    def get(self, request):
        form = InputForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if 'phi1' in request.POST:
            form = InputForm(request.POST)
            if form.is_valid():
                phi1 = float(form.cleaned_data['phi1'])
                phi2 = float(form.cleaned_data['phi2'])
                phi3 = float(form.cleaned_data['phi3'])
                DataModel.objects.all().delete()
                phi_list = [phi1, phi2, phi3]
                for i in phi_list:
                    DataModel(phi=i).save()
                _, points_x_y = solve(phi_list, target='Start approximation')
            else:
                return render(request, self.template_name, {'form': form})
        else:
            phi_list = [i.phi for i in DataModel.objects.all()]
            new_phi, points_x_y = solve(phi_list)
            DataModel(phi=new_phi).save()
        self.move_file('graph.png')
        return render(request, self.template_name, {
            'graph': True, 'points': points_x_y
        })