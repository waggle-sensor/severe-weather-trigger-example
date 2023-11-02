# Severe Weather Trigger Example

This is a short example of a Sage Cloud to Edge trigger which starts and stops jobs in response to severe weather events scraped from the National Weather Service API.

## Design

This trigger example works roughly as follows:

```sh
       User creates job
       once at start using
       sesctl and auth token.
[ Job ] ----------------> [ SES [Job] ]
                                  ^
                                  |
                                  |
             This example suspend / resumes job based
             on severe weather events each time it runs
             using sesctl and auth token.
```
