# Database Tables
this file tells you about the name, purpose, and the contents for each db tables

## all DB tables
- users (communication info and reputation)
- stalls (location, facilities, and owner)
- slots (time and price)
- bookings (transaction records)

## purpose and content for each table

### `users`
stores the name, communication info, reputation score, and the time they created the account.

- `user_id`: auto generated integer. start from 1, and keep adding as new users joined
- `line_uid`: string, upto 255 characters. can't be same as others'
- `name`: string, upto 100 characters. the user's name
- `phone`: string, upto 20 characters. the user's phone number
- `category`: string, upto 50 characters. whether they are owner or renter
- `reputation_score`: integer, default as 100. to track a user's trustworthiness. the score will drop if they frequently cancel their orders.
- `created_at`: timestamp. the exact time the user's info is written into the database.

### `stalls`
stores the location name, latitude and longitude, facilities, and owner id

- `stall_id`: auto generated integer. start from 1, and keep adding as new stalls added
- `location_name`: string, upto 100 characters. the name of the location (eg: XXX district XXX avenue number XX)
- `lat`: decimal XXX.XXXXXX. latitude of the location
- `long`: decimal XXX.XXXXXX. longitude of the location
- `facilities`: plain text. the facilities avilable at the location (eg: water, electricity)
- `owner_id`: integer. the stall's owner's id

### `slots`
stores the stall id, date, price, and the avilability status for the stall.
- `slot_id`: auto generated integer. start from 1, and keep adding as new stalls added
- `stall_id`: integer, auto linked to `stall_id` on the table `stalls`
- `date`: date, cannot be empty. the scheduled date to start using the stall
- `price`: integer, cannot be empty. the price for renting the stall
- `status`: integer, default at 0. the status for the availability. 0: available, 1: locked, 2: booked, 3: under maintenance.


### `bookings`
stores the booked informations, including the slot, the user (renter), payment status, qr code token, and the time the deal is made.
- `booking_id`: auto generated integer. start from 1, and keep adding as new deals being made
- `slot_id`: integer, auto linked to the `slot_id` on the table `slots`.
- `user_id`: integer, auto linked to the `user_id` on the table `user`.
- `payment_status`: string, upto 20 characters, default as "PENDING". to track whether the money is paid
- `payment_method`: string, upto 50 characters. the payment method of this booking.
- `qr_token`: string, upto 100 characters. the qr code token
- `created_at`: timestamp. the exact time the deal is made.
