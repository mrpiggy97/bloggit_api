#search and filter communities that match string
from taggit.models import Tag

from posts_app.models import Post

def get_communities_from_string(string):
    communities = []
    filtered_communities = {}
    query = string.split(" ")
    for word in query:
        filtered_communities[word] = Tag.objects.filter(slug=word)
    
    for community_list in filtered_communities.values():
        for community in community_list:
            if community.slug in string and community.slug not in communities:
                communities.append(community)
    return communities

def search_for_posts(string):
    communities = get_communities_from_string(string)
    posts = []
    posts_per_comm = {}
    
    for comm in communities:
        posts_per_comm[comm.slug] = Post.objects.filter(communities=comm).order_by('-id')
    
    for post_list in posts_per_comm.values():
        for post in post_list:
            if post not in posts:
                posts.append(post)
    return posts