from celery import shared_task, Celery
from celery.schedules import crontab
import csv
import os
from flask import current_app
from Applications.models import User, Books, Request, Section
from Applications.utils import send_email
from jinja2 import Template
from datetime import timedelta

import requests


#this task will check whether the user has visited or not
@shared_task
def check_visited_users():
       with current_app.app_context():
                
                template_str = """
                        <p>
                        Hi {{ username }}!
                        </p>
                        <br />
                        <p>
                        We’ve noticed you haven’t been around lately. Come back and explore the latest additions to our collection at LibKit.
                        </p>
                        <br />
                        <p>
                        We can't wait to have you back,
                        </p>
                        <p>
                        LibKit team
                        </p>
                """


                try:
                      response = requests.get('http://127.0.0.1:5000/visited')
                      if response.status_code == 200:
                              not_visited_users = response.json()
                              for user in not_visited_users:
                                     template = Template(template_str)
                                     address=user['email']
                                     subject = "We miss you!"
                                     message = template.render(username=user['username'])
                                     send_email(address, subject, message)
                                     

                except Exception as e:
                      print(f"Error occurred: {e}")
                      return f"Failed to check visited users. Error: {e}"

                     

#This task will create and send the monthly report 
@shared_task
def generate_monthly_report():
    with current_app.app_context():
        try:
            response = requests.get('http://127.0.0.1:5000/monthly_report')
            if response.status_code == 200:
                report = response.json()
                # Prepare email content
                template_str = """
                    <p>
                        Dear admin,
                    </p>
                    <br />
                    <p>
                        Attached is the monthly report for the library.
                    </p>
                    <p>
                        Number of Sections: {{ number_of_sections }}
                    </p>
                    <p>
                        Number of Books: {{ number_of_books }}
                    </p>
                    <p>
                        Number of Users: {{ number_of_users }}
                    </p>
                    <p>
                        Number of Books Issued: {{ number_of_books_issued }}
                    </p>
                    <br />
                    <p>
                        Best regards,
                    </p>
                    <p>
                        LibKit team
                    </p>
                """
                template = Template(template_str)
                subject = "Monthly Library Report"
                message = template.render(
                    number_of_sections=report['number_of_sections'],
                    number_of_books=report['number_of_books'],
                    number_of_users=report['number_of_users'],
                    number_of_books_issued=report['number_of_books_issued']
                )
                address = "libkit@admin.com"

                # Create CSV file for book details
                csv_filename = 'monthly_report_books.csv'
                with open(csv_filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(["ID", "Title", "Author", "Rating"])
                    for book in report['books']:
                        writer.writerow([book['id'], book['title'], book['author'], book['rating']])

                # Attach CSV file to email
                with open(csv_filename, 'rb') as f:
                    send_email(address, subject, message, attachment=f, filename=csv_filename, subtype="csv")

                # Clean up the CSV file
                os.remove(csv_filename)

                return f'Monthly report generated and sent successfully.'
            else:
                raise Exception(f"API request failed with status code {response.status_code}")
        except Exception as e:
            print(f"Error occurred: {e}")
            return f"Failed to generate monthly report. Error: {e}"








#this task will export book cycle csv

@shared_task
def export_books_cycle_to_csv():        

        with current_app.app_context():

                # Create CSV file
                csv_filename = 'books_cycle.csv'
                with open(csv_filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(["User Name", "Book Title", "Author", "Genre", "Request Date", "Return Date"])
                    
                    try:
                
                        response = requests.get('http://127.0.0.1:5000/book_cycle')
                
                        # Check if the request was successful
                        if response.status_code == 200:
                                books_list = response.json()
                                for book in books_list:
                                        writer.writerow([book['user'], book['book'], book['author'], book['section'], book['issued_date'], book['return_date']])
                        else:        
                                raise Exception(f"API request failed with status code {response.status_code}")
                    except Exception as e:
                                print(f"Error occurred: {e}")
                                return f"Failed to export books cycle data. Error: {e}"



                #Prepare email content
                template_str = """
                <p>
                    Dear admin,
                </p>
                <br />
                <p>
                    As requested, we have attached CSV report for {{ cname }} in this email.
                </p>
                <p>
                    If you have any questions or concerns about the report, please don\'t hesitate to reach out to us.
                </p>
                <br />
                <p>
                    Best regards,
                </p>
                <p>
                    LibKit team
                </p>
                """
                template = Template(template_str)
                subject = "Books Cycle Report"
                message = template.render(cname="Books Cycle Report")
                address = "libkit@admin.com"

                # Attach CSV file to email
                with open(csv_filename, 'rb') as f:
                    send_email(address, subject, message, attachment=f, filename=csv_filename, subtype="csv")

                # Clean up the CSV file
                os.remove(csv_filename)

                return f'Exporting request to CSV file is done successfully at {csv_filename}'


