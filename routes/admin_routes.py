import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, send_file, request
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from app import db
from models import User, Package, Payment, Location, Inquiry, Image  # Ensure Image is imported
from utils import generate_receipt_pdf
import logging  # Import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')  # Changed to admin_bp for consistency
logger = logging.getLogger(__name__)  # Initialize logger

@admin_bp.before_request
def check_admin():
    """Ensure user is authenticated and has admin privileges"""
    logger.debug(f"Admin access check: authenticated={current_user.is_authenticated}")
    if current_user.is_authenticated:
        logger.debug(f"Admin check for user: {current_user.username}, is_admin={current_user.is_admin}")
    if not current_user.is_authenticated or not current_user.is_admin:
        logger.warning(f"Unauthorized admin access attempt: authenticated={current_user.is_authenticated}")
        abort(403)  # Forbidden access


@admin_bp.route('/')
@login_required
def dashboard():
    """Admin dashboard with overview statistics"""

    # Basic statistics
    user_count = User.query.count()
    package_count = Package.query.count()
    total_payments = Payment.query.count()
    completed_payments = Payment.query.filter_by(status='completed').count()
    pending_payments = Payment.query.filter_by(status='pending').count()
    cancelled_payments = Payment.query.filter_by(status='cancelled').count()

    # Total revenue from completed payments
    completed_payment_records = Payment.query.filter_by(status='completed').all()
    total_revenue = sum(payment.amount for payment in completed_payment_records) if completed_payment_records else 0

    # Recent payments with eager loading of related packages
    recent_payments = (
        Payment.query
        .options(joinedload(Payment.packages))
        .order_by(Payment.created_at.desc())
        .limit(5)
        .all()
    )

    # New packages added in the current month
    thirty_days_ago = datetime.utcnow().replace(day=1)  # First day of current month
    new_packages = Package.query.filter(Package.created_at >= thirty_days_ago).count()

    # Placeholder growth values (replace with real calculations as needed)
    booking_growth = 15
    revenue_growth = 12
    user_growth = 8

    # Popular packages based on booking count and revenue
    popular_packages = []
    packages = Package.query.limit(5).all()

    for package in packages:
        package_payments = Payment.query.filter_by(package_id=package.id, status='completed').all()
        booking_count = len(package_payments)
        revenue = sum(payment.amount for payment in package_payments)

        if booking_count > 0:
            package.booking_count = booking_count
            package.revenue = revenue
            popular_packages.append(package)

    # Sort popular packages by booking count and limit to top 5
    popular_packages.sort(key=lambda x: x.booking_count, reverse=True)
    popular_packages = popular_packages[:5]

    # Most popular package for the highlight card
    popular_package = popular_packages[0] if popular_packages else None
    popular_package_count = popular_package.booking_count if popular_package else 0

    return render_template(
        'admin/dashboard.html',
        total_payments=total_payments,
        completed_payments=completed_payments,
        pending_payments=pending_payments,
        cancelled_payments=cancelled_payments,
        total_revenue=total_revenue,
        user_count=user_count,
        package_count=package_count,
        new_packages=new_packages,
        recent_payments=recent_payments,
        booking_growth=booking_growth,
        revenue_growth=revenue_growth,
        user_growth=user_growth,
        popular_packages=popular_packages,
        popular_package=popular_package,
        popular_package_count=popular_package_count
    )

@admin_bp.route('/payments')
@login_required
def payments():
    """View all payment records"""
    # Get all payment records
    payment_records = Payment.query.order_by(Payment.created_at.desc()).all()

    # Calculate statistics
    total_payments = len(payment_records)
    completed_payments = sum(1 for p in payment_records if p.status == 'completed')
    pending_payments = sum(1 for p in payment_records if p.status == 'pending')
    cancelled_payments = sum(1 for p in payment_records if p.status == 'cancelled')

    # Calculate total revenue
    total_revenue = sum(p.amount for p in payment_records if p.status == 'completed')

    # Get most popular package
    package_counts = {}
    for payment in payment_records:
        if payment.status == 'completed':
            package_id = payment.package_id
            if package_id in package_counts:
                package_counts[package_id] += 1
            else:
                package_counts[package_id] = 1

    popular_package = None
    popular_package_count = 0

    if package_counts:
        most_popular_id = max(package_counts.items(), key=lambda x: x[1])[0]
        popular_package = Package.query.get(most_popular_id)
        popular_package_count = package_counts[most_popular_id]

    # Get recent payments
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(10).all()

    return render_template('admin/payments.html',
                           payments=payment_records,
                           total_payments=total_payments,
                           completed_payments=completed_payments,
                           pending_payments=pending_payments,
                           cancelled_payments=cancelled_payments,
                           total_revenue=total_revenue,
                           popular_package=popular_package,
                           popular_package_count=popular_package_count,
                           recent_payments=recent_payments)


