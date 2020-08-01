from django.shortcuts import render
import requests







def home(request):

    is_cached = ('geodata' in request.session)

    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        response = requests.get('http://ip-api.com/json')
        request.session['geodata'] = response.json()

    geodata = request.session['geodata']


    return render(request, 'home.html', {

        'ip': geodata['query'],
        'country': geodata['country'],
        'latitude': geodata['lat'],
        'longitude': geodata['lon'],
        'api_key': 'AIzaSyB952hvmpzaswkLSGgOiIrfdBrqSfIY-nU',  # Don't do this! This is just an example. Secure your keys properly.
        'is_cached': is_cached
    })



#
# def github(request):
#     search_result = {}
#     print(request)
#     if 'username' in request.GET:
#         username = request.GET['username']
#         print(username)
#         url = 'https://api.github.com/users/%s' % username
#         response = requests.get(url)
#         print(response)
#         search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
#         search_result = response.json()
#         search_result['success'] = search_was_successful
#         search_result['rate'] = {
#             'limit': response.headers['X-RateLimit-Limit'],
#             'remaining': response.headers['X-RateLimit-Remaining'],
#         }
#     return render(request, 'github.html', {'search_result': search_result})




from django.shortcuts import render
from github import Github, GithubException

def github_client(request):
    search_result = {}
    if 'username' in request.GET:
        username = request.GET['username']
        client = Github()

        try:
            user = client.get_user(username)
            search_result['name'] = user.name
            search_result['login'] = user.login
            search_result['public_repos'] = user.public_repos
            search_result['success'] = True
        except GithubException as ge:
            search_result['message'] = ge.data['message']
            search_result['success'] = False

        rate_limit = client.get_rate_limit()
        search_result['rate'] = {
            'limit': rate_limit.rate.limit,
            'remaining': rate_limit.rate.remaining,
        }
    return render(request, 'github.html', {'search_result': search_result})