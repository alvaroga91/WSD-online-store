from onlinestore.models import *
from django.contrib.auth import views

from django.contrib import messages
from django.contrib.auth.models import User

from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.shortcuts import redirect
import json
from onlinestore.models import Save, Game, HighScore, Developer, Sales

from hashlib import md5

import datetime

def loginpage(request):
	return render(request, 'registration/login.html', {})


def main(request):
	if not request.user.is_authenticated():
		return views.login(request)
	else:
		return profile(request)


def profile(request):
	if not request.user.is_authenticated():
		return redirect('/login/?next=%s' % request.path)

	is_developer = hasattr(request.user, 'developer')
	developed_games = None
	if is_developer:
		developed_games = request.user.developer.developed_games.all()
	purchases = request.user.purchases.all()
	games = []
	for purchase in purchases:
		if (purchase.success):
			games.append(purchase.game)

	return render(request, 'profile.html', {
		"is_developer": is_developer,
		"developed_games": developed_games,
		"bought_games": games})
		

def tweet(request):
	return render(request, 'tweet.html', {})


def registration(request):
	if request.method == 'POST':
		if request.POST['passwd'] == request.POST['passwd2'] and request.POST['username'] and request.POST['email']:
			usern = request.POST['username']
			find_user = User.objects.filter(username=usern)

			if find_user:
				messages.add_message(request, messages.INFO, 'Username already taken. Choose a different username.')
				return render(request, 'registration/registration.html', {})

			email = request.POST['email']
			password = request.POST['passwd']
			password2 = request.POST['passwd2']
			u = User.objects.create_user(usern, email, password)

			if request.POST['user-role'] == 'developer':
				d = Developer(user=u)
				d.save()

			return render(request, 'registration/thanks.html', {})
		else:
			messages.add_message(request, messages.INFO,
								 'Passwords do not match or an input field left empty. All fields are needed.')
			return render(request, 'registration/registration.html', {})

	else:
		return render(request, 'registration/registration.html', {})


def game_save(request, game_id):
	if not request.user.is_authenticated():
		return HttpResponseForbidden()
	if request.method == 'POST':
		ret = request.POST
		game_state = json.loads(ret['gameState'])
		query_set = Save.objects.filter(player=request.user.id).filter(game=game_id)
		if query_set.exists():
			save = query_set[0]
			save.gameState = json.dumps(game_state)
			save.save()
		else:
			save = Save(player_id=request.user.id, game_id=game_id, gameState=json.dumps(game_state))
			save.save()
		return HttpResponse('')
	else:
		return HttpResponseBadRequest('')


def game_load(request, game_id):
	if not request.user.is_authenticated():
		return HttpResponseForbidden()
	if request.method == 'GET':
		querySet = Save.objects.filter(player=request.user.id).filter(game=game_id)
		if querySet.exists():
			save = querySet[0].gameState
			return HttpResponse(save, content_type="application/json")
		else:
			return HttpResponseNotFound('')
	return HttpResponseBadRequest('')


def game_score(request, game_id):
	if not request.user.is_authenticated():
		return HttpResponseForbidden()
	if request.method == 'POST':
		scoreValue = request.POST.get("score")
		score = HighScore(player_id=request.user.id, game_id=game_id, score=int(scoreValue))
		score.save()
		return HttpResponse("success")
	return HttpResponseNotFound('<h1>Page not found</h1>')


def addgame(request):
	if not hasattr(request.user, 'developer'):
		return HttpResponseNotFound('<h1>Page not found</h1>')

	if request.method == 'POST':
		game_name = request.POST['game_name']
		source_url = request.POST['source_url']
		price = request.POST['price']
		description = request.POST['description']
		category = request.POST['game-category']

		if game_name and source_url and price and float(price) >=0:
			try:
				g = Game(name=game_name, source_URL=source_url, developer=request.user.developer, price=price,
						 	description=description, category=category)
				g.save()
			except:
				messages.add_message(request, messages.INFO,
									 'Database error, potential causes: a game with this name (or URL) exists or price not valid.')
				return render(request, 'developer_add_game.html', {})
			messages.add_message(request, messages.INFO, 'A new game added')
			return redirect('/profile')
		else:
			messages.add_message(request, messages.INFO, 'A name, a URL and a nonnegative price are needed to add a game.')
			return render(request, 'developer_add_game.html', {})

	else:
		return render(request, 'developer_add_game.html', {})

	return render(request, 'developer_add_game.html', {})


