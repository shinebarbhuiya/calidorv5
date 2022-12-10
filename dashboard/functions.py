import os 
import openai
from django.conf import settings




openai.api_key = settings.OPENAI_API_KEYS



def generate_blog_topic(topic, keywords, audience):
    blog_topics = []

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"Generate 10 blog topic ideas on the given topic for the topic : {topic}\nAudience: {audience}\nStrictly don't use numbers in the list, use * to list titles\nKeywords: {keywords}\n*",
    temperature=0.8,
    max_tokens=500,
    top_p=1,
    best_of=1,
    frequency_penalty=0,
    presence_penalty=0
    )


    if 'choices' in response:
        if len(response['choices'])>0:
            res = response['choices'][0]['text']
        else:
            return []
    else:
        return []

    b_list = res.split('*')
    if len(b_list) > 0:
        for blog in b_list:
            blog_topics.append(blog)
    else:
        return []
    print(blog_topics)
    return blog_topics


def generate_blog_section_titles(topic, keywords, audience):
    blog_sections = []

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"Generate 10 adequate blog sections titles for the provided blog topic , audience and keywords:\nTopic: {topic}\nAudience:  {audience}\nStrictly don't use numbers in the list, use * to list titles\nKeywords: {keywords}\n*",
    temperature=0.8,
    max_tokens=500,
    top_p=1,
    best_of=1,
    frequency_penalty=0,
    presence_penalty=0
    )


    if 'choices' in response:
        if len(response['choices'])>0:
            res = response['choices'][0]['text']
        else:
            return []
    else:
        return []

    b_list = res.split('*')
    if len(b_list) > 0:
        for blog in b_list:
            blog_sections.append(blog)
    else:
        return []
    print(blog_sections)
    return blog_sections






def generate_blog_section_details(blogTopic, sectionTopic, audience, keywords):

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=f"Generate detailed blog section write up for the following blog section heading, using the blog title, audience and keywords. \nBlog Title:  {blogTopic}\nBlog Section Heading: {sectionTopic}\nAudience: {audience}\nKeywords: {keywords}\n",
    temperature=0.8,
    max_tokens=500,
    top_p=1,
    best_of=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    if 'choices' in response:
        if len(response['choices'])>0:
            res =  response['choices'][0]['text']
            cleanRes = res.replace('\\n', '<br />')
            return cleanRes
        else:
            return ''
    else:
        return ''












# def generate_blog_section_headings(topic, keywords):

#     response = openai.Completion.create(
#     model="text-davinci-002",
#     prompt=f"Generate blog section headings and section titles based on the following blog section topic\nTopic : {topic}\nKeywords: {keywords}\n*",
#     temperature=0.8,
#     max_tokens=301,
#     top_p=1,
#     best_of=1,
#     frequency_penalty=0,
#     presence_penalty=0
#     )

#     if 'choices' in response:
#         if len(response['choices'])>0:
#             res = response['choices'][0]['text']
#         else:
#             res = None
#     else:
#         res = None
    
   
#     return res


# topic = 'How to become an author'
# keyword = 'become an author, tips, guide, how to, aurthor'

# res = generate_blog_topic(topic, keyword).replace('\n', '')
# b_list = res.split('*')

# for blog in b_list:
#     blog_topics.append(blog)
#     print('\n')
#     print(blog)
#     print(blog_topics)