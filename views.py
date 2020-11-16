import json
from flask import Blueprint, render_template, redirect, request, session

from quickbooks import QuickBooks
from quickbooks.exceptions import ObjectNotFoundException

from forms import QueryOneForm
from quickbooks_api import get_qb_object, get_qb_client


def create_views(auth):
    views = Blueprint('views', __name__)
    auth_url = auth['url']
    auth_client = auth['client']

    @views.route('/views/<path:path>', methods=['GET', 'POST'])
    @views.route('/views/<path:path>/one', methods=['GET', 'POST'])
    def index(path=None):
        if 'user_info' not in session:
            # Completely log out
            return redirect('/logout')
        else:
            user_info = session['user_info']

        form = QueryOneForm()

        view = 'one'

        if request.method == 'POST':
            # Handle form submission
            if form.validate_on_submit():
                data_id = form.id.data


                qb_obj = get_qb_object(path)

                try:
                    data = qb_obj.get(data_id, get_qb_client())
                    data = data.to_json()  # JSONify the object
                except ObjectNotFoundException:
                    data = {"code": "404", "msg": "Object does not exist"}

                return render_template('home.html', user_info=user_info, path=path,
                                       view=view, form=form, data=data)
        else:
            return render_template('home.html', user_info=user_info, path=path, view=view, form=form)

    @views.route('/views/<path:path>/all', methods=['GET', 'POST'])
    def path_view_all(path):
        if 'user_info' not in session:
            # Completely log out
            return redirect('/logout')
        else:
            user_info = session['user_info']

        view = 'all'

        qb_obj = get_qb_object(path)

        try:
            data = qb_obj.all(qb=get_qb_client(), max_results=100)  # Hard limit of 1,000 but too taxing to request for and no one wants to sift through that much data either

            data = json.dumps({
                "QueryResponse": {
                    # to_json doesn't actually convert to json but a string
                    # so I have to do this funky stuff to get it to render correctly on the page
                    path.title(): [json.loads(d.to_json()) for d in data]
                }
            }, indent=4)
        except ObjectNotFoundException:
            data = {"code": "404", "msg": "Object does not exist"}

        return render_template('home.html', user_info=user_info, path=path, view=view, data=data)

    ########################################
    # Authentication

    @views.route('/')
    @views.route('/login')
    def login():
        # Check if logged in already and redirect if true
        if 'is_authorised' in session:
            return redirect('/views/account')

        # We want the user to immediately log in
        return redirect(auth_url)

    @views.route('/logout')
    def logout():
        # Refresh token endpoint
        try:
            auth_client.revoke(token=auth_client.refresh_token)
        except ValueError as e:
            print(e)

        session.clear()

        return redirect('/')

    @views.route('/oauth')
    def oauth_handler():
        # Get the uhh get params
        auth_code = request.args.get('code')
        state = request.args.get('state')
        realm_id = request.args.get('realmId')

        # Get bearer token
        auth_client.get_bearer_token(auth_code, realm_id=realm_id)

        response = auth_client.get_user_info()

        session['is_authorised'] = True
        session['token'] = auth_client.access_token
        session['access_token'] = auth_client.access_token
        session['refresh_token'] = auth_client.refresh_token
        session['company_id'] = realm_id
        session['user_info'] = response.json()
        session['client'] = QuickBooks(
            auth_client=auth_client,
            refresh_token=auth_client.refresh_token,
            company_id=realm_id,
        )

        print(session['user_info'])

        return redirect('/')

    # Return the views
    return views
