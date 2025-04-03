import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import Package, Location, Inquiry, Image
from flask_sqlalchemy import pagination
from forms import PackageForm, LocationForm, ImageUploadForm
from app import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
logger = logging.getLogger(__name__)

# Admin access check
@admin_bp.before_request
def check_admin():
    logger.debug(f"Admin access check: authenticated={current_user.is_authenticated}")
    if current_user.is_authenticated:
        logger.debug(f"Admin check for user: {current_user.username}, is_admin={current_user.is_admin}")
    
    if not current_user.is_authenticated or not current_user.is_admin:
        logger.warning(f"Unauthorized admin access attempt: authenticated={current_user.is_authenticated}")
        abort(403)  # Forbidden

@admin_bp.route('/')
@login_required
def dashboard():
    package_count = Package.query.count()
    location_count = Location.query.count()
    inquiry_count = Inquiry.query.filter_by(status='Pending').count()
    inquiry_awaiting_count = Inquiry.query.filter_by(status='Contacted').count()
    
    # Get recent system updates
    system_updates = []
    
    # Add recent package updates
    recent_packages = Package.query.order_by(Package.created_at.desc()).limit(3).all()
    for package in recent_packages:
        system_updates.append({
            'type': 'package',
            'message': f'New package added: "{package.name}"',
            'date': package.created_at
        })
    
    # Add recent location updates
    recent_locations = Location.query.order_by(Location.created_at.desc()).limit(3).all()
    for location in recent_locations:
        system_updates.append({
            'type': 'location',
            'message': f'New location added: "{location.name}"',
            'date': location.created_at
        })
    
    # Add recent inquiry updates
    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(3).all()
    for inquiry in recent_inquiries:
        system_updates.append({
            'type': 'inquiry',
            'message': f'New inquiry from {inquiry.name}',
            'date': inquiry.created_at
        })
    
    # Sort updates by date
    system_updates.sort(key=lambda x: x['date'], reverse=True)
    system_updates = system_updates[:5]  # Only show latest 5 updates
    
    return render_template(
        'admin/dashboard.html', 
        package_count=package_count,
        location_count=location_count,
        inquiry_count=inquiry_count,
        inquiry_awaiting_count=inquiry_awaiting_count,
        system_updates=system_updates
    )

@admin_bp.route('/packages')
@login_required
def packages():
    packages = Package.query.all()
    return render_template('admin/packages.html', packages=packages)

@admin_bp.route('/packages/add', methods=['GET', 'POST'])
@login_required
def add_package():
    form = PackageForm()
    form.location_id.choices = [(l.id, l.name) for l in Location.query.all()]
    
    if form.validate_on_submit():
        package = Package(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            duration=form.duration.data,
            category=form.category.data,
            location_id=form.location_id.data,
            featured_image=form.featured_image.data
        )
        
        db.session.add(package)
        db.session.commit()
        
        flash('Package added successfully!', 'success')
        return redirect(url_for('admin.packages'))
    
    return render_template('admin/package_form.html', form=form, title='Add New Package')

@admin_bp.route('/packages/edit/<int:package_id>', methods=['GET', 'POST'])
@login_required
def edit_package(package_id):
    package = Package.query.get_or_404(package_id)
    form = PackageForm(obj=package)
    form.location_id.choices = [(l.id, l.name) for l in Location.query.all()]
    
    if form.validate_on_submit():
        package.name = form.name.data
        package.description = form.description.data
        package.price = form.price.data
        package.duration = form.duration.data
        package.category = form.category.data
        package.location_id = form.location_id.data
        package.featured_image = form.featured_image.data
        
        db.session.commit()
        
        flash('Package updated successfully!', 'success')
        return redirect(url_for('admin.packages'))
    
    return render_template('admin/package_form.html', form=form, title='Edit Package')

@admin_bp.route('/packages/delete/<int:package_id>', methods=['POST'])
@login_required
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)
    
    db.session.delete(package)
    db.session.commit()
    
    flash('Package deleted successfully!', 'success')
    return redirect(url_for('admin.packages'))

@admin_bp.route('/locations')
@login_required
def locations():
    page = request.args.get('page', 1, type=int)  # Get current page, default is 1
    per_page = 12  # Set items per page
    query = Location.query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
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
        pagination=pagination  # Send pagination object to the template
    )
