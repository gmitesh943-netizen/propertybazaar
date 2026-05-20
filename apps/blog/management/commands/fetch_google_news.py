import feedparser
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post, Category
from accounts.models import User
from django.core.files.base import ContentFile
import time

class Command(BaseCommand):
    help = 'Fetches real-time news from Google News RSS and populates the blog'

    def handle(self, *args, **options):
        # Get or create a default author (first superuser)
        author = User.objects.filter(is_superuser=True).first()
        if not author:
            self.stdout.write(self.style.ERROR('No superuser found to assign as author.'))
            return

        categories = Category.objects.all()
        if not categories.exists():
            self.stdout.write(self.style.WARNING('No categories found. Please run seed_blog_categories.py first.'))
            return

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        for category in categories:
            self.stdout.write(f'Fetching news for category: {category.name}')
            
            query = f'{category.name} real estate India'
            rss_url = f'https://news.google.com/rss/search?q={query.replace(" ", "%20")}&hl=en-IN&gl=IN&ceid=IN:en'
            
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:8]: # Fetch top 8 for each category
                title = entry.title
                link = entry.link
                summary = entry.summary
                
                if Post.objects.filter(title=title).exists():
                    continue

                self.stdout.write(f'  Processing: {title}')
                
                thumbnail_file = None
                try:
                    # Resolve Google News redirect link to get the actual article URL
                    res = requests.get(link, headers=headers, timeout=10, allow_redirects=True)
                    actual_url = res.url
                    
                    soup = BeautifulSoup(res.text, 'html.parser')
                    og_image = soup.find('meta', property='og:image') or soup.find('meta', name='twitter:image')
                    
                    if og_image and og_image.get('content'):
                        img_url = og_image['content']
                        # Ignore generic icons/logos
                        if 'googlesyndication' not in img_url and 'googleusercontent' not in img_url:
                            img_res = requests.get(img_url, headers=headers, timeout=10)
                            if img_res.status_code == 200:
                                thumbnail_file = ContentFile(img_res.content, name=f'{slugify(title[:50])}.jpg')
                except Exception as e:
                    self.stdout.write(f'    Thumbnail fetch error: {e}')

                # Fallback to high-quality Unsplash image if no article image found
                if not thumbnail_file:
                    try:
                        unsplash_url = f'https://source.unsplash.com/1200x800/?realestate,architecture,{category.slug}'
                        img_res = requests.get(unsplash_url, headers=headers, timeout=10)
                        if img_res.status_code == 200:
                            thumbnail_file = ContentFile(img_res.content, name=f'placeholder-{category.slug}.jpg')
                    except:
                        pass

                post = Post.objects.create(
                    author=author,
                    category=category,
                    title=title,
                    content=summary + f'<br><br><a href="{link}" target="_blank" class="btn btn-sm btn-outline-primary rounded-pill mt-3">Read full article on source</a>',
                    is_published=True
                )
                if thumbnail_file:
                    post.thumbnail.save(f'{slugify(title[:50])}.jpg', thumbnail_file, save=True)
                
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Successfully updated news with high-quality images!'))