@admin_bp.route('/receipt/<int:payment_id>')
@login_required
def download_receipt(payment_id):
    """Generate and download a receipt PDF for any payment"""
    payment_record = Payment.query.get_or_404(payment_id)

    # Only allow receipt download for completed payments
    if payment_record.status != 'completed':
        flash('Receipt is only available for completed payments.', 'warning')
        return redirect(url_for('admin.payments'))

    # Generate the PDF
    pdf_buffer = generate_receipt_pdf(payment_record)

    # Send the PDF file
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'receipt-{payment_record.stripe_payment_id}.pdf'
    )

@admin_bp.route('/packages')
@login_required
def packages():
    packages = Package.query.all()
    return render_template('admin/packages.html', packages=packages)

@admin_bp.route('/packages/add', methods=['GET', 'POST'])
@login_required
def add_package():
    from forms import PackageForm  # Import here to avoid circular dependency
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
        return redirect(url_for('admin_bp.packages'))  # Use admin_bp

    return render_template('admin/package_form.html', form=form, title='Add New Package')

@admin_bp.route('/packages/edit/<int:package_id>', methods=['GET', 'POST'])
@login_required
def edit_package(package_id):
    from forms import PackageForm  # Import here to avoid circular dependency
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
        return redirect(url_for('admin_bp.packages'))  # Use admin_bp

    return render_template('admin/package_form.html', form=form, title='Edit Package')

@admin_bp.route('/packages/delete/<int:package_id>', methods=['POST'])
@login_required
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)

    db.session.delete(package)
    db.session.commit()

    flash('Package deleted successfully!', 'success')
    return redirect(url_for('admin_bp.packages'))  # Use admin_bp

@admin_bp.route('/locations')
@login_required
def locations():
    locations = Location.query.all()
    locations_data = []
    for location in locations:
        locations_data.append({
            "id": location.id,
            "name": location.name,
            "region": location.region,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "featured_image": location.featured_image,
            "description": location.description,
            "packages": [p.name for p in location.packages]  # Include package names
        })
    return render_template('admin/locations.html', locations=locations_data)

@admin_bp.route('/locations/add', methods=['GET', 'POST'])
@login_required
def add_location():
    from forms import LocationForm  # Import here to avoid circular dependency
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
        return redirect(url_for('admin_bp.locations'))  # Use admin_bp

    return render_template('admin/location_form.html', form=form, title='Add New Location')

@admin_bp.route('/locations/edit/<int:location_id>', methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    from forms import LocationForm  # Import here to avoid circular dependency
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
        return redirect(url_for('admin_bp.locations'))  # Use admin_bp

    return render_template('admin/location_form.html', form=form, title='Edit Location')

@admin_bp.route('/locations/delete/<int:location_id>', methods=['POST'])
@login_required
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)

    # Check if there are packages associated with this location
    packages = Package.query.filter_by(location_id=location_id).all()
    if packages:
        flash('Cannot delete location because it has associated packages. Remove the packages first.', 'danger')
        return redirect(url_for('admin_bp.locations'))  # Use admin_bp

    db.session.delete(location)
    db.session.commit()

    flash('Location deleted successfully!', 'success')
    return redirect(url_for('admin_bp.locations'))  # Use admin_bp

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
    
    return redirect(url_for('admin_bp.inquiries'))

@admin_bp.route('/images')
@login_required
def images():
    from forms import ImageUploadForm  # Import here to avoid circular dependency
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
    from forms import ImageUploadForm  # Import here to avoid circular dependency
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

    return redirect(url_for('admin_bp.images'))  # Use admin_bp

@admin_bp.route('/images/delete/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)

    # In a real implementation, you would also delete the file from storage
    db.session.delete(image)
    db.session.commit()

    flash('Image deleted successfully!', 'success')
    return redirect(url_for('admin_bp.images'))  # Use admin_bp

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