def editgame(request):
	if not hasattr(request.user, 'developer'):
		return HttpResponseNotFound('<h1>Page not found</h1>')

	if request.method == 'POST':
		if 'to_be_edited' in request.POST:
			messages.add_message(request, messages.INFO, 'Edit the fields you want to change.')
			game = Game.objects.get(name=request.POST['to_be_edited'])
			params = {"game_name": game.name, "source_url": game.source_URL, "category": game.category, "price": game.price,
					  "description": game.description}
			return render(request, 'developer_edit_game.html', params)

		elif request.POST['game_name'] and request.POST['source_url'] and request.POST['category'] and request.POST['price'] and float(request.POST['price']) >= 0:
			game = Game.objects.get(name=request.POST['game_name'])
			game.game_name = request.POST['game_name']
			game.source_URL = request.POST['source_url']
			game.price = request.POST['price']
			game.category = request.POST['category']
			game.description = request.POST['description']
			try:
				game.save()
				messages.add_message(request, messages.INFO, 'Game information was edited.')
			except:
				messages.add_message(request, messages.INFO,
									 'Database error, potential causes: a game with this name (or URL) exists or price not valid. Try again.')
			return redirect('/profile')
		else:
			messages.add_message(request, messages.INFO, 'Required field missing or price not valid. Try again')
			return redirect('/profile')

	return redirect('/profile')


def deletegame(request):
	if not hasattr(request.user, 'developer'):
		return HttpResponseNotFound('<h1>Page not found</h1>')

	if request.method == 'POST':
		if 'to_be_deleted' in request.POST:
			game = Game.objects.get(name=request.POST['to_be_deleted'])
			params = {"game_name": game.name, "source_url": game.source_URL, "price": game.price,
					  "description": game.description}
			return render(request, 'developer_delete_game.html', params)

		elif 'delete_confirmed' in request.POST:
			game = Game.objects.get(name=request.POST['g_name'])
			try:
				game.delete()
				messages.add_message(request, messages.INFO, 'Game deleted.')
			except:
				messages.add_message(request, messages.INFO,
									 'Something went wrong and the game could not be deleted. Please try again.')
			return redirect('/profile')

		else:
			return render(request, 'developer_delete_game.html', {})

	return redirect('/profile')


def gamesales(request):
	if not hasattr(request.user, 'developer'):
		return HttpResponseNotFound('<h1>Page not found</h1>')

	if request.method == 'POST' and 'view_sales_of' in request.POST:
		g = Game.objects.filter(name=request.POST['view_sales_of'])
		s_dict = Sales.objects.filter(game=g, success=True).values()
		sold_num = len(s_dict)
		date_list = list()
		price_list = list()
		time_format = '%Y-%m-%d %H:%M:%S'
		for i in range(0, sold_num):
			# date_list.append(str(s_dict[i]['date']))
			date_list.append(s_dict[i]['date'].strftime(time_format))
		for j in range(0, sold_num):
			price_list.append(str(s_dict[j]['price']))
		zipped_sales = zip(date_list, price_list)
		net_sales = 0.0
		for k in range(0, len(price_list)):
			net_sales = net_sales + float(price_list[k])
		params = {"game_name": request.POST['view_sales_of'], "sold_num": sold_num, "zipped_sales": zipped_sales,
				  "net_sales": net_sales}
		return render(request, 'developer_game_sales.html', params)

	return redirect('/profile')


