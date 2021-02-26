import pytz
import random
from datetime import datetime, time
import pandas as pd
import pycountry


def findtz(df):
    TIMELO = time(17, 0)
    TIMEHI = time(18, 0)
    tzs = list(pytz.common_timezones_set)
    random.shuffle(tzs)

    for tz in tzs:
        local = datetime.now(pytz.timezone(tz)).time()
        if TIMELO <= local <= TIMEHI:
            matches = df[df.timezone.isin([tz])]
            if not matches.empty:
                place = matches.sample(1).iloc[0]
                return place


def getStateName(country, state, adminCodes):
    code = country + "." + state
    return adminCodes[adminCodes["admincode"] == code].iloc[0]["state"]


def main():
    data = pd.read_csv(
        "cities15000.txt",
        delimiter="\t",
        header=None,
        usecols=[2, 4, 5, 8, 10, 17],
        names=["city", "lat", "long", "country", "state", "timezone"],
    )

    codes = pd.read_csv(
        "admincodes.txt",
        delimiter="\t",
        header=None,
        usecols=[0, 1],
        names=["admincode", "state"],
    )

    location = findtz(data)
    if location is not None:
        country = pycountry.countries.get(alpha_2=location.country).name
        state = getStateName(location.country, location.state, codes)

        print(
            "It's 5 o'clock in " + location.city + ", " + state + ", " + country + "."
        )


if __name__ == "__main__":
    main()