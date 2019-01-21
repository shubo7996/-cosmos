from django import forms

from posts import models


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "cluster")
        model = models.Post

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["cluster"].queryset = (
                models.Cluster.objects.filter(
                    pk__in=user.clusters.values_list("cluster__pk")
                )
            )
