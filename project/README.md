This web application is made for nonprofits that use a monthly donation program to support themselves.
It uses GoCardless to take payments, and connects to the GoCardless API to draw customer information out in the form of a first name and last initial, and donation amount.

Users can log in to view their subscriptions, and can change to one of the 3 other subscription options from the My Subscriptions page.
The Behind the Scenes page is visible only to logged in users, and shows the work that the nonprofit is doing using donor money.

The counters on the homepage loop through GoCardless details: one counts up the total number of donations received by the nonprofit per month, and the other the total number of donors.
When a user donates through GoCardless, their patronage and donation amount are automatically reflected in the counters.
This gives potential donors a sense that their contributions really work towards a significant monthly income for the nonprofit and they are part of its progress.

One-off donations are not counted as the application aims to encourage regular, small contributions over single sums.
When a subscription is cancelled, the loop skips over them and they are removed from the patron board and counters.