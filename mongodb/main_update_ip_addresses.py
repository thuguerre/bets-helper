# Python script inspired from:
# https://github.com/mongodb-developer/Travic-CI-to-Atlas-IP-Access-Lister/blob/master/github-actions-access-lister.py

import requests
from requests.auth import HTTPDigestAuth
from pprint import pprint
import configparser
import os
import sys
import json
from typing import List
import logging

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from LocalExecHelper import LocalExecHelper

def get_current_mongodb_ip_addresses(group_id: str, public_key: str, private_key: str) -> List[str]:

    mongodb_address_list_text = json.loads(requests.get(url=f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{group_id}/accessList?pretty=true",
        auth=HTTPDigestAuth(public_key, private_key)).text)

    mongodb_address_list = []
    for result in mongodb_address_list_text["results"]:
        if "0.0.0.0/0" not in result["cidrBlock"]:
            mongodb_address_list.append(result["cidrBlock"].split("/")[0])
            logging.debug("adding address : " + result["cidrBlock"].split("/")[0])

    return mongodb_address_list


def delete_mongodb_ip_addresses(group_id: str, public_key: str, private_key: str, ip_addresses: List[str]):

    # Format the IP Addresses to have associated comments that we will store in Atlas
    ip_addresses_to_delete = []
    for address in ip_addresses:
        r = requests.delete(url=f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{group_id}/accessList/{address}",
            auth=HTTPDigestAuth(public_key, private_key))    
        
        logging.debug(r)
        logging.debug(r.text)


def get_githubactions_addresses() -> List[str]:

    # Get the list of IP Addresses that GitHub uses
    temp_githubactions_addresses = requests.get('https://api.github.com/meta').json()["actions"]

    githubactions_addresses = []
    for address in temp_githubactions_addresses:
        if "::" not in address:
            githubactions_addresses.append(address)
    
    return githubactions_addresses

def update_mongodb_ip_addresses(group_id: str, public_key: str, private_key: str, github_actions_ip_addresses: List[str]):

    # Format the IP Addresses to have associated comments that we will store in Atlas
    authorized_ip_addresses = []
    for address in github_actions_ip_addresses:
        authorized_ip_addresses.append({
            "ipAddress": address,
            "comment": "IP Address for GitHub Actions"
        })

    authorized_ip_addresses.append({
        "ipAddress": "92.158.86.29",
        "comment": "Thomas Huguerre's IP Address"
    })

    # Make the POST request to add the IP addresses to the Access List
    r = requests.post(url=f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{group_id}/accessList?pretty=true",
        auth=HTTPDigestAuth(public_key, private_key), json=authorized_ip_addresses)
    
    logging.debug(r)
    logging.debug(r.text)

#
# Main Function
#
if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)

    try:
        os.environ["MONGODB_NAME"]
    except KeyError:
        LocalExecHelper()

    group_id = os.environ["MONGODB_GROUP_ID"]
    public_key = os.environ["MONGODB_PUBLIC_KEY"]
    private_key = os.environ["MONGODB_PRIVATE_KEY"]

    current_mongodb_ip_addresses = get_current_mongodb_ip_addresses(group_id, public_key, private_key)
    delete_mongodb_ip_addresses(group_id, public_key, private_key, current_mongodb_ip_addresses)

    github_actions_ip_addresses = get_githubactions_addresses()
    update_mongodb_ip_addresses(group_id, public_key, private_key, [])
    