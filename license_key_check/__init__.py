# import libs
import requests
import json
from loguru import logger


def check_license(license_url_list, license_key, debug=False):
    if debug == True:
        logger.debug('Starting script')
    if debug == True:
        logger.debug('Fetching current date and time from timeapi.io in JSON')
    try:
        today = requests.get(
            "https://timeapi.io/api/Time/current/coordinate").json()
        if debug == True:
            logger.info("Fetched JSON data, saved dict to 'today'")
    except requests.exceptions.RequestException as error:
        if debug == True:
            logger.error("Failed to fetch TimeAPI.io\nException: " + str(error))
        return(-406)
    if debug == True:
        logger.debug("Setting 'to_day' from dict 'today'")
    to_day = today["day"]
    if debug == True:
        logger.info("Setted 'to_day' to: " + str(to_day))
    if debug == True:
        logger.debug("Setting 'to_month' from dict 'today'")
    to_month = today["month"]
    if debug == True:
        logger.info("Setted 'to_month' to: " + str(to_month))
    if debug == True:
        logger.debug("Setting 'to_year' from dict 'today'")
    to_year = today["year"]
    if debug == True:
        logger.info("Setted 'to_year' to: " + str(to_year))
    if debug == True:
        logger.debug("Fetching JSON license list from: " + license_url_list.split("/")[2] + "...")
    try:
        data = requests.get(license_url_list).json()
        if debug == True:
            logger.info("Fetched JSON data, saved to dict 'data'")
    except requests.exceptions.RequestException as error:
        if debug == True:
            logger.error("Failed to fetch JSON license list\nException: " + str(error))
        return(-406)
    if debug == True:
        logger.debug("Checking license key in license list")
    if license_key in data:  # check if license exists
        check_license.id = int(data[license_key]["id"])
        license_json = data[license_key]
        if debug == True:
            logger.info("License key in a license list, license info:\n" + str(json.dumps(license_json, indent = 2)))
        if debug == True:
            logger.debug("Checking whether the license key expired")
        check_license.expire = data[license_key]["expire"]
        exp_day = int(data[license_key]["expire"].split(".")[0])
        exp_month = int(data[license_key]["expire"].split(".")[1])
        exp_year = int(data[license_key]["expire"].split(".")[2])
        if exp_day <= to_day and exp_month <= to_month and exp_year <= to_year:  # check if license is not expired
            if debug == True:
                logger.info("License key expired! The license key valid until: " +
                            str(exp_day) + "." + str(exp_month) + "." + str(exp_year))
            return(-1)
        else:
            if debug == True:
                logger.info("License key valid! The license key valid until: " +
                            str(exp_day) + "." + str(exp_month) + "." + str(exp_year))
            return(1)
    else:
        if debug == True:
            logger.info("Key not found in license list")
        return(0)
