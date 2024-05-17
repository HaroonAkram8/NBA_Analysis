def seasons_list(start_season_year: int, end_season_year: int):
    seasons = []
    for year in range(start_season_year, end_season_year+1):
        seasons.append(str(year) + "-" + str(int(str(year)[2:]) + 1))
    
    return seasons