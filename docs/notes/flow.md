# FLOW

## Main Navigation

sitewide: logout (if not logged in)

sitewide: (on show) add/edit HRC & edit horse/rider

## Select Rider

url: showdate/select_rider

* redirs (based on flow type (add hrc, edit horse, edit rider, edit hrc)
    * Rider Detail
    * Select Horse
* sessions
    * save rider_pk

Add New Rider is hidden if flow type != add hrc

## Rider Detail

url: showdate/rider(/pk)

* inputs (session)
    * nothing (if adding rider)
    * rider_pk (if editing rider)
* redirs
    * select_rider (if adding)
    * showpage (if editing)
* session
    * 

## Horse Detail

url: showdate/horse(/pk)

* inputs
    * nothing (if adding)
    * horse_pk (if editing)
* redirs
    * select_horse (if adding)
    * showpage (if editing)
* sessions
    * 


