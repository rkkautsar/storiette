from django.db import models
from django.contrib.auth.models import User
from utils.models import BaseModel
from django.utils.functional import cached_property


class Category(BaseModel):
    parent = models.ForeignKey("self", related_name="children", null=True, blank=True, on_delete=models.CASCADE)
    name = models.TextField(max_length=255)

    @cached_property
    def full_name(self):
        name = self.name
        parent = self.parent
        while parent is not None:
            name = parent.name + " > " + name
            parent = parent.parent
        return name

    def __str__(self):
        return self.full_name


class Paragraph(BaseModel):
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, related_name="paragraphs", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.content


class Story(BaseModel):
    title = models.TextField(max_length=255)
    feature_image = models.URLField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, related_name="stories", on_delete=models.SET_NULL, null=True, blank=True)
    master = models.ForeignKey(User, related_name="stories", on_delete=models.SET_NULL, null=True, blank=True)
    origin = models.ForeignKey("self", related_name="forks", on_delete=models.SET_NULL, null=True, blank=True)
    paragraphs = models.ManyToManyField(Paragraph, through='StoryParagraph')

    @property
    def is_fork(self):
        return self.origin is not None

    def fork(self, master):
        story = Story(origin=self,
                      title=self.title,
                      feature_image=self.feature_image,
                      category=self.category,
                      master=master)
        story.save()
        story.paragraphs = self.paragraphs.all()
        return story


class StoryParagraph(BaseModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('story', 'paragraph'),)
