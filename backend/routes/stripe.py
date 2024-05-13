from fastapi import APIRouter, HTTPException, Request
import stripe
import os
from dotenv import load_dotenv
from config.db import conn
from models.index import appointments
from schemas.index import Appointment
from sqlalchemy.sql import select, update, desc

payment = APIRouter()

load_dotenv()

# Initialize the Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET")

@payment.post("/pay/checkout")
async def create_checkout_session(request: Request):
    req_data = await request.json()
    try:
        # Create a Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            customer_email="blueowls@example.com",
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "product_data": {
                            "name": "BlueOwls Patient Appointment",
                        },
                        "unit_amount": 49900,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="https://deploy-front-nu.vercel.app/pay/success", 
            cancel_url="https://deploy-front-nu.vercel.app/dashboard",
            metadata={
                "patient_id": req_data['patientId'],
            }
        )

        return checkout_session

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@payment.post("/webhook")
async def handle_stripe_webhook(request: Request):
    # Parse the incoming webhook event from Stripe
    payload = await request.body()
    sig_header = request.headers['Stripe-Signature']
    endpoint_secret = os.getenv("STRIPE_WEBHOOK")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if event['type'] == 'checkout.session.completed':
        # Payment successful, update appointment payment status
        appointment_id = event['data']['object']['metadata']['patient_id']
        query = appointments.select().where(
            (appointments.c.patient_id == appointment_id)
        ).order_by(desc(appointments.c.id)).limit(1)
        
        # Execute the query
        result = conn.execute(query).fetchone()
        
        if result:
            # Update the payment status of the latest appointment record to "completed"
            update_query = appointments.update().where(appointments.c.id == result.id).values(payment_status="completed")
            conn.execute(update_query)
        else:
            raise HTTPException(status_code=404, detail="Appointment not found")
    
    return {"status": "success"}
