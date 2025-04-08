import os
import uuid
import stripe
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from app import db
from models import Package, Payment, User
from forms import PaymentForm
from utils import generate_receipt_pdf

payment = Blueprint('payment', __name__)

# Demo key - not a real key
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_demo_key')
DOMAIN_URL = os.environ.get('REPLIT_DOMAINS', 'http://localhost:5000').split(',')[0]

# Demo mode flag - set to True since we're in demo mode
DEMO_MODE = True

# Initialize Stripe with a placeholder key (won't be used in demo mode)
if not DEMO_MODE:
    # This would be the real Stripe integration code
    stripe.api_key = STRIPE_SECRET_KEY


@payment.route('/checkout/<int:package_id>', methods=['GET', 'POST'])
@login_required
def checkout(package_id):
    package = Package.query.get_or_404(package_id)
    form = PaymentForm()
    
    # Pre-fill package ID and email
    form.package_id.data = package.id
    
    if form.validate_on_submit():
        try:
            # Create payment record in pending state
            amount = package.price * form.travelers.data
            
            payment_record = Payment(
                user_id=current_user.id,
                package_id=package.id,
                amount=amount,
                currency='INR',
                status='pending',
                # In demo mode, generate fake IDs
                stripe_payment_id=f'demo_payment_{uuid.uuid4().hex[:8]}',
                stripe_session_id=f'demo_session_{uuid.uuid4().hex[:8]}'
            )
            
            db.session.add(payment_record)
            db.session.commit()
            
            flash('Your booking information has been saved. Please proceed to payment.', 'success')
            return redirect(url_for('payment.confirm', payment_id=payment_record.id))
            
        except IntegrityError:
            db.session.rollback()
            flash('There was an error processing your booking. Please try again.', 'danger')
    
    return render_template('payment/checkout.html', form=form, package=package)


@payment.route('/confirm/<int:payment_id>')
@login_required
def confirm(payment_id):
    payment_record = Payment.query.get_or_404(payment_id)
    
    # Verify payment belongs to current user
    if payment_record.user_id != current_user.id:
        flash('You do not have permission to view this payment.', 'danger')
        return redirect(url_for('payment.history'))
    
    return render_template('payment/confirm.html', payment=payment_record)


@payment.route('/checkout-session/<int:payment_id>')
@login_required
def checkout_session(payment_id):
    payment_record = Payment.query.get_or_404(payment_id)
    
    # Verify payment belongs to current user
    if payment_record.user_id != current_user.id:
        flash('You do not have permission to process this payment.', 'danger')
        return redirect(url_for('payment.history'))
    
    if DEMO_MODE:
        # In demo mode, simulate successful payment
        payment_record.status = 'completed'
        payment_record.stripe_payment_id = f'demo_payment_{uuid.uuid4().hex[:8]}'
        db.session.commit()
        
        flash('Demo payment completed successfully!', 'success')
        return redirect(url_for('payment.success'))
    
    # This would be the real Stripe checkout session code
    try:
        # Process with Stripe and update the payment record
        pass
    except stripe.error.StripeError as e:
        flash(f'Payment error: {str(e)}', 'danger')
        return redirect(url_for('payment.cancel'))
    
    return redirect(url_for('payment.success'))


@payment.route('/webhook', methods=['POST'])
def webhook():
    if DEMO_MODE:
        # In demo mode, skip webhook processing
        return jsonify(success=True)
    
    # This would be the real Stripe webhook handling code
    try:
        # Process Stripe webhook event
        pass
    except stripe.error.StripeError as e:
        return jsonify(error=str(e)), 400
    
    return jsonify(success=True)


@payment.route('/success')
@login_required
def success():
    # Get the most recent completed payment for this user
    payment_record = Payment.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).order_by(Payment.created_at.desc()).first()
    
    return render_template('payment/success.html', payment=payment_record)


@payment.route('/cancel')
@login_required
def cancel():
    return render_template('payment/cancel.html')


@payment.route('/history')
@login_required
def history():
    payments = Payment.query.filter_by(user_id=current_user.id).order_by(Payment.created_at.desc()).all()
    return render_template('payment/history.html', payments=payments)


@payment.route('/receipt/<int:payment_id>')
@login_required
def download_receipt(payment_id):
    """Generate and download a receipt PDF for a completed payment"""
    payment_record = Payment.query.get_or_404(payment_id)
    
    # Verify payment belongs to current user or user is admin
    if payment_record.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to download this receipt.', 'danger')
        return redirect(url_for('payment.history'))
    
    # Only allow receipt download for completed payments
    if payment_record.status != 'completed':
        flash('Receipt is only available for completed payments.', 'warning')
        return redirect(url_for('payment.history'))
    
    # Generate the PDF
    pdf_buffer = generate_receipt_pdf(payment_record)
    
    # Send the PDF file
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'receipt-{payment_record.stripe_payment_id}.pdf'
    )
