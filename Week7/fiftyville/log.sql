-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find crimes that happened on JULY 28 on Humphrey Street
SELECT description
    FROM crime_scene_reports
    WHERE month = 7
    AND day = 28
    AND street = "Humphrey Street";

-- Theft at 10:15 am
-- check  interviews
SELECT name, transcript
    FROM interviews
    WHERE month = 7
    AND day = 28;

--| Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
--If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |

SELECT name, activity, people.license_plate, hour, minute
    FROM bakery_security_logs, people
    WHERE month = 7
    AND day = 28
    AND people.license_plate = bakery_security_logs.license_plate
    AND activity = "exit"
    AND hour = 10
    AND minute <= 25;

-- Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana

--| Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
--I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

--| Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard
--the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on
--the other end of the phone to purchase the flight ticket.

-- Check atm_transactions on Leggett Street
SELECT name, atm_transactions.account_number, amount
    FROM atm_transactions, bank_accounts, people
    WHERE atm_location = "Leggett Street"
    AND transaction_type = "withdraw"
    AND month = 7
    AND day = 28
    AND atm_transactions.account_number = bank_accounts.account_number
    AND bank_accounts.person_id = people.id;

--|  name   | account_number | amount |
--+---------+----------------+--------+
--| Bruce   | 49610011       | 50     | -
--| Diana   | 26013199       | 35     | -
--| Brooke  | 16153065       | 80     |
--| Kenny   | 28296815       | 20     |
--| Iman    | 25506511       | 20     |
--| Luca    | 28500762       | 48     | -
--| Taylor  | 76054385       | 60     |
--| Benista | 81061156       | 30     |

-- Check phone_calls for duration <1 min
SELECT caller, receiver, duration
    FROM phone_calls
    WHERE month = 7
    AND day = 28
    AND duration < 60;

SELECT receiver, duration
    FROM phone_calls
    WHERE month = 7
    AND day = 28
    AND caller = (SELECT phone_number
        FROM people
        WHERE name = "Bruce")

SELECT name
    FROM people
    WHERE phone_number = "(375) 555-8161";

-- Check flights for earlies flight 07/29 out of Fiftyville
SELECT id, destination_airport_id, hour, minute
    FROM flights
    WHERE month = 7
    AND DAY = 29
    AND origin_airport_id = (
        SELECT id from airports
            WHERE city = "Fiftyville"
    )
    ORDER BY hour ASC, minute;
-- id 36, destination_airport_id = 4, hour 8, minute 20
SELECT name, seat
    FROM passengers, people
    WHERE flight_id = 36
    AND people.passport_number = passengers.passport_number;
