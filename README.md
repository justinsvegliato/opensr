# OpenSR
// TODO

# Installation

To install OpenSR, we just need to do the steps below:

1. First, let's sign up for a Cloud9 IDE account [here](https://c9.io/web/sign-up/free). Note that you need to activate your account after signing up. You should receive an email within 5 minutes after registering that contains an activation link.

2. After we've signed up and activated our account, let's log into Cloud9 [here](https://c9.io/signin.html). It'll take a few seconds to load your account for the first time. The page that'll you'll be redirected is your dashboard.

3. It's now time to create our first workspace. To do so, you can either click [here](https://c9.io/new) or just click the box that says "Create a new workspace" on your dashboard. This will bring up a form that allows you to create your first project.

4. Now we need to fill out the form on this page. 
 
  1. Enter *opensr* for the *Workspace name* input.
  
  2. Enter *OpenSR* for the *Description* input.
  
  3. Click the *Public* checkbox under *Hosted workspace*. This will let everyone see your instance of OpenSR. 
  
  4. Enter *https://github.com/justinsvegliato/opensr.git* for the *Clone from Git or Mercurial URL* input. This specifies where to grab the OpenSR code from!
  
  5. Click *Django* under *Choose a template*. We do this because OpenSR is built using Django and Python.
  
  6. Click *Create workspace* to build your workspace using the information you just supplied. This might take a few minutes and will probably show you a few loading displays.
  
5. In the bottom of your screen, you'll see a tab labeled *bash.* In this console, we'll simply type the text below and press enter:
```bash
./install.sh
```
Don't worry about what this does specifically. It's just installing a few things that we need on the server. If you're asked a yes or no question, simply type *Y* and then press enter!