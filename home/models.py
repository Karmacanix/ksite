from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.shortcuts import redirect, render

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import Tag, TaggedItemBase

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index


class StandardPageTag(TaggedItemBase):
    """
    This model allows us to create a many-to-many relationship between
    the StandardPage object and tags. There's a longer guide on using it at
    http://docs.wagtail.io/en/latest/reference/pages/model_recipes.html#tagging
    """
    content_object = ParentalKey('StandardPage', related_name='tagged_items')


class StandardPage(Page):
    """
    A Standard Page
    """
    introduction = RichTextField(blank=True)
    body = RichTextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = ClusterTaggableManager(through=StandardPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        FieldPanel('body', classname="full"),
        FieldPanel('tags'),
    ]

    @property
    def get_tags(self):
        """
        Return all the tags that are related to the post into a list we can access on the template.
        We're additionally adding a URL to access StandardPage objects with that tag
        """
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/'+'/'.join(s.strip('/') for s in [
                'home',
                'tags',
                tag.slug
            ])
        return tags

    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ['HomePage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []


class HomePage(RoutablePageMixin, Page):
    """
    Home page for standard pages.
    We need to alter the page model's context to return the child page objects,
    the StandardPage objects, so that it works as an index page
    RoutablePageMixin is used to allow for a custom sub-URL for the tag views
    defined above.
    """
    tag_line = models.CharField(max_length=148)

    content_panels = Page.content_panels + [
        FieldPanel('tag_line', classname="full"),
    ]

    # Speficies that only StandardPage objects can live under the home page
    subpage_types = ['StandardPage']

    # Defines a method to access the children of the page (e.g. StandardPage objects). 
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    def get_context(self, request):
        # Get posts
        posts = StandardPage.objects.descendant_of(self).live().order_by('-updated')
        latest_posts = StandardPage.objects.descendant_of(self).live().order_by('-updated')
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(posts, 3)  # Show 3 posts per page
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = super(HomePage, self).get_context(request)
        context['posts'] = posts
        context['latest_posts'] = latest_posts
        return context

    # This defines a Custom view that utilizes Tags. This view will return all
    # related StandardPages for a given Tag or redirect back to the HomePage.
    # More information on RoutablePages is at
    # http://docs.wagtail.io/en/latest/reference/contrib/routablepage.html
    @route('^home/tags/$', name='tag_archive')
    @route('^home/tags/(\w+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'home/home_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child StandardPage objects for this HomePage.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = StandardPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # Returns the list of Tags for all child posts of this StandardPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags