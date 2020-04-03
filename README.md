# raspberrypi_projects

- Some interesting projects to run on raspberrypi

## NS Train Notification
This project is to subscribe a set of destinations and continuously check the train status. Once there is any delay >=5 mins then a notification email will be sent to the email address.

__workflow__
- Look up your starting and ending destination code
- Set your travel routines: at what time you would like to take the train
- Set your email credentials in .env file so that email could be sent
- Done-> receive the notification for train cancellation and delay!
