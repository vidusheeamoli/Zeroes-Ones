from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown
import os

def mkdir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)


templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
contents_dir = os.path.join(os.path.dirname(__file__), 'contents')


jinja_env = Environment(loader = FileSystemLoader(templates_dir))

all_posts = [] #list
#Generating all Individual Blogs and also collecting all_posts  
for blog in os.listdir(contents_dir):
	if blog.endswith(".md") and (not blog.startswith(".")):
		with open('contents/{}'.format(blog), 'r') as file:
				parsed = markdown(file.read(), extras=['metadata'])
		template = jinja_env.get_template('blog.html')
		blog_name, blog_extension = os.path.splitext(blog)
		blog_name = blog_name+".html"
		data = {
				'content': parsed,
				'title': parsed.metadata['title'],
				'date': parsed.metadata['date'],
				'address': blog_name
				}
		mkdir('./output') #make output directory if not already made
		output_dir = os.path.join(os.path.dirname(__file__), 'output')
		new_blog = os.path.join(output_dir, blog_name)
		output_file = open(new_blog, "w")
		output_file.write(template.render(post=data))

		all_posts.append({
				'title': parsed.metadata['title'],
				'date': parsed.metadata['date'],
				'address': blog_name
				})

#Creating Index.html, should include date and title and links
template = jinja_env.get_template('index.html')
blog_name = "index.html"
new_blog = os.path.join(output_dir, blog_name)
output_file = open(new_blog, "w")
output_file.write(template.render(posts=all_posts))


