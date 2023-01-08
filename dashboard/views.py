
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .functions import *

# local imports 
from .forms import ProfileForm, ProfileImageForm
from .models import Blog,Profile,BlogSection

# Create your views here.

@login_required
def dashboard(request):
    empty_blog = []
    completed_blogs = []
    monthCount = 0

    blogs = Blog.objects.filter(profile=request.user.profile)
    for blog in blogs:
        sections = BlogSection.objects.filter(blog=blog)
        if sections.exists():
            # Calculate blog words
            blogWords = 0
            for section in sections:
                section.save()
                blogWords += int(section.word_count)
                monthCount += int(section.word_count)
            blog.word_count = str(blogWords)
            blog.save()

            # blog.words = len(blog.title.split(' '))
            completed_blogs.append(blog)
        else:
            empty_blog.append(blog)

    timeSaved = monthCount/60
    
    context = {}
    context['empty_blog']= empty_blog[:10] 
    context['completed_blogs'] = completed_blogs 
    context['numBlogs'] = len(completed_blogs)
    context['monthCount'] = str(monthCount)
    context['timeSaved'] = int(timeSaved)
    context['countReset'] = '20th January 2023'
    return render(request, 'dashboard/index.html', context=context)

@login_required
def profile(request):
    context = {}
    profile = request.user


    if request.method == 'GET':
        form  = ProfileForm(instance=request.user.profile, user = request.user)
        image_form = ProfileImageForm(instance=request.user.profile)
        context['form'] = form
        context['image_form'] = image_form

        return render(request, 'dashboard/profile.html', context)

    if request.method == 'POST':
        form  =  ProfileForm(request.POST, instance=request.user.profile, user = request.user)
        image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
 

        if form.is_valid():
            form.save()
            return redirect('profile')
        if image_form.is_valid():
            image_form.save()
            return redirect('profile')


    # form = ProfileForm()

    

    
    return render(request, 'dashboard/profile.html', context=context)

@login_required
def blog_topic_generator(request):
    context = {}

    if request.method == 'POST':
        blog_topic = request.POST['blog_idea']   
        request.session['blog_idea'] = blog_topic


        blog_keyword = request.POST['blog_keyword']
        request.session['blog_keyword'] = blog_keyword


        audience = request.POST['audience']
        request.session['audience'] = audience

        blogTopics = generate_blog_topic(topic=blog_topic, keywords=blog_keyword, audience=audience)
        if len(blogTopics) > 0:
            request.session['blogTopics'] = blogTopics
            return redirect('blog_section')
        else:
            messages.error(request, "Sorry, we couldn't generate blog ideas! Try Again!!!")
            return redirect('blog_topic_generator')
        # print('Valid')
        # print(request.POST['blog_keyword'])

    return render(request, 'dashboard/topic_generator.html', context=context)

@login_required
def blog_sections(request):
    

    if 'blogTopics' in request.session:
        pass
    else:
        messages.error(request, "Start by creating blog topic ideas")
        return redirect('blog_topic_generator')

    context = {}
    context['blogTopics'] = request.session['blogTopics']


    return render(request, 'dashboard/blog-section.html', context=context)

@login_required
def save_topic(request, blogTopic):
    if 'blog_idea' in request.session and 'blog_keyword' in request.session and 'audience' in request.session and 'blogTopics' in request.session:  
        blog = Blog.objects.create(
            title = blogTopic,
            blogIdea = request.session['blog_idea'] ,  
            audience = request.session['audience'] ,
            keyword = request.session['blog_keyword'] ,
            profile = request.user.profile
        )
        blog.save()
        
        blogTopics = request.session['blogTopics'] 
        blogTopics.remove(blogTopic)
        request.session['blogTopics'] = blogTopics

        return redirect('blog_section')
    
    else:
        return redirect('blog_topic_generator')

@login_required
def use_topic(request, blogTopic):

    
    context = {}

    if 'blog_idea' in request.session and 'blog_keyword' in request.session and 'audience' in request.session:
        blog = Blog.objects.create(
            title = blogTopic,
            blogIdea = request.session['blog_idea'] ,  
            audience = request.session['audience'] ,
            keyword = request.session['blog_keyword'] ,
            profile = request.user.profile
        )
        blog.save()

        blog_sections = generate_blog_section_titles(topic=blogTopic, keywords=request.session['blog_keyword'], audience=request.session['audience'])

    else:
        return redirect('blog_topic_generator')
    
    if len(blog_sections) > 0:

        # We are adding sections to the session
        request.session['blog_sections'] = blog_sections

        # Adding the sections to the context
        context['blogSections'] = blog_sections
        # return redirect('select_blog_section')
    else:
        messages.error(request, "Sorry, we couldn't generate blog ideas! Try Again!!!")
        return redirect('blog_topic_generator')

    
    if request.method == "POST":
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:
                print(val)

                # Generating the blog section details 
                section = generate_blog_section_details(blogTopic=blogTopic, sectionTopic=val, audience=request.session['audience'], keywords=request.session['blog_keyword'])

                #Create Database Record
                blogSec = BlogSection.objects.create(
                    title = val,
                    body = section,
                    blog = blog)
                blogSec.save()
        
        return redirect('view_generated_blog', slug=blog.slug)


    return render(request, 'dashboard/select-blog-section.html', context=context)

@login_required
def view_generated_blog(request, slug):
    try:   
        blog=Blog.objects.get(slug=slug)
    except:
        messages.error(request, "Something went wrong!!! Try Again!!!")
        return redirect('blog_topic_generator')
    
    #Fetch the created sections for the blog
    blogSections = BlogSection.objects.filter(blog=blog)
    context = {}
    context['blog'] = blog
    context['blogSections'] = blogSections

    return render(request, 'dashboard/view_generated_blog.html', context=context)


@login_required
def delete_blog_topic(request, uniqueId):
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
        if blog.profile == request.user.profile:
            blog.delete()
            return redirect('dashboard')
        else:
            messages.error(request, "Some error occured!!")
            return redirect('dashboard')

    except:
        messages.error(request, "Blog not found!!")
        return redirect('dashboard')




@login_required
def createBlogFromTopic(request, uniqueId):

    context = {}

    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
    except:
        messages.error(request, "Blog not found!!")
        return redirect('dashboard')

    blog_sections = generate_blog_section_titles(topic=blog.title, keywords=blog.keyword, audience=blog.audience)

    
    
    if len(blog_sections) > 0:

        # We are adding sections to the session
        request.session['blog_sections'] = blog_sections

        # Adding the sections to the context
        context['blogSections'] = blog_sections
        # return redirect('select_blog_section')
    else:
        messages.error(request, "Sorry, we couldn't generate blog ideas! Try Again!!!")
        return redirect('blog_topic_generator')

    
    if request.method == "POST":
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:
                print(val)

                # Generating the blog section details 
                section = generate_blog_section_details(blogTopic=blog.title, sectionTopic=val, audience=blog.audience, keywords=blog.keyword)

                #Create Database Record
                blogSec = BlogSection.objects.create(
                    title = val,
                    body = section,
                    blog = blog)
                blogSec.save()
        
        return redirect('view_generated_blog', slug=blog.slug)


    return render(request, 'dashboard/select-blog-section.html', context=context)