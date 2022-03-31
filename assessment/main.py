import unittest
from unittest import TestCase

import pytest
import requests
import json
import logging

## Global variables and functions
from pytest import fail


class XharkTankAssessment(TestCase):

    HEADERS = None

    def __init__(self, *args, **kwargs):

        unittest.TestCase.__init__(self, *args, **kwargs)
        self.HEADERS = {"Content-Type": "application/json"} # "X-Firebase-Auth": "INTERNAL_IMPERSONATE_USER_" + str(user),
        self.localhost = 'http://localhost:8081/'

        self.POSITIVE_STATUS_CODES = [200, 201, 202, 203]
        self.NEGATIVE_STATUS_CODES = [400, 401, 402, 403, 404, 405, 409]

    ### Helper functions
    def get_api(self, endpoint):
      
        response = requests.get(self.localhost + endpoint, headers=self.HEADERS)
        self.print_curl_request_and_response(response)
        return response

    def post_api(self, endpoint, body):
       
        response = requests.post(self.localhost + endpoint, headers=self.HEADERS, data=body)
        self.print_curl_request_and_response(response)
        return response

    def print_curl_request_and_response(self, response):
    
        if(response.status_code in self.POSITIVE_STATUS_CODES):
         
            self.decode_and_load_json(response)

    def patch_api(self, endpoint, body):
       
        response = requests.patch(self.localhost + endpoint, headers = self.HEADERS, data = body)
        self.print_curl_request_and_response(response)
        return response

    def decode_and_load_json(self, response):
        try:
            text_response = response.content.decode('utf-8')
            data = json.loads(text_response)
        except Exception as e:
          
            logging.exception(str(e))
            return response
        return data

    def checkKey(self,dict,key):
        if key in dict:
            return True
        else:
            return False
    ### Helper functions end here

    @pytest.mark.order(1)
    def test_1_get_all_pitches_when_empty_db(self):
        """When run with empty database, get all pitches should return success, and response should be an empty list """
        endpoint = 'pitches'
        response = self.get_api(endpoint)
        self.assertEqual(response.status_code, 200)
        response_length = len(self.decode_and_load_json(response))
        self.assertEqual(response_length, 0)

    @pytest.mark.order(2)
    def test_2_post_pitch(self):
        """Post a Pitch and verify that it returns id in the response"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#1",
            "pitchTitle": "Sample Title #1",
            "pitchIdea" : "Sample Idea #1",
            "askAmount" : 1000000000,
            "equity": 25.3
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        self.assertEqual(len(data))


    @pytest.mark.order(3)
    def test_3_get_single_pitch(self):
        """Given a pitch id verify that it returns that pitch"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#2",
            "pitchTitle": "Sample Title #2",
            "pitchIdea" : "Sample Idea #2",
            "askAmount" : 1000000000,
            "equity": 25.3
        }

        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        self.assertEqual(len(data))
        endpoint = 'pitches/{}'.format(data["id"])
        response = self.get_api(endpoint)
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        self.assertTrue(self.checkKey(data,"entrepreneur"))
        self.assertTrue(self.checkKey(data,"pitchIdea"))
        self.assertTrue(self.checkKey(data,"pitchTitle"))
        self.assertTrue(self.checkKey(data,"askAmount"))
        self.assertTrue(self.checkKey(data,"equity"))
        self.assertTrue(self.checkKey(data,"offers"))
        body["id"] = data["id"]
        body["offers"] = []
        self.assertDictEqual(body,data)


    @pytest.mark.order(4)
    def test_4_get_all_pitches_when_pitches_present_in_db(self):
        """Get all pitches and verify that it returns all pitches"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#3",
            "pitchTitle": "Sample Title #3",
            "pitchIdea" : "Sample Idea #3",
            "askAmount" : 1000000000,
            "equity": 25.3
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        response = self.get_api(endpoint)
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        response_length = len(self.decode_and_load_json(response))
        self.assertEqual(response_length, 3)


    @pytest.mark.order(5)
    def test_5_post_offer(self):
        """Post an Offer and verify that it returns id in the response"""
        endpoint = 'pitches'
        body = {
            "entrepreneur": "Yakshit#4",
            "pitchTitle": "Sample Title #4",
            "pitchIdea" : "Sample Idea #4",
            "askAmount" : 1000000000,
            "equity": 25.3
        }

        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))
        endpoint = 'pitches/{}/makeOffer'.format(data["id"])
        body = {
            "investor": "Anupam Mittal",
            "amount" : 1000000000,
            "equity": 25.3,
            "comment":"A new concept in the ed-tech market. I can relate with the importance of the Learn By Doing philosophy. Keep up the Good Work! Definitely interested to work with you to scale the vision of the company!"
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        self.assertTrue(self.checkKey(data,"id"))



if __name__ == '__main__':
    unittest.main()


