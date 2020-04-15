def estimator(data):
    """
    function to determine impact and severe impact of covid-19 on a country
    :param data:
    :return:
    """
    # Challenge 1
    # calculate currentlyInfected based on reportedCases
    print(data)
    try:
        if isinstance(data['reportedCases'], int):
            impact = {'currentlyInfected': data['reportedCases'] * 10}
            severeImpact = {'currentlyInfected': data['reportedCases'] * 50}
        else:
            return {}
    except KeyError:
        return {}

    # normalize timeToElapse to days
    days = 0
    try:
        if isinstance(data['timeToElapse'], int):
            if data['periodType'].lower() == 'months':
                days = data['timeToElapse'] * 30
            elif data['periodType'].lower() == 'weeks':
                days = data['timeToElapse'] * 7
            elif data['periodType'].lower() == 'days':
                days = data['timeToElapse']
            else:
                return 'Key "periodType" has to be one of the following: weeks, months or days'
        else:
            return {}
    except AttributeError:
        return {}

    # Calculate currentlyInfected based on elapsed day sets
    days_set = (days // 3)
    impact['infectionsByRequestedTime'] = impact['currentlyInfected'] * (2 ** days_set)
    severeImpact['infectionsByRequestedTime'] = severeImpact['currentlyInfected'] * \
                                                (2 ** days_set)

    # Challenge 2
    # calculate severe cases and available beds
    impact['severeCasesByRequestedTime'] = impact['infectionsByRequestedTime'] * 0.15
    severeImpact['severeCasesByRequestedTime'] = severeImpact['infectionsByRequestedTime'] * 0.15

    if isinstance(data['totalHospitalBeds'], int):
        available_beds = data['totalHospitalBeds'] * 0.35
        impact['hospitalBedsByRequestedTime'] = int(available_beds -
                                                    impact['severeCasesByRequestedTime'])
        severeImpact['hospitalBedsByRequestedTime'] = int(available_beds -
                                                          severeImpact['severeCasesByRequestedTime']
                                                          )
    else:
        return {}

    # Challenge 3
    impact['casesForICUByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.05)
    severeImpact['casesForICUByRequestedTime'] = int(severeImpact['infectionsByRequestedTime'] *
                                                     0.05)

    impact['casesForVentilatorsByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.02)
    severeImpact['casesForVentilatorsByRequestedTime'] = int(severeImpact
                                                             ['infectionsByRequestedTime'] * 0.02)

    impact['dollarsInFlight'] = int(impact['infectionsByRequestedTime'] *
                                    data['region']['avgDailyIncomePopulation'] *
                                    data['region']['avgDailyIncomeInUSD'] / days)
    severeImpact['dollarsInFlight'] = int(severeImpact['infectionsByRequestedTime'] *
                                          data['region']['avgDailyIncomePopulation'] *
                                          data['region']['avgDailyIncomeInUSD'] / days)

    return {'data': data, 'impact': impact, 'severeImpact': severeImpact}
