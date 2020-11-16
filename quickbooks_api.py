from flask import session

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

from quickbooks import QuickBooks

# QB objects
from quickbooks.objects.account import Account
from quickbooks.objects.bill import Bill
from quickbooks.objects.company_info import CompanyInfo
from quickbooks.objects.customer import Customer
from quickbooks.objects.employee import Employee
from quickbooks.objects.estimate import Estimate
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.item import Item
from quickbooks.objects.payment import Payment
from quickbooks.objects.taxagency import TaxAgency
from quickbooks.objects.vendor import Vendor

# Instantiate client
auth_client = AuthClient(
    "ABnSSkncHKmnx17XSaNfgrxTwNXm5FzGYTUURNkhhriU2EZXI6",
    "UoPFjInBWlUCbM1t5ftzqMmhKZgPtr7ZqxaFM6u1",
    "http://localhost:5000/oauth",
    "sandbox",
)

# Get authorization URL
auth_url = auth_client.get_authorization_url([
    Scopes.ACCOUNTING,
    Scopes.OPENID,
    Scopes.PROFILE,
    Scopes.EMAIL,
])

qb_objects = {
    'ACCOUNT': Account,
    'BILL': Bill,
    'COMPANYINFO': CompanyInfo,
    'CUSTOMER': Customer,
    'EMPLOYEE': Employee,
    'ESTIMATE': Estimate,
    'INVOICE': Invoice,
    'ITEM': Item,
    'PAYMENT': Payment,
    'TAXAGENCY': TaxAgency,
    'VENDOR': Vendor,
}


def get_qb_object(obj=''):
    return qb_objects[obj.upper()]


def get_qb_client():
    return QuickBooks(
        auth_client=auth_client,
        refresh_token=session['refresh_token'],
        company_id=session['company_id'],
        minorversion=55
    )