@admin_bp.route('/locations/add', methods=['GET', 'POST'])
@login_required
def add_location():
    form = LocationForm()
    
    if form.validate_on_submit():
        location = Location(
            name=form.name.data,
            region=form.region.data,
            description=form.description.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            featured_image=form.featured_image.data
        )
        
        db.session.add(location)
        db.session.commit()
        
        flash('Location added successfully!', 'success')
        return redirect(url_for('admin.locations'))
    
    return render_template('admin/location_form.html', form=form, title='Add New Location')

@admin_bp.route('/locations/edit/<int:location_id>', methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    
    if form.validate_on_submit():
        location.name = form.name.data
        location.region = form.region.data
        location.description = form.description.data
        location.latitude = form.latitude.data
        location.longitude = form.longitude.data
        location.featured_image = form.featured_image.data
        
        db.session.commit()
        
        flash('Location updated successfully!', 'success')
        return redirect(url_for('admin.locations'))
    
    return render_template('admin/location_form.html', form=form, title='Edit Location')

@admin_bp.route('/locations/delete/<int:location_id>', methods=['POST'])
@login_required
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    # Check if there are packages associated with this location
    packages = Package.query.filter_by(location_id=location_id).all()
    if packages:
        flash('Cannot delete location because it has associated packages. Remove the packages first.', 'danger')
        return redirect(url_for('admin.locations'))
    
    db.session.delete(location)
    db.session.commit()
    
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('admin.locations'))

@admin_bp.route('/inquiries')
@login_required
def inquiries():
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    else:
        inquiries = Inquiry.query.filter_by(status=status_filter).order_by(Inquiry.created_at.desc()).all()
    
    return render_template('admin/inquiries.html', inquiries=inquiries, status_filter=status_filter)

@admin_bp.route('/inquiries/update-status/<int:inquiry_id>/<status>', methods=['POST'])
@login_required
def update_inquiry_status(inquiry_id, status):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    
    if status in ['Pending', 'Contacted', 'Resolved']:
        inquiry.status = status
        db.session.commit()
        flash('Inquiry status updated successfully!', 'success')
    else:
        flash('Invalid status value!', 'danger')
    
    return redirect(url_for('admin.inquiries'))

@admin_bp.route('/images')
@login_required
def images():
    category_filter = request.args.get('category', 'all')
    
    if category_filter == 'all':
        images = Image.query.order_by(Image.uploaded_at.desc()).all()
    else:
        images = Image.query.filter_by(category=category_filter).order_by(Image.uploaded_at.desc()).all()
    
    form = ImageUploadForm()
    
    return render_template('admin/images.html', images=images, category_filter=category_filter, form=form)

@admin_bp.route('/images/upload', methods=['POST'])
@login_required
def upload_image():
    form = ImageUploadForm()
    
    if form.validate_on_submit():
        # In a real implementation, you would save the uploaded file
        # For now, we'll just save the reference in the database
        image = Image(
            filename=f"placeholder-image-{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg",
            category=form.category.data,
            description=form.description.data
        )
        
        db.session.add(image)
        db.session.commit()
        
        flash('Image uploaded successfully!', 'success')
    else:
        flash('Error uploading image. Please check the form and try again.', 'danger')
    
    return redirect(url_for('admin.images'))

@admin_bp.route('/images/delete/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    
    # In a real implementation, you would also delete the file from storage
    db.session.delete(image)
    db.session.commit()
    
    flash('Image deleted successfully!', 'success')
    return redirect(url_for('admin.images'))

@admin_bp.route('/analytics')
@login_required
def analytics():
    # Get inquiry status counts
    pending_count = Inquiry.query.filter_by(status='Pending').count()
    contacted_count = Inquiry.query.filter_by(status='Contacted').count()
    resolved_count = Inquiry.query.filter_by(status='Resolved').count()
    
    # Get package counts by category
    categories = db.session.query(Package.category).distinct().all()
    category_counts = []
    
    for category in categories:
        count = Package.query.filter_by(category=category[0]).count()
        category_counts.append({
            'category': category[0],
            'count': count
        })
    
    # Get most popular packages
    popular_packages = Package.query.limit(5).all()  # In a real app, this would be based on actual stats
    
    # Inquiry sources (mockup data for this demo)
    inquiry_sources = [
        {'source': 'Website', 'count': 45},
        {'source': 'Social Media', 'count': 30},
        {'source': 'Referral', 'count': 15},
        {'source': 'Email', 'count': 10}
    ]
    
    return render_template(
        'admin/analytics.html',
        pending_count=pending_count,
        contacted_count=contacted_count,
        resolved_count=resolved_count,
        category_counts=category_counts,
        popular_packages=popular_packages,
        inquiry_sources=inquiry_sources
    )
