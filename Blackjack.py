from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'blackjack_secret'

# Card deck
suits = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'J': 10, 'Q': 10, 'K': 10, 'A': 11}


def deal_card():
    return random.choice(ranks), random.choice(list(suits.keys()))


def calculate_hand(hand):
    value = sum(values[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


def display_hand(hand):
    return ', '.join([f'{rank}{suits[suit]}' for rank, suit in hand])


@app.route('/')
def index():
    session.clear()
    session['player_hand'] = [deal_card(), deal_card()]
    session['dealer_hand'] = [deal_card(), deal_card()]
    return render_template('index.html', player_hand=session['player_hand'], dealer_hand=session['dealer_hand'],
                           message="Game started! Hit or Stand?")


@app.route('/hit')
def hit():
    session['player_hand'].append(deal_card())
    player_value = calculate_hand(session['player_hand'])
    if player_value > 21:
        return render_template('index.html', player_hand=session['player_hand'], dealer_hand=session['dealer_hand'],
                               message="Bust! You exceeded 21. Dealer wins.")
    return render_template('index.html', player_hand=session['player_hand'], dealer_hand=session['dealer_hand'],
                           message="Hit or Stand?")


@app.route('/stand')
def stand():
    while calculate_hand(session['dealer_hand']) < 17:
        session['dealer_hand'].append(deal_card())
    player_score = calculate_hand(session['player_hand'])
    dealer_score = calculate_hand(session['dealer_hand'])

    if dealer_score > 21 or player_score > dealer_score:
        message = "Congratulations! You win!"
    elif player_score < dealer_score:
        message = "Dealer wins. Better luck next time!"
    else:
        message = "It's a tie!"

    return render_template('index.html', player_hand=session['player_hand'], dealer_hand=session['dealer_hand'],
                           message=message)


if __name__ == "__main__":
    app.run(debug=True)
