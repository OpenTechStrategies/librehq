# Initial Project Outline

## Step 1 - Single instance

1. Initial setup
   * flask set up, basic documentation, submodule setup
1. Integrate initial setup from librehq-wikis

## Step 2 - Multi instance

1. Integrate Step 2 from librehq-wikis

## Step 3 - Account federation

1. Add account concept to codebase
   * DB setup (postgres), migration, model
       * username, password for now, to be minimal to get something working approximately how we want
   * Will be learning python db tools as I go
1. Add signup ability
   * Replace index page with signup page
   * Email validation
   * Add validation key to database
   * Is there a standard python tool for this out there?
1. Add signin ability
   * Enhance index page with login or signup
   * After signing in, takes you to the previously created "add a media wiki instance from csv"

## Step 4 - Wiki maintenace - wikis

1. Integrate Step 4 from librehq-wikis

## Step 5 - Error checking

1. Account error checking
   * email address, username, duplication
   * Is there a current way python community does this?
1. Integrate Step 5 from librehq-wikis

## Step 6 - Csv2Wiki upload specifications

1. Integrate Step 6 from librehq-wikis

## Step 7 - ansible

1. Add ansible implementation of installation documentation
1. Add installation instructions that point to ansible script
