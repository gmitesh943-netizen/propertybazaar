import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from blog.models import Post, Tag
from django.utils import timezone
import html

class Command(BaseCommand):
    help = 'Syncs latest real estate news from Google News RSS'

    def handle(self, *args, **options):
        self.stdout.write("Fetching latest news from Google News...")
        
        url = "https://news.google.com/rss/search?q=Ahmedabad+Real+Estate+News&hl=en-IN&gl=IN&ceid=IN:en"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            User = get_user_model()
            admin_user = User.objects.filter(is_superuser=True).first()
            
            if not admin_user:
                self.stderr.write("No admin user found to assign as author.")
                return

            news_tag, _ = Tag.objects.get_or_create(name='Latest News')
            
            count = 0
            for item in items[:10]:  # Limit to 10 latest
                title = html.unescape(item.find('title').text)
                link = item.find('link').text
                pub_date = item.find('pubDate').text
                description = html.unescape(item.find('description').text)
                
                slug = slugify(title)
                
                if not Post.objects.filter(slug=slug).exists():
                    post = Post.objects.create(
                        author=admin_user,
                        title=title,
                        slug=slug,
                        content=f"<p>{description}</p><p><a href='{link}' target='_blank'>Read full article on source</a></p>",
                        is_published=True
                    )
                    post.tags.add(news_tag)
                    count += 1
                    self.stdout.write(f"Created: {title}")
            
            self.stdout.write(self.style.SUCCESS(f"Successfully synced {count} new articles."))
            
        except Exception as e:
            self.stderr.write(f"Error syncing news: {str(e)}")
