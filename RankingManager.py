import math


class RankingManager:
    def __init__(self, elo_ranking, matches_played):
        self.k = self.get_development_coefficient(elo_ranking, matches_played)

    def get_development_coefficient(self, ranking, matches):
        if matches <= 30:
            return 40
        elif 30 <= matches and ranking <= 2400.0:
            return 20
        else:
            return 10

    def probability(self, rating1, rating2):
        return 1.0 / (1 + 1.0 * 10 ** ((1.0 * (rating1 - rating2) / 400)))

    def elo_rating(self, Ra, Rb, d):
        Pb = self.probability(Ra, Rb)
        Pa = self.probability(Rb, Ra)

        if d:  # Player One wins
            return Ra + self.k * (1 - Pa), Rb + self.k * (0 - Pb)
        else:
            return Ra + self.k * (0 - Pa), Rb + self.k * (1 - Pb)
