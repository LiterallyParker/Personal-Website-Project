class Card {
    constructor(suit,rank) {
        this.suit = suit
        this.rank = rank
    }
    displayCard() {
        console.log(`${this.rank} of ${this.suit}`)
    }
}
class Deck {
    constructor() {
        this.cards = []
        let suits = ["Spades","Hearts","Clubs","Diamonds"]
        let ranks = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]
        for(let i = 0; i < suits.length; i++) {
            for(let j = 0; j < ranks.length; j++) {
                this.cards.push(new Card(suits[i],ranks[j]))
            }
        }
    }
    shuffle() {
        this.cards.sort(() => Math.random() - 0.5)
    }
    deal(num) {
        let cardsDealt = []
        for(let i = 0; i < num; i++) {
            cardsDealt.push(this.cards.pop())
        }
        return cardsDealt
    }
    flipCards() {
        for(let i = 0; i < this.cards.length; i++) {
            this.cards[i].displayCard()
        }
    }
}
class Hand {
    constructor() {
        this.cards = [];
    }
    showHand() {
        for(let i = 0; i < this.cards.length; i++) {
            console.log(this.cards[i])
        }
    }
}
class Poker {
    play() {
        this.deck = new Deck();
        this.hand = new Hand();
        this.deck.shuffle()
        this.hand.cards = this.deck.deal(5)
        for(let i = 0; i < this.hand.cards.length; i++) {
            console.log(this.hand.cards[i])
        }
    }
}
let game = new Poker()
game.play()
