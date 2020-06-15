# Code test

## Overview
This test is designed to be small enough to not take too much time,
but loose enough that you will be able to show your own
architectural solutions as well as your code structure.

### Hypothetical background
The application is a small service, which accepts data from a GPS tracker device.
In the beginning of a track, it requests a route to be created,
then continuously populates it with data points (WGS84 coordinates).
A route is expected to be done within a day, after that the user can't
add more data points.
Eventually a request to get the length of the route is made.

There is also a second part which is to calculate
the longest path for each day.

This information is expected to be highly requested,
and past days can't have new routes included, nor new points added to routes from past days.
This the requests will only query days in the past (queries about the longest route
in the present day will not be made, as the day is still going and new routes can be added).

### Requirements
We have provided you with an acceptance test. This acceptance test is
a positive test for how a web server should ingest information, and output
a calculated result. This test is only for the route length. We don't
provide a test for the second part.

### Delivery
Share a code base with us in any way that makes sense to you,
when you feel that you are done. We expect your code to include a Dockerfile
and a docker-compose.

### Time management
We won’t be timing you. Do your best, show your skills, but keep in mind there
is no reason to overdo it.


