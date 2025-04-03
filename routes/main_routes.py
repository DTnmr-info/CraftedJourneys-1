from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Package, Location, Inquiry
from flask_sqlalchemy import pagination
from forms import ContactForm
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_packages = Package.query.limit(3).all()
    return render_template('index.html', featured_packages=featured_packages)

@main_bp.route('/packages')
def packages():
    category = request.args.get('category', None)
    region = request.args.get('region', None)
    
    query = Package.query
    
    if category:
        query = query.filter(Package.category == category)
    
    if region:
        query = query.join(Package.location).filter(Location.region == region)
    
    packages = query.all()
    categories = db.session.query(Package.category).distinct().all()
    regions = db.session.query(Location.region).distinct().all()
    
    return render_template(
        'packages.html', 
        packages=packages, 
        categories=[cat[0] for cat in categories], 
        regions=[reg[0] for reg in regions],
        selected_category=category,
        selected_region=region
    )

@main_bp.route('/packages/<int:package_id>')
def package_detail(package_id):
    package = Package.query.get_or_404(package_id)
    
    # Find related packages in the same category
    related_packages = Package.query.filter(
        Package.category == package.category, 
        Package.id != package.id
    ).limit(3).all()
    
    # Sample itinerary data (in a real application, this would come from the database)
    itinerary = [
        {
            'title': 'Arrival & Welcome',
            'description': 'Upon arrival at the airport/railway station, you\'ll be welcomed by our representative who will transfer you to your hotel. After check-in and some rest, enjoy a welcome dinner with a brief orientation about your upcoming journey.'
        },
        {
            'title': 'Exploration Day',
            'description': 'After breakfast, embark on a guided tour of the main attractions. Enjoy a traditional lunch at a local restaurant, followed by visits to cultural sites and markets. The evening is yours to relax or explore the surroundings.'
        },
        {
            'title': 'Cultural Immersion',
            'description': 'Today is dedicated to a deeper cultural experience. Participate in local activities, interact with community members, and learn about traditional crafts. Enjoy an authentic dinner with a local family.'
        },
        {
            'title': 'Free Day & Farewell',
            'description': 'Spend the morning at your leisure. Optional activities available. In the afternoon, gather for a farewell lunch. Transfer to the airport/railway station for your onward journey with fond memories of your trip.'
        }
    ]
    
    # Sample gallery images (in a real application, these would come from the database)
    gallery_images = [
        {'url': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80', 'alt': 'Scenic view of the destination'},
        {'url': 'https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=400&q=80', 'alt': 'Local culture'},
        {'url': 'https://images.unsplash.com/photo-1546961329-78bef0414d7c?auto=format&fit=crop&w=400&q=80', 'alt': 'Activities'},
        {'url': 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=400&q=80', 'alt': 'Accommodation'},
        {'url': 'https://images.unsplash.com/photo-1517759544474-6b28a886d22d?auto=format&fit=crop&w=400&q=80', 'alt': 'Food and cuisine'}
    ]
    
    # Pass all required data to the template
    from datetime import datetime
    return render_template(
        'package_detail.html', 
        package=package, 
        related_packages=related_packages,
        itinerary=itinerary,
        gallery_images=gallery_images,
        now=datetime.now()
    )

@main_bp.route('/locations')
def locations():
    region = request.args.get('region', None)
    page = request.args.get('page', 1, type=int)  # Get current page, default is 1
    per_page = 12  # Set items per page

    query = Location.query

    if region:
        query = query.filter(Location.region == region)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    regions = db.session.query(Location.region).distinct().all()

    locations_data = []
    for location in pagination.items:
        locations_data.append({
            "id": location.id,
            "name": location.name,
            "region": location.region,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "featured_image": location.featured_image,
            "description": location.description,
            "packages": location.packages
        })

    return render_template(
        'locations.html', 
        locations=locations_data,
        regions=[reg[0] for reg in regions],
        selected_region=region,
        pagination=pagination  # Send pagination object to the template
    )
@main_bp.route('/locations/<int:location_id>')
def location_detail(location_id):
    location = Location.query.get_or_404(location_id)
    packages = Package.query.filter_by(location_id=location_id).all()
    
    return render_template('location_detail.html', location=location, packages=packages)

@main_bp.route('/services')
def services():
    return render_template('services.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        inquiry = Inquiry(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data,
            interest=form.interest.data,
            status="Pending"
        )
        
        db.session.add(inquiry)
        db.session.commit()
        
        flash('Thank you for your inquiry! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', form=form)
