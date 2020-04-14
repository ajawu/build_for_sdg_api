def estimator(data):
    """
    function to determine impact and severe impact of covid-19 on a country
    """
    # Challenge 1
    # calculate currentlyInfected based on reportedCases
    try:
        if isinstance(data['reportedCases'], int):
            impact = {'currentlyInfected': data['reportedCases'] * 10}
            severeImpact = {'currentlyInfected': data['reportedCases'] * 50}
        else:
            return {'error': "Key 'reportedCases' has to be of type 'int'"}
    except KeyError:
        return {'error': "Key 'reportedCases' not found"}

    # normalize timeToElapse to days
    days = 0
    if data['periodType'].lower() == 'months':
        days = data['timeToElapse'] * 30
    elif data['periodType'].lower() == 'weeks':
        days = data['timeToElapse'] * 7
    elif data['periodType'].lower() == 'days':
        days = data['timeToElapse']
    else:
        return {'error': "Key 'periodType' has to be one of the following: "
                         "weeks, months or days"}

    # Calculate currentlyInfected based on elapsed day sets
    impact['infectionsByRequestedTime'] = impact['currentlyInfected'] * (2 ** (days // 3))
    severeImpact['infectionsByRequestedTime'] = severeImpact['currentlyInfected'] * \
        (2 ** (days // 3))

    # Challenge 2
    # calculate severe cases and available beds
    impact['severeCasesByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.15)
    severeImpact['severeCasesByRequestedTime'] = int(severeImpact['infectionsByRequestedTime'] *
                                                     0.15)

    available_beds = data['totalHospitalBeds'] * 0.35

    impact['hospitalBedsByRequestedTime'] = int(available_beds -
                                                impact['severeCasesByRequestedTime'])
    severeImpact['hospitalBedsByRequestedTime'] = int(available_beds -
                                                      severeImpact['severeCasesByRequestedTime']
                                                      )

    # Challenge 3
    impact['casesForICUByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.05)
    severeImpact['casesForICUByRequestedTime'] = int(severeImpact['infectionsByRequestedTime'] *
                                                     0.05)

    impact['casesForVentilatorsByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.02)
    severeImpact['casesForVentilatorsByRequestedTime'] = \
        int(severeImpact['infectionsByRequestedTime'] * 0.02)

    impact['dollarsInFlight'] = round(impact['infectionsByRequestedTime'] *
                                      data['region']['avgDailyIncomePopulation'] *
                                      data['region']['avgDailyIncomeInUSD'] * days, 2)
    severeImpact['dollarsInFlight'] = round(severeImpact['infectionsByRequestedTime'] *
                                            data['region']['avgDailyIncomePopulation'] *
                                            data['region']['avgDailyIncomeInUSD'] * days, 2)

    return {'data': data, 'impact': impact, 'severeImpact': severeImpact}

# handle decimal place for money
