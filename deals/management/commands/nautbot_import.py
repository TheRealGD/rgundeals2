#!/usr/bin/env python
import json
import urllib.parse
import re
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from deals.models import Category, VendorDomain, Vendor, Deal
from users.models import User

class Command(BaseCommand):
    help = 'Generate data from a nautbot json export'

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        # Load JSON
        links = json.load(open(options['filename'], 'r'))
        db_inserts = 0


        # Create a list of dealers + domain mappings (for vendor domains/vendor listings)
        # This isn't accurate, since if a dealer submits a deal on another site he gets that domain,
        # but for testing its OK.
        vendors = dict()
        dealer_links = [x for x in links if x['flair'] != 'none']
        for link in dealer_links:
            domain = urllib.parse.urlparse(link['linkurl']).netloc.replace('www.', '')
            if link['name'] not in vendors:
                vendors[link['name']] = list()
            if domain not in vendors[link['name']]:
                vendors[link['name']].append(domain)

        # Create dealers/domains if necessary and write to DB
        for vendor_name, domains in vendors.items():
            vendor_object, new = Vendor.objects.get_or_create(name=vendor_name, defaults={'slug': slugify(vendor_name)})
            if new:
                db_inserts += 1
            for domain in domains:
                if VendorDomain.objects.get_or_create(domain=domain, defaults={'vendor': vendor_object})[1]:
                    db_inserts += 1
        categories = {}
        # Generate categories & Links
        for link in links:
            category = re.search(r'^\[(\w+)\]', link['title'])
            if category:
                category = category.group(1).capitalize()
                # check to see if category exists for db entry
                if category not in categories:
                    # Create or get
                    category_object, new = Category.objects.get_or_create(
                        name=category,
                        defaults={'color': '2196f3', 'slug': slugify(category)}
                    )
                    categories[category] = category_object
                    if new:
                        db_inserts += 1
                category = categories[category]
            else:
                category = Category.objects.get(id=1)
            Deal.objects.create(
                url=link['linkurl'],
                title=link['title'],
                category=category,
                created_by=User.objects.get(id=1)  # TODO: Make this user configurable
            )
            db_inserts += 1
        self.stdout.write(self.style.SUCCESS('Parsed "%s"' % options['filename']))
        self.stdout.write(self.style.SUCCESS('Successfully inserted %i records' % db_inserts))
