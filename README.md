# Basic Installation

To install OpenSR, we just need to do the steps below:

1. First, let's sign up for a Cloud9 IDE account [here](https://c9.io/web/sign-up/free). Note that you need to activate your account after signing up. You should receive an email that contains an activation link.

2. After we've signed up and activated our account, let's log into Cloud9 [here](https://c9.io/signin.html). It'll take a few seconds to load your account for the first time. The page that'll you'll be redirected to is your dashboard.

3. It's now time to create our first workspace. To do so, you can either click [here](https://c9.io/new) or just click the box that says "Create a new workspace" on your dashboard. This will bring up a form that allows you to create your first project.

4. We now need to fill out the form on this page. 

  1. Enter **opensr** for the **Workspace name** input.
  
  2. Enter **OpenSR** for the **Description** input.
  
  3. Click the **Public** checkbox under **Hosted workspace**. This will let everyone see your instance of OpenSR.
  
  4. Enter **https://github.com/justinsvegliato/opensr.git** for the **Clone from Git or Mercurial URL** input. This specifies where to grab the OpenSR code from!
  
  5. Click **Django** under **Choose a template**. We do this because OpenSR is built using Django and Python.
  
  6. Click **Create workspace** to build your workspace using the information you just supplied. This might take a few minutes and will probably show you a few loading displays.
  
5. In the bottom of your screen, you'll see a tab labeled *bash.* In this console, we'll simply type the text in the gray box below and then press enter. Don't worry about the details of what this does. It's just installing a few things that we need on the server. **If you're asked a yes or no question, simply type *Y* and then press enter!** Otherwise, the installation won't continue. 

  ```bash
  ./install.sh
  ```

6. Next, we need to get a free database from Heroku. To do that, create a Heroku account by clicking (here)[https://signup.heroku.com/www-home-top]. Again, make sure to check your email to activate the new account. After clicking through the links from the activation email, you should end up at your Heroku dashboard. If not, click (here)[https://id.heroku.com/login] to login.

7. Next, we need to use Heroku to create a free database for us to use. This'll store participant data. 

  1. Click (here)[https://postgres.heroku.com/databases] to create a database.
  
  2. Once we're on that page, click the **Create database** button. This'll display a prompt that provides all the options you can choose from. 
  
  3. We want the free option, so just select **Dev Plan (Free)** and then click **Add Database**. It might take a few minutes to provision the database since it's an involved process, so wait a few minutes and then refresh the page you're on.
  
  4. Once you refresh, you should have a page with just one row. Go ahead and click the purple text of that row. It should start with the text **heroku-postgres**. It'll bring up a new page. Keep this page open. We'll need the this information in the next step.
  
8. Now that we've created a database, we need to plug in the database details into Cloud9. To do so, go back to your OpenSR workspace in Cloud9. On the left hand side of that page, you'll see a navigation pane that contains folders and files. Open up the top folder **opensr** if it's not already open and then open up the other **opensr** . Once we've opened up that folder, click the **settings.py** file. We'll need to change a few aspects of this file to account for the database we've just created.

9. In **settings.py** file, we only need to modify a couple things. Let's start with the database details. Change the information between the single quotes (*'*) for **NAME**, **USER**, **PASSWORD**, **HOST**, and **PORT**. This information is listed on the Heroku page that we kept open from before. Just copy and paste the database details to the **settings.py** file that we have open. Be careful! If we accidentally delete a single quote (**'**) or another character, it might mess up our program!

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'Put the data from the Database field from Heroku here',
          'USER': 'Put the data from the User field from Heroku here',
          'PASSWORD': 'Put the data from the Password field from Heroku Here',
          'HOST': 'Put the data from the Host field from Heroku here',
          'PORT': 'Put the data from the Port field from Heroku here',
      },
  }
  ```

10. While we're at it, let's also change the administrators of the system. Just replace **Your name** and **Your email** with your own information. Again, be careful! 

  ```python
  ADMINS = (
      ('Your name', 'Your email'),
  )
  ```

11. Once we've made those changes, we need to save the file. Simply select **File** at the top of the screen and then click **Save**. All of our information should now be ready!

12. Next, we need to run one more command in the console at the bottom of the Cloud9 workspace. Just type the text in the gray box below and press enter. If any prompts come up, enter **yes**. You might have to create a *superuser*. This is basically an administrator. Just use whatever credentials you feel are appropriate.

  ```bash
  python manage.py syncdb
  ```

13. We're done! To run our application, just enter the text in the gray box below. This will run our application. You can quit the server by pressing the **CONTROL** key and **C** together.
 
  ```bash
  python manage.py runserver $IP:$PORT
  ```

14. To view the application, just go to the link in the gray box below. Make sure to replace **<your_account_name>** with your actual Cloud9 IDE account name that you created at the beginning of this tutorial (make sure to replace the angle brackets (**<**) too)!

  ```python
  http://opensr-c9-<your_account_name>.c9.io/
  ```

15. You probably noticed that you don't have any tests in the dropdown on the page you just went to. Go ahead and create tests by viewing the administrative control panel. Use the link in the gray box below. Again, remember to put your actual account name in the link.

  ```python
  http://opensr-c9-<your_account_name>.c9.io/admin/
  ```
