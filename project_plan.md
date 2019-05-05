# Project Plan

+ Initialize repo
+ Break down stories
+ Flesh out tasks


## High level tasks:
User management: (Backend & frontend)  
  - registration  
  - Authentication (token Authentication)  
  - One-time password sent to user on registration  

Bank Account management: (Backend & frontend)  
  - Account creation  
  - Account deposit  
  - Account withdrawal (limits on withdrawals)  
  - Account reports (transactions)  

Project setup:

1. Github hook for slack notifications - done
2. Integrate with circleci for continuous integration
3. Deploy project on Heroku

Obvious but worth noting:
  - Follow PEP8 coding style guide
  - TDD all the way
  - Data needs to be persisted (Postgres)
  - REST API
  - Documentation.
  - GIT (Feature branch workflow)


  # Banking app API



  - Slack hook to notify on PRs raised Done
  Good to have: notifications

## API:
Actions:
  + User register  
    Inputs:
        - fname
        - lname
        - email
    Return:
        - email with link to change password
  + User set password
        - password diff between OTP
  + Get username & password and return token
    Inputs:  
        - email
        - password
    Return:
        -token

  + Deposit
    Inputs:
        - amount
        - type
        -
    Return:
        - success/ failure
        - notification
  + Withdraw
    Inputs:
        - amount
        - type
        -
    Return:
        - success/ failure
        - notification
  + Transfer (V2)


## FRONTEND:
  To consume API
  Design to be updated

api/v1/auth/register

- Add user register ()
api/v1/auth/login

### MODELS
Banking models:
- Banking User
  + user id (pk)
  + id_number (charfield)
  + picture (imagefield)
  + email (emailfield)
  + date_of_birth (date_field)
  + physical_address (charfield)
  + proof of address (file)
  + verified (boolean)

- Account
  + banking (User object)
  + account_no (PK)
  + account type (charfield with options)
  + account name (charfield)
  + description (textfield)
  + balance (longint)
  + active (boolean)
  + created at date (datefield)
  + archived at date (datefield)

- Transactions
  + transcation_id (PK)
  + timestamp (datefield)
  + account (FK-> account)
  + type (charfield with options)
  + description (charfield)
  + amount (longint)
