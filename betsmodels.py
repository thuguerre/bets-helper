class MatchResult:

    date = None
    sport = None
    country = None
    league = None
    home_team = None
    home_score = None
    visitor_team = None
    vistor_score = None

    def __init__(self):
        pass

    def __init__(self, date, sport, country, league, home_team, home_score, visitor_team, visitor_score):
        self.date = date
        self.sport = sport
        self.country = country
        self.league = league
        self.home_team = home_team
        self.home_score = home_score
        self.visitor_team = visitor_team
        self.visitor_score = visitor_score
    
    def toJSON(self):
        return {
            "date": self.date,
            "sport": self.sport,
            "country": self.country,
            "league": self.league,
            "home_team": self.home_team,
            "home_score": self.home_score,
            "visitor_team": self.visitor_team,
            "visitor_score": self.visitor_score
        }