def viewgames(request):
	order_by = request.GET.get('order_by', 'name')
	games = Game.objects.all().order_by(order_by)
	return render(request, 'gamelist.html', {"games": games})


def viewgamepage(request, game_id):
	if request.user.is_authenticated():
		# Checks whether a sale is registered for that user and that game.
		game = Game.objects.get(pk=game_id)
		dev = game.developer.user
		global_scores = HighScore.objects.filter(game_id=game_id).order_by('-score')
		has_bought = (Sales.objects.filter(user=request.user, game=game, success=True).exists() | (dev == request.user))
		return render(request, 'game_page.html', {"game": game,
												  "has_bought": has_bought,
												  "global_scores": global_scores})

	return views.login(request)


def buygamepage(request, game_id):
	if request.user.is_authenticated():
		game = Game.objects.get(pk=game_id)
		if not (has_bought_game(request.user, game)):
			sale, created = Sales.objects.get_or_create(user=request.user, game=game, price=game.price)
			pid = sale.id
			sid = "alvarojaakkovesa"
			chk = checksum(pid, sid, game.price)
			print("\nFirst: " + chk)
			params = {"game": game, "pid": pid, "sid": sid, "price": game.price, "checksum": chk}
			return render(request, 'buy.html', params)
		else:
			return playgamepage(request, game_id)

	return render(request, 'registration/login.html', {})


def playgamepage(request, game_id):
	if request.user.is_authenticated():

		game = Game.objects.get(pk=game_id)
		global_scores = HighScore.objects.filter(game_id=game_id).order_by('-score')
		player_scores = global_scores.filter(player_id=request.user.id)
		#dev = game.developer.user
		#if (Sales.objects.filter(user=request.user, game=game, success=True).exists() | (dev == request.user)):
		if (has_bought_game(request.user, game)):
			print("exists\n")
			return render(request, 'game/game.html', {
				"game": game,
				"global_scores": global_scores,
				"player_scores": player_scores
			})
		else:
			return render(request, 'game_page.html', {"game": game, "has_bought": False})

	return render(request, 'registration/login.html', {})


def has_bought_game(user, game):
	dev = game.developer.user
	return Sales.objects.filter(user=user, game=game, success=True).exists() | (dev == user)

# Here we will check that the purchase went ok (checksum = ok)
def buysuccess(request, pid):
	if request.user.is_authenticated():
		sid = "alvarojaakkovesa"
		get_checksum = request.GET['checksum']
		pid = request.GET['pid']
		sale = Sales.objects.get(pk=pid)

		calc_checksum = securitystring(pid, request.GET["ref"])
		game = sale.game

		print(sale.date)
		if get_checksum == calc_checksum:
			sale.success = True
			sale.save()
			return render(request, 'payments/success.html', {"game": game})
		else:

			return render(request, 'payments/error.html', {"game": game})

	return render(request, 'registration/login.html', {})


def buycancel(request, pid):
	if request.user.is_authenticated():
		sale = Sales.objects.get(pk=pid)
		game = sale.game
		return render(request, 'game_page.html', {"game": game, "has_bought": False})

	return render(request, 'registration/login.html', {})


def buyerror(request, pid):
	if request.user.is_authenticated():
		sale = Sales.objects.get(pk=pid)
		game = sale.game
		return render(request, 'payments/error.html', {"game": game})

	return render(request, 'registration/login.html', {})


def checksum(pid, sid, amount):
	secret_key = "6ca381a8cf5761c9cd72064e0e1a5765"
	s = "pid=%s&sid=%s&amount=%s&token=%s" % (pid, sid, amount, secret_key)
	m = md5(s.encode("ascii"))
	return m.hexdigest()


def securitystring(pid, ref):
	secret_key = "6ca381a8cf5761c9cd72064e0e1a5765"
	s = "pid=%s&ref=%s&token=%s" % (pid, ref, secret_key)
	m = md5(s.encode("ascii"))
	return m.hexdigest()
