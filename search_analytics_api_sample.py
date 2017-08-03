#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example for using the Google Search Analytics API (part of Search Console API).
A basic python command-line example that uses the searchAnalytics.query method
of the Google Search Console API. This example demonstrates how to query Google
search results data for your property. Learn more at
https://developers.google.com/webmaster-tools/
To use:
1) Install the Google Python client library, as shown at https://developers.google.com/webmaster-tools/v3/libraries.
2) Sign up for a new project in the Google APIs console at https://code.google.com/apis/console.
3) Register the project to use OAuth2.0 for installed applications.
4) Copy your client ID, client secret, and redirect URL into the client_secrets.json file included in this package.
5) Run the app in the command-line as shown below.
Sample usage:
    $ python search_analytics_api_sample.py 'https://www.example.com/' '2015-05-01' '2015-05-30'
"""
import json
import argparse
import xlsxwriter
import sys
import datetime
import math
from googleapiclient import sample_tools

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_uri', type=str,
                                             help=('Site or app URI to query data for (including '
                                                         'trailing slash).'))
argparser.add_argument('start_date', type=str,
                                             help=('Start date of the requested date range in '
                                                         'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                                             help=('End date of the requested date range in '
                                                         'YYYY-MM-DD format.'))


def main(argv):
    service, flags = sample_tools.init(
            argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
            scope='https://www.googleapis.com/auth/webmasters.readonly')

    # First run a query to learn which dates we have data for. You should always
    # check which days in a date range have data before running your main query.
    # This query shows data for the entire range, grouped and sorted by day,
    # descending; any days without data will be missing from the results.
    # request = {
    #     'startDate': flags.start_date,
    #     'endDate': flags.end_date,
    #     'dimensions': ['date']
    # }
    # response = execute_request(service, flags.property_uri, request)
    # print_table(response, 'Available dates')

    # Get totals for the date range.
    # request = {
    #     'startDate': flags.start_date,
    #     'endDate': flags.end_date
    # }
    # response = execute_request(service, flags.property_uri, request)
    # print_table(response, 'Totals')

    # Get top 10 queries for the date range, sorted by click count, descending.
    request = {
            'startDate': flags.start_date,
            'endDate': flags.end_date,
            'dimensions': ['query'],
            'rowLimit': 25
    }
    response = execute_request(service, flags.property_uri, request)
    write_file(response, 'Top Queries')

    # Get top 11-20 mobile queries for the date range, sorted by click count, descending.
    # request = {
    #     'startDate': flags.start_date,
    #     'endDate': flags.end_date,
    #     'dimensions': ['query'],
    #     'dimensionFilterGroups': [{
    #         'filters': [{
    #             'dimension': 'device',
    #             'expression': 'mobile'
    #         }]
    #     }],
    #
    #     'startRow': 10
    # }
    # response = execute_request(service, flags.property_uri, request)
    # print_table(response, 'Top 11-20 Mobile Queries')

    # Get top 10 pages for the date range, sorted by click count, descending.
    # request = {
    #     'startDate': flags.start_date,
    #     'endDate': flags.end_date,
    #     'dimensions': ['page'],
    #     'rowLimit': 10
    # }
    # response = execute_request(service, flags.property_uri, request)
    # print_table(response, 'Top Pages')

    # Get the top 10 queries in India, sorted by click count, descending.
    # request = {
    #     'startDate': flags.start_date,
    #     'endDate': flags.end_date,
    #     'dimensions': ['query'],
    #     'dimensionFilterGroups': [{
    #         'filters': [{
    #             'dimension': 'country',
    #             'expression': 'ind'
    #         }]
    #     }],
    #     'rowLimit': 10
    # }
    # response = execute_request(service, flags.property_uri, request)
    # print_table(response, 'Top queries in India')

    # Group by both country and device.
    # request = {
    #     'startDate': flags.start_date,
    #     'endDate': flags.end_date,
    #     'dimensions': ['country', 'device'],
    #     'rowLimit': 10
    # }
    # response = execute_request(service, flags.property_uri, request)
    # print_table(response, 'Group by country and device')


def execute_request(service, property_uri, request):
    """Executes a searchAnalytics.query request.
    Args:
        service: The webmasters service to use when executing the query.
        property_uri: The site or app URI to request data for.
        request: The request to be executed.
    Returns:
        An array of response rows.
    """
    return service.searchanalytics().query(
            siteUrl=property_uri, body=request).execute()


def write_file(response, title):

    # Create an new Excel file and add a worksheet.
        dateNow = datetime.datetime.now()
        reportDate = dateNow.strftime("%Y-%m-%d")
        workbook = xlsxwriter.Workbook('SEO_report.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 20)
        worksheet.write("A1", "Keys")
        worksheet.write("B1", "Clicks")
        worksheet.write("C1", "Position")

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})
        rows = response['rows']

        count = 1
        for row in rows:
            count = count + 1
            columnKeys = "A%d" % (count)
            columnClicks = "B%d" % (count)
            columnPosition = "C%d" % (count)
            if 'keys' in row:
                keys = u','.join(row['keys']).encode('utf-8')
                worksheet.write(columnKeys, keys)
                clicks = row['clicks']
                clicks = math.ceil(clicks*100)/100
                worksheet.write(columnClicks, clicks)
                position = row['position']
                position = math.ceil(position*100)/100
                worksheet.write(columnPosition, position)

        workbook.close()

    # print title + ':'

    # if 'rows' not in response:
    #   print 'Empty response'
    #   return

    # rows = response['rows']
    # row_format = '{:<20}' + '{:>20}' * 4
    # print row_format.format('Keys', 'Clicks', 'Impressions', 'CTR', 'Position')
    # file.write(row_format.format('Keys', 'Clicks', 'Impressions', 'CTR', 'Position\n'))
    # for row in rows:
    #   keys = ''
    #   # Keys are returned only if one or more dimensions are requested.
    #   if 'keys' in row:
    #     keys = u','.join(row['keys']).encode('utf-8')
    #   print row_format.format(
    #       keys, row['clicks'], row['impressions'], row['ctr'], row['position'])
    #   file.write(row_format.format(keys, row['clicks'], row['impressions'], row['ctr'], row['position']))
    #   file.write("\n")

    # file.close()

def print_table(response, title):
    """Prints out a response table.
    Each row contains key(s), clicks, impressions, CTR, and average position.
    Args:
        response: The server response to be printed as a table.
        title: The title of the table.
    """
    print title + ':'

    if 'rows' not in response:
        print 'Empty response'
        return

    rows = response['rows']
    row_format = '{:<20}' + '{:>20}' * 4
    print row_format.format('Keys', 'Clicks', 'Impressions', 'CTR', 'Position')
    for row in rows:
        keys = ''
        # Keys are returned only if one or more dimensions are requested.
        if 'keys' in row:
            keys = u','.join(row['keys']).encode('utf-8')
        print row_format.format(
                keys, row['clicks'], row['impressions'], row['ctr'], row['position'])

if __name__ == '__main__':
    main(sys.argv)